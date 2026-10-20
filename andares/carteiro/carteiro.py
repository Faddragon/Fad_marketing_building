#!/usr/bin/env python3
"""carteiro - leva cada trabalho de uma etapa a outra. Sem IA, sem internet.

Caminho de um trabalho (a cada 15 s):
  pedidos/<id>.json (skip)  ->  trabalhos/<id>/ficha.json
  conceito: acorda o marketing pela API do Hermes -> conceito-v<N>/ com 'pronto'
  revisao : pede o parecer do skip (revisoes/<id>-conceito-v<N>.json, mesma impressao digital)
  arte    : acorda o marketing de novo -> arte-v<N>/ (post.json + imagens) com 'pronto'
  revisao : parecer do skip sobre a arte
  entrega : copia para prontos/<id>/ -> a expedicao assume (revisao final, codigo do medico, Postiz)

Reprovado: grava devolutiva-<etapa>-v<N+1>.md, anota a licao em licoes.md e refaz.
Duas reprovacoes na mesma etapa: 'parado' (o medico decide).
Ajuste pedido pelo medico depois da previa (avisos/ajuste-<id>.json): recomeca pelo conceito.

O carteiro NAO avalia conteudo. So confere formato, procura dado de paciente por padroes simples
(CPF, 'paciente Fulano Sobrenome') e leva o arquivo adiante. Quem julga e o skip; quem aprova e o medico.

Uso:
  carteiro.py loop              (padrao)
  carteiro.py teste             confere a chave e a API do marketing
  carteiro.py exemplo           cria um pedido de mentira em pedidos/ (testa o caminho todo)
  carteiro.py status            mostra os trabalhos
  carteiro.py reabrir ID [etapa]  tira de 'parado' ou 'erro' e tenta de novo (padrao: a etapa em que parou)
  carteiro.py descartar ID      encerra um trabalho
"""
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

SP = timezone(timedelta(hours=-3))
CORREIO = os.environ.get("CORREIO_DIR", "/correio")
API = os.environ.get("MARKETING_URL", "http://predio-marketing:8642").rstrip("/")
CHAVE = os.environ.get("API_SERVER_KEY", "")
TICK = int(os.environ.get("TICK_SEGUNDOS", "15"))

MAX_REPROVACOES = 2          # na segunda reprovacao da mesma etapa, para
MAX_TENTATIVAS = 3           # tentativas de acordar o marketing por versao (queda, reinicio)
RUN_MAX_MIN = 60             # um run acima disso e cancelado
ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{6}$")
FINAIS = ("entregue", "descartado")
PARADOS = ("parado", "erro")

PEDIDOS = os.path.join(CORREIO, "pedidos")
PESQUISAS = os.path.join(CORREIO, "pesquisas")
TRABALHOS = os.path.join(CORREIO, "trabalhos")
REVISOES = os.path.join(CORREIO, "revisoes")
PRONTOS = os.path.join(CORREIO, "prontos")
AVISOS = os.path.join(CORREIO, "avisos")
LICOES = os.path.join(CORREIO, "licoes.md")

# dado de paciente: padroes simples, so para barrar o obvio. O julgamento de verdade e do skip.
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
RE_CPF_SECO = re.compile(r"\bcpf\D{0,6}\d{11}\b", re.I)
RE_PACIENTE = re.compile(r"\b[Pp]aciente\s+(?:chamad[oa]\s+)?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]{2,}\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]{2,}")
RE_PRONTUARIO = re.compile(r"\bprontu[aá]rio\s*(?:n[ºo°.]*)?\s*\d{3,}", re.I)
PADROES_PACIENTE = [("CPF", RE_CPF), ("CPF", RE_CPF_SECO), ("nome de paciente", RE_PACIENTE),
                    ("numero de prontuario", RE_PRONTUARIO)]
EXT_TEXTO = (".md", ".txt", ".json", ".html", ".csv")
IGNORAR_NA_IMPRESSAO = {"pronto", "erro.txt", "avisos.md"}


# ---------------------------------------------------------------- utilidades

def agora():
    return datetime.now(SP)


def log(msg):
    print(f"{agora():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def ler_json(caminho, padrao=None):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return padrao


def salvar_json(caminho, obj):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, caminho)


def salvar_texto(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, caminho)


def ler_texto(caminho, n=None):
    try:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            return f.read(n) if n else f.read()
    except OSError:
        return ""


def pasta_trabalho(id_):
    return os.path.join(TRABALHOS, id_)


def caminho_ficha(id_):
    return os.path.join(pasta_trabalho(id_), "ficha.json")


def salvar_ficha(f):
    f["atualizado_em"] = agora().isoformat()
    salvar_json(caminho_ficha(f["id"]), f)


def uma_linha(txt, n=300):
    return re.sub(r"\s+", " ", str(txt or "")).strip()[:n]


def buscar_paciente(textos):
    """Devolve o NOME do padrao achado (nunca o trecho), ou None."""
    for t in textos:
        for nome, rx in PADROES_PACIENTE:
            if rx.search(t or ""):
                return nome
    return None


def textos_da_pasta(pasta):
    saida = []
    for raiz, _, arqs in os.walk(pasta):
        for a in arqs:
            if a.lower().endswith(EXT_TEXTO):
                saida.append(ler_texto(os.path.join(raiz, a), 400_000))
    return saida


def impressao(pasta):
    """Impressao digital da pasta: muda se qualquer arquivo (menos os de controle) mudar."""
    h = hashlib.sha256()
    for raiz, dirs, arqs in os.walk(pasta):
        dirs.sort()
        for a in sorted(arqs):
            if a in IGNORAR_NA_IMPRESSAO or a.endswith(".tmp"):
                continue
            rel = os.path.relpath(os.path.join(raiz, a), pasta)
            h.update(rel.encode())
            with open(os.path.join(raiz, a), "rb") as fh:
                h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def anotar_licao(ficha, peca, regra, texto):
    linha = f"- {agora():%Y-%m-%d} | {uma_linha(peca, 60)} | {uma_linha(regra, 40)} | " \
            f"{uma_linha(texto, 300)} (marca: {ficha.get('marca_id') or '-'})"
    atual = ler_texto(LICOES)
    if linha in atual.splitlines():
        return
    if not atual:
        atual = "# Livro de licoes\n\n"
    elif not atual.endswith("\n"):
        atual += "\n"
    salvar_texto(LICOES, atual + linha + "\n")


# ---------------------------------------------------------------- API do Hermes (marketing)

class ErroApi(Exception):
    pass


def api(metodo, caminho, corpo=None, idem=None, timeout=30):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(API + caminho, data=dados, method=metodo)
    req.add_header("Authorization", f"Bearer {CHAVE}")
    if dados is not None:
        req.add_header("Content-Type", "application/json")
    if idem:
        req.add_header("Idempotency-Key", idem)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            txt = r.read().decode("utf-8", "replace")
            return json.loads(txt) if txt.strip() else {}
    except urllib.error.HTTPError as e:
        raise ErroApi(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}")
    except Exception as e:
        raise ErroApi(f"{type(e).__name__}: {e}")


def pedido_ao_marketing(ficha):
    etapa, v = ficha["etapa"], ficha["versao"]
    pasta = f"/opt/correio/trabalhos/{ficha['id']}"
    return (f"Use a skill processar-ficha.\n"
            f"Ficha: {ficha['id']}\nEtapa: {etapa}\nVersao: {v}\nPasta da ficha: {pasta}/\n"
            f"Entregue em {pasta}/{etapa}-v{v}/ e crie o arquivo vazio 'pronto' por ultimo. "
            f"Se travar, escreva erro.txt na pasta da ficha. "
            f"Na etapa arte, grave tambem post.json no formato de references/formato-entrega.md.")


# ---------------------------------------------------------------- fichas

def listar_fichas():
    try:
        nomes = sorted(os.listdir(TRABALHOS))
    except OSError:
        return []
    saida = []
    for n in nomes:
        f = ler_json(caminho_ficha(n))
        if isinstance(f, dict) and f.get("id") == n:
            saida.append(f)
    return saida


def historico(ficha, texto):
    h = ficha.setdefault("historico", [])
    h.append({"em": agora().isoformat(), "evento": uma_linha(texto, 200)})
    del h[:-40]


def parar(ficha, status, motivo):
    ficha["status"] = status
    ficha["motivo"] = uma_linha(motivo, 400)
    ficha.pop("run", None)
    historico(ficha, f"{status}: {motivo}")
    salvar_ficha(ficha)
    log(f"{ficha['id']}: {status} - {motivo}")


def novo_trabalho(arq):
    id_ = arq[:-5]
    pedido = ler_json(os.path.join(PEDIDOS, arq))
    base = {"id": id_, "criado_em": agora().isoformat(), "historico": []}
    if not ID_RE.match(id_) or not isinstance(pedido, dict) or str(pedido.get("id", id_)) != id_:
        if ID_RE.match(id_):
            base.update({"tema": "(pedido invalido)", "etapa": "pedido", "versao": 0})
            parar(base, "erro", "pedido.json invalido ou com id diferente do nome do arquivo")
        else:
            log(f"pedido ignorado (nome fora do padrao): {arq}")
        return
    tema = uma_linha(pedido.get("tema"), 200)
    pesq = str(pedido.get("pesquisa") or "")
    pasta_pesq = os.path.join(PESQUISAS, pesq)
    ficha = {**base, "tema": tema, "angulo": pedido.get("angulo", ""), "publico": pedido.get("publico", "adultos leigos"),
             "pecas": pedido.get("pecas", []), "pesquisa": pesq, "tema_da_pesquisa": pedido.get("tema_da_pesquisa"),
             "pedidos_do_medico": pedido.get("pedidos_do_medico", ""), "proibido": pedido.get("proibido", []),
             "origem": pedido.get("origem", "medico"), "marca_id": pedido.get("marca_id"),
             "etapa": "conceito", "versao": 1, "rodada": 1, "versoes": {"conceito": 1, "arte": 0},
             "reprovacoes": {"conceito": 0, "arte": 0}, "ajustes": [], "conceito_aprovado": None,
             "status": "conceito_producao"}
    os.makedirs(pasta_trabalho(id_), exist_ok=True)
    if not tema:
        return parar(ficha, "erro", "pedido sem tema")
    campos = [ficha["tema"], str(ficha["angulo"]), str(ficha["pedidos_do_medico"]), json.dumps(ficha["proibido"], ensure_ascii=False)]
    achado = buscar_paciente(campos)
    if achado:
        for k in ("tema", "angulo", "pedidos_do_medico"):      # nao deixa o dado seguir para ficha, avisos nem logs
            ficha[k] = "(oculto)"
        ficha["proibido"] = []
        return parar(ficha, "parado", f"o pedido parece conter dado de paciente ({achado}). Reescreva sem dados pessoais")
    if not pesq or not re.fullmatch(r"[A-Za-z0-9._-]+", pesq) or not os.path.isfile(os.path.join(pasta_pesq, "pesquisa.md")):
        return parar(ficha, "erro", f"pesquisa '{pesq}' nao encontrada em pesquisas/")
    shutil.copy(os.path.join(PEDIDOS, arq), os.path.join(pasta_trabalho(id_), "pedido.json"))
    shutil.copy(os.path.join(pasta_pesq, "pesquisa.md"), os.path.join(pasta_trabalho(id_), "pesquisa.md"))
    ref = os.path.join(pasta_pesq, "referencia-bruta.md")
    if os.path.isfile(ref):
        shutil.copy(ref, os.path.join(pasta_trabalho(id_), "referencia-bruta.md"))
    historico(ficha, "trabalho aberto")
    salvar_ficha(ficha)
    log(f"{id_}: trabalho aberto ({tema})")


def olhar_pedidos():
    try:
        arqs = sorted(a for a in os.listdir(PEDIDOS) if a.endswith(".json"))
    except OSError:
        return
    for a in arqs:
        if not os.path.exists(caminho_ficha(a[:-5])):
            try:
                novo_trabalho(a)
            except Exception as e:
                log(f"erro ao abrir {a}: {type(e).__name__}: {e}")


# ---------------------------------------------------------------- producao (marketing)

def pasta_versao(ficha, etapa=None, v=None):
    return os.path.join(pasta_trabalho(ficha["id"]), f"{etapa or ficha['etapa']}-v{v or ficha['versao']}")


def validar_arte(pasta):
    post = ler_json(os.path.join(pasta, "post.json"))
    if not isinstance(post, dict):
        return "post.json ausente ou invalido"
    redes = [r for r in ("instagram", "linkedin") if post.get(r)]
    if not redes:
        return "post.json sem instagram nem linkedin"
    for r in redes:
        for n in post[r].get("imagens") or []:
            if n != os.path.basename(n) or not os.path.isfile(os.path.join(pasta, n)):
                return f"imagem nao encontrada: {n}"
    return None


def avancar_producao(ficha):
    run = ficha.get("run")
    pasta = pasta_versao(ficha)
    if not run:
        tentativa = ficha.get("tentativa", 1)
        idem = f"{ficha['id']}-{ficha['etapa']}-v{ficha['versao']}-t{tentativa}"
        try:
            r = api("POST", "/v1/runs", {"input": pedido_ao_marketing(ficha),
                                         "session_id": f"ficha-{ficha['id']}-{ficha['etapa']}"}, idem=idem)
        except ErroApi as e:
            n = ficha["erros_api"] = ficha.get("erros_api", 0) + 1
            log(f"{ficha['id']}: nao consegui acordar o marketing ({e})")
            if n >= 20:
                parar(ficha, "erro", f"marketing nao responde pela API ({uma_linha(e, 120)})")
            else:
                salvar_ficha(ficha)
            return
        ficha.pop("erros_api", None)
        ficha["run"] = {"id": r.get("run_id"), "inicio": agora().isoformat(), "tentativa": tentativa}
        historico(ficha, f"marketing acordado ({ficha['etapa']} v{ficha['versao']}, tentativa {tentativa})")
        salvar_ficha(ficha)
        log(f"{ficha['id']}: marketing acordado ({ficha['etapa']} v{ficha['versao']})")
        return
    try:
        st = api("GET", f"/v1/runs/{run['id']}")
    except ErroApi as e:
        log(f"{ficha['id']}: nao consegui ver o run ({e})")
        return
    status = st.get("status")
    inicio = datetime.fromisoformat(run["inicio"])
    if status in ("running", "queued", "started", "pending", None, "unknown"):
        if agora() - inicio > timedelta(minutes=RUN_MAX_MIN):
            try:
                api("POST", f"/v1/runs/{run['id']}/stop", {})
            except ErroApi:
                pass
            return falhou_producao(ficha, f"o marketing passou de {RUN_MAX_MIN} min e foi interrompido")
        return
    # terminou (completed, failed, cancelled, interrupted)
    erro_txt = ler_texto(os.path.join(pasta_trabalho(ficha["id"]), "erro.txt"), 1000).strip()
    if erro_txt:
        os.replace(os.path.join(pasta_trabalho(ficha["id"]), "erro.txt"),
                   os.path.join(pasta_trabalho(ficha["id"]), f"erro-{ficha['etapa']}-v{ficha['versao']}.txt"))
        return parar(ficha, "erro", f"o marketing parou: {erro_txt}")
    if status != "completed" or not os.path.exists(os.path.join(pasta, "pronto")):
        return falhou_producao(ficha, f"run {status}; entrega sem 'pronto'")
    if ficha["etapa"] == "arte":
        problema = validar_arte(pasta)
        if problema:
            return falhou_producao(ficha, f"arte invalida: {problema}")
    achado = buscar_paciente(textos_da_pasta(pasta))
    if achado:
        return parar(ficha, "parado", f"a entrega parece conter dado de paciente ({achado}). Nada foi enviado para revisao")
    pedir_revisao(ficha, pasta)


def falhou_producao(ficha, motivo):
    t = ficha.get("tentativa", 1)
    ficha.pop("run", None)
    if t >= MAX_TENTATIVAS:
        return parar(ficha, "erro", f"{motivo} (apos {t} tentativas)")
    ficha["tentativa"] = t + 1
    historico(ficha, f"falha: {motivo}; tentando de novo")
    salvar_ficha(ficha)
    log(f"{ficha['id']}: {motivo}; nova tentativa")


# ---------------------------------------------------------------- revisao (skip)

def arq_pendente(ficha):
    return os.path.join(pasta_trabalho(ficha["id"]), f"revisao-pendente-{ficha['etapa']}-v{ficha['versao']}.json")


def arq_parecer(ficha):
    return os.path.join(REVISOES, f"{ficha['id']}-{ficha['etapa']}-v{ficha['versao']}.json")


def pedir_revisao(ficha, pasta):
    impr = impressao(pasta)
    salvar_json(arq_pendente(ficha), {
        "id": ficha["id"], "etapa": ficha["etapa"], "versao": ficha["versao"],
        "pasta": os.path.relpath(pasta, CORREIO), "impressao": impr, "marca_id": ficha.get("marca_id"),
        "pesquisa": ficha.get("pesquisa"), "pedido_em": agora().isoformat(),
        "instrucao": "Revise (skill guardiao-publicacao, secao etapas) e grave "
                     f"revisoes/{ficha['id']}-{ficha['etapa']}-v{ficha['versao']}.json copiando esta impressao."})
    ficha.pop("run", None)
    ficha.pop("tentativa", None)
    ficha["status"] = f"{ficha['etapa']}_revisao"
    ficha["revisao_pedida_em"] = agora().isoformat()
    historico(ficha, f"{ficha['etapa']} v{ficha['versao']} entregue; aguardando parecer do skip")
    salvar_ficha(ficha)
    log(f"{ficha['id']}: {ficha['etapa']} v{ficha['versao']} aguardando o skip")


def avancar_revisao(ficha):
    pasta = pasta_versao(ficha)
    pend = ler_json(arq_pendente(ficha), {})
    atual = impressao(pasta)
    if pend.get("impressao") != atual:      # alguem mexeu na pasta: o parecer antigo nao vale
        pedir_revisao(ficha, pasta)
        return
    par = ler_json(arq_parecer(ficha))
    if not isinstance(par, dict) or par.get("impressao") != atual:
        return
    res = par.get("resultado")
    pontos = [p for p in (par.get("pontos") or []) if isinstance(p, dict)]
    if res == "aprovado":
        historico(ficha, f"{ficha['etapa']} v{ficha['versao']} aprovado pelo skip")
        return depois_de_aprovado(ficha)
    if res == "parar":
        quem = "; ".join(uma_linha(p.get("problema"), 120) for p in pontos[:2]) or "o skip pediu para parar"
        return parar(ficha, "parado", f"o skip pediu para parar em {ficha['etapa']} v{ficha['versao']}: {quem}")
    if res != "reprovado":
        return
    e = ficha["etapa"]
    ficha["reprovacoes"][e] = ficha["reprovacoes"].get(e, 0) + 1
    for p in pontos:
        anotar_licao(ficha, p.get("peca", e), p.get("regra", "-"), f"{p.get('problema', '')} -> {p.get('correcao', '')}")
    if ficha["reprovacoes"][e] >= MAX_REPROVACOES:
        gravar_devolutiva(ficha, ficha["versao"] + 1, pontos, par.get("alertas"))
        return parar(ficha, "parado", f"{e} reprovado {ficha['reprovacoes'][e]}x pelo skip. O medico decide (reabrir ou descartar)")
    ficha["versao"] += 1
    ficha["rodada"] = ficha["versao"]
    ficha["versoes"][e] = ficha["versao"]
    gravar_devolutiva(ficha, ficha["versao"], pontos, par.get("alertas"))
    ficha["status"] = f"{e}_producao"
    historico(ficha, f"{e} reprovado; refazendo como v{ficha['versao']}")
    salvar_ficha(ficha)
    log(f"{ficha['id']}: {e} reprovado, vai para v{ficha['versao']}")


def gravar_devolutiva(ficha, v, pontos, alertas):
    linhas = [f"# Devolutiva: {ficha['etapa']} v{v}", "",
              f"A versao anterior foi reprovada na revisao de conformidade. Corrija so o que esta abaixo.", ""]
    for p in pontos:
        linhas.append(f"- **{uma_linha(p.get('peca'), 60)}** ({uma_linha(p.get('regra'), 30)}): "
                      f"{uma_linha(p.get('problema'), 300)}. Correcao: {uma_linha(p.get('correcao'), 300)}")
    for a in (alertas or []):
        linhas.append(f"- Alerta: {uma_linha(a, 300)}")
    salvar_texto(os.path.join(pasta_trabalho(ficha["id"]), f"devolutiva-{ficha['etapa']}-v{v}.md"), "\n".join(linhas) + "\n")


def depois_de_aprovado(ficha):
    if ficha["etapa"] == "conceito":
        ficha["conceito_aprovado"] = f"conceito-v{ficha['versao']}"
        ficha["etapa"] = "arte"
        ficha["versoes"]["arte"] = ficha["versoes"].get("arte", 0) + 1
        ficha["versao"] = ficha["versoes"]["arte"]
        ficha["rodada"] = ficha["versao"]
        ficha["reprovacoes"]["arte"] = 0
        ficha["status"] = "arte_producao"
        salvar_ficha(ficha)
        log(f"{ficha['id']}: conceito aprovado, comeca a arte")
        return
    entregar(ficha)


# ---------------------------------------------------------------- entrega

def entregar(ficha):
    origem = pasta_versao(ficha)
    post = ler_json(os.path.join(origem, "post.json")) or {}
    destino = os.path.join(PRONTOS, ficha["id"])
    if os.path.exists(destino):             # ajuste: guarda a entrega anterior no historico do trabalho
        n = 1
        while os.path.exists(os.path.join(pasta_trabalho(ficha["id"]), f"prontos-anterior-{n}")):
            n += 1
        shutil.move(destino, os.path.join(pasta_trabalho(ficha["id"]), f"prontos-anterior-{n}"))
    os.makedirs(destino)
    post.setdefault("id", ficha["id"])
    if ficha.get("marca_id"):
        post.setdefault("marca_id", ficha["marca_id"])
    if ficha.get("pesquisa"):
        post.setdefault("pesquisa", ficha["pesquisa"])
    nomes = []
    for r in ("instagram", "linkedin"):
        for n in (post.get(r) or {}).get("imagens") or []:
            if n not in nomes:
                nomes.append(n)
    for n in nomes:
        shutil.copy(os.path.join(origem, n), os.path.join(destino, n))
    salvar_json(os.path.join(destino, "post.json"), post)
    salvar_texto(os.path.join(destino, "pronto"), "")      # por ultimo: a expedicao so olha com 'pronto'
    ficha["status"] = "entregue"
    ficha["entregue_em"] = agora().isoformat()
    historico(ficha, "pasta pronta entregue a expedicao (prontos/)")
    salvar_ficha(ficha)
    log(f"{ficha['id']}: entregue em prontos/ (expedicao assume)")


# ---------------------------------------------------------------- ajuste do medico (depois da previa)

def olhar_ajustes():
    try:
        arqs = [a for a in os.listdir(AVISOS) if a.startswith("ajuste-") and a.endswith(".json")]
    except OSError:
        return
    for a in arqs:
        d = ler_json(os.path.join(AVISOS, a))
        id_ = a[len("ajuste-"):-5]
        ficha = ler_json(caminho_ficha(id_))
        if not isinstance(d, dict) or not isinstance(ficha, dict):
            continue
        if ficha.get("ajuste_tratado") == d.get("em"):
            continue
        comentario = uma_linha(d.get("comentario"), 600)
        ficha["ajuste_tratado"] = d.get("em")
        if buscar_paciente([comentario]):
            salvar_ficha(ficha)
            parar(ficha, "parado", "o ajuste parece conter dado de paciente; reescreva sem dados pessoais")
            continue
        ficha.setdefault("ajustes", []).append({"etapa": "arte", "comentario": comentario, "em": d.get("em")})
        anotar_licao(ficha, "ajuste do medico", "AJUSTE", comentario)
        # recomeca pelo conceito: o texto pode ter mudado, entao passa pela revisao de novo
        ficha["versoes"]["conceito"] = ficha["versoes"].get("conceito", 1) + 1
        ficha["etapa"], ficha["versao"] = "conceito", ficha["versoes"]["conceito"]
        ficha["rodada"] = ficha["versao"]
        ficha["reprovacoes"] = {"conceito": 0, "arte": 0}
        ficha["status"] = "conceito_producao"
        ficha.pop("run", None)
        ficha.pop("tentativa", None)
        ficha.pop("motivo", None)
        gravar_devolutiva(ficha, ficha["versao"],
                          [{"peca": "geral", "regra": "AJUSTE DO MEDICO", "problema": comentario,
                            "correcao": "atenda ao pedido dele; ele aprovou o resto"}], None)
        historico(ficha, f"ajuste do medico recebido; conceito v{ficha['versao']}")
        salvar_ficha(ficha)
        log(f"{ficha['id']}: ajuste do medico, recomeca no conceito v{ficha['versao']}")


# ---------------------------------------------------------------- ciclo

def avancar(ficha):
    s = ficha.get("status", "")
    if s in FINAIS or s in PARADOS:
        return
    if s.endswith("_producao"):
        avancar_producao(ficha)
    elif s.endswith("_revisao"):
        avancar_revisao(ficha)


def escrever_status(fichas):
    linhas = ["# Carteiro", f"Atualizado: {agora():%d/%m %H:%M}", "",
              "| Trabalho | Tema | Etapa | Estado | Obs |", "| --- | --- | --- | --- | --- |"]
    for f in sorted(fichas, key=lambda x: x["id"], reverse=True)[:30]:
        obs = f.get("motivo", "") if f.get("status") in PARADOS else ""
        linhas.append(f"| {f['id']} | {uma_linha(f.get('tema'), 50)} | {f.get('etapa')} v{f.get('versao')} | "
                      f"{f.get('status')} | {uma_linha(obs, 120)} |")
    novo = "\n".join(linhas) + "\n"
    antigo = ler_texto(os.path.join(AVISOS, "carteiro.md"))
    if re.sub(r"Atualizado:.*", "", novo) != re.sub(r"Atualizado:.*", "", antigo):
        salvar_texto(os.path.join(AVISOS, "carteiro.md"), novo)


def tick():
    olhar_pedidos()
    olhar_ajustes()
    fichas = listar_fichas()
    for f in fichas:
        try:
            avancar(f)
        except Exception as e:
            log(f"{f['id']}: erro no ciclo: {type(e).__name__}: {e}")
    escrever_status(listar_fichas())


def cmd_loop():
    log(f"carteiro no ar (marketing em {API})")
    if len(CHAVE) < 16:
        log("AVISO: API_SERVER_KEY ausente ou curta; o marketing nao vai aceitar as chamadas")
    while True:
        try:
            tick()
        except Exception as e:
            log(f"erro no ciclo: {type(e).__name__}: {e}")
        time.sleep(TICK)


# ---------------------------------------------------------------- comandos de uso

def cmd_teste():
    print(f"API do marketing: {API}")
    print(f"Chave: {'ok (' + str(len(CHAVE)) + ' caracteres)' if len(CHAVE) >= 16 else 'AUSENTE ou curta'}")
    try:
        print("health:", api("GET", "/health"))
    except ErroApi as e:
        print("health: FALHOU:", e)
        print("-> o marketing esta no ar? A API esta ligada (API_SERVER_ENABLED) e escutando em 0.0.0.0?")
        return 1
    try:
        r = api("POST", "/v1/runs", {"input": "Responda apenas: ok. Nao use nenhuma ferramenta.",
                                     "session_id": "carteiro-teste"}, idem=f"teste-{int(time.time())}")
        rid = r.get("run_id")
        print("run criado:", rid)
        for _ in range(60):
            time.sleep(3)
            st = api("GET", f"/v1/runs/{rid}")
            if st.get("status") not in ("running", "queued", "started", "pending", None):
                print("resultado:", st.get("status"), "|", uma_linha(st.get("output"), 120))
                return 0 if st.get("status") == "completed" else 1
        print("o run nao terminou em 3 min")
        return 1
    except ErroApi as e:
        print("POST /v1/runs FALHOU:", e)
        return 1


def cmd_exemplo():
    id_ = agora().strftime("%Y-%m-%d-%H%M%S")
    pid = "P-exemplo"
    os.makedirs(os.path.join(PESQUISAS, pid), exist_ok=True)
    salvar_texto(os.path.join(PESQUISAS, pid, "pesquisa.md"),
                 "# Pesquisa P-exemplo\nModo: focado\n\n## Temas sugeridos\n1. Hidratacao: o basico\n\n"
                 "## Evidencia por tema\n### 1. Hidratacao\n- Mensagem central: beber agua ao longo do dia ajuda.\n"
                 "- Fontes:\n  - (exemplo, sem fonte real: nao publique)\n")
    salvar_json(os.path.join(PEDIDOS, f"{id_}.json"), {
        "id": id_, "tema": "Hidratacao: o basico (EXEMPLO)", "angulo": "dica simples", "publico": "adultos leigos",
        "pecas": [{"tipo": "carrossel", "rede": "instagram", "slides": 5}], "pesquisa": pid,
        "pedidos_do_medico": "", "proibido": [], "origem": "medico", "criado_em": agora().isoformat()})
    print(f"Pedido de exemplo criado: {id_}. Acompanhe com: carteiro.py status")
    return 0


def cmd_status():
    fichas = listar_fichas()
    if not fichas:
        print("Nenhum trabalho.")
    for f in fichas:
        print(f"{f['id']}  {f.get('etapa')} v{f.get('versao')}  {f.get('status')}  {uma_linha(f.get('tema'), 40)}"
              + (f"\n    -> {f.get('motivo')}" if f.get('status') in PARADOS else ""))
    return 0


def cmd_reabrir():
    if len(sys.argv) < 3:
        print("Use: carteiro.py reabrir <id> [conceito|arte]")
        return 1
    f = ler_json(caminho_ficha(sys.argv[2]))
    if not isinstance(f, dict):
        print("Trabalho nao encontrado.")
        return 1
    if f.get("status") not in PARADOS:
        print(f"O trabalho esta em '{f.get('status')}'; so se reabre 'parado' ou 'erro'.")
        return 1
    etapa = sys.argv[3] if len(sys.argv) > 3 else (f.get("etapa") if f.get("etapa") in ("conceito", "arte") else "conceito")
    if etapa not in ("conceito", "arte"):
        print("Etapa deve ser conceito ou arte.")
        return 1
    if etapa == "arte" and not f.get("conceito_aprovado"):
        print("Ainda nao ha conceito aprovado; use conceito.")
        return 1
    f["etapa"] = etapa
    f["versoes"][etapa] = max(f["versoes"].get(etapa, 0), 0) + 1
    f["versao"] = f["versoes"][etapa]
    f["rodada"] = f["versao"]
    f["reprovacoes"][etapa] = 0
    f["status"] = f"{etapa}_producao"
    for k in ("run", "tentativa", "motivo", "erros_api"):
        f.pop(k, None)
    historico(f, f"reaberto pelo medico em {etapa} v{f['versao']}")
    salvar_ficha(f)
    print(f"Reaberto: {etapa} v{f['versao']}.")
    return 0


def cmd_descartar():
    if len(sys.argv) < 3:
        print("Use: carteiro.py descartar <id>")
        return 1
    f = ler_json(caminho_ficha(sys.argv[2]))
    if not isinstance(f, dict):
        print("Trabalho nao encontrado.")
        return 1
    f["status"] = "descartado"
    f.pop("run", None)
    historico(f, "descartado pelo medico")
    salvar_ficha(f)
    print("Descartado.")
    return 0


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "loop"
    funcoes = {"loop": cmd_loop, "teste": cmd_teste, "exemplo": cmd_exemplo, "status": cmd_status,
               "reabrir": cmd_reabrir, "descartar": cmd_descartar}
    if comando not in funcoes:
        print(__doc__)
        sys.exit(1)
    sys.exit(funcoes[comando]() or 0)
