#!/usr/bin/env python3
"""expedicao - leva ao Postiz o que o medico aprovou. Sem IA.

Fluxo (a cada 30 s):
  1. acha pastas novas em prontos/<id>/ (post.json + imagens + arquivo 'pronto')
  2. pede a revisao do skip (LGPD, CFM, evidencia): grava prontos/<id>/revisao-pendente.json
     e espera revisoes/<id>-publicacao.json com a mesma impressao digital do conteudo
  3. so com revisao aprovada manda a previa ao medico no Telegram, com um codigo de 4 digitos
  4. le as decisoes que o skip gravou (decisoes/*.json) e confere o codigo
  5. aprovado: sobe as imagens ao Postiz e agenda cada rede no horario escolhido
     (o Postiz publica; a expedicao nao guarda token de rede social)
  6. depois do horario, confere no Postiz se saiu e avisa no Telegram

Estado de cada trabalho (inclusive o codigo) fica em /segredo/estado/jobs/, onde o skip nao enxerga.
Se o conteudo mudar depois da revisao ou da previa, volta para a revisao.
Pausa: config/publicacao.md com "publicacao: pausada".

Modos (MODO em /segredo/expedicao.env, lido a cada ciclo):
  teste     nao chama o Postiz (so previa, codigo e avisos)
  rascunho  cria rascunho no Postiz, sem agendar
  agendar   agenda de verdade

Uso:
  expedicao.py loop        (padrao)
  expedicao.py configurar  pergunta os dados e grava /segredo/expedicao.env
  expedicao.py teste       confere Postiz, canais e Telegram
  expedicao.py exemplo     cria um post de exemplo em prontos/ (para testar o caminho todo)
  expedicao.py status      mostra o estado dos trabalhos
  expedicao.py reabrir ID  apaga o estado de um trabalho para ele ser recebido de novo
"""
import csv
import getpass
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

TELEGRAM = "https://api.telegram.org"
SP = timezone(timedelta(hours=-3))
CORREIO = os.environ.get("CORREIO_DIR", "/correio")
SEGREDO = os.environ.get("SEGREDO_DIR", "/segredo")
TICK = int(os.environ.get("TICK_SEGUNDOS", "30"))

VALIDADE_CODIGO_H = 72          # a previa vale 3 dias
MIN_ANTECEDENCIA_MIN = 10       # nunca publica na hora
MAX_ANTECEDENCIA_DIAS = 75
CONFERIR_APOS_MIN = 2           # espera isso depois do horario para perguntar ao Postiz
ALERTAR_ATRASO_MIN = 30         # ainda na fila depois disso: avisa
REVISAO_DEMORADA_H = 24         # skip nao revisou: avisa o medico
MAX_LEGENDA = 2200
MAX_HASHTAGS = 30
MAX_IMAGEM_BYTES = 15 * 1024 * 1024
ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

PRONTOS = os.path.join(CORREIO, "prontos")
ENVIADOS = os.path.join(CORREIO, "enviados")
REJEITADOS = os.path.join(CORREIO, "rejeitados")
DECISOES = os.path.join(CORREIO, "decisoes")
REVISOES = os.path.join(CORREIO, "revisoes")
CONFIG = os.path.join(CORREIO, "config")
AVISOS = os.path.join(CORREIO, "avisos")
ESTADO_DIR = os.path.join(SEGREDO, "estado")
JOBS_DIR = os.path.join(ESTADO_DIR, "jobs")
PROCESSADOS = os.path.join(ESTADO_DIR, "decisoes-processadas.json")
CSV_PUBLICACOES = os.path.join(ENVIADOS, "publicacoes.csv")


class ErroPostiz(Exception):
    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


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


def salvar_json(caminho, obj, modo=None):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    if modo:
        os.chmod(tmp, modo)
    os.replace(tmp, caminho)


def salvar_texto(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, caminho)


def parse_dt(s):
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=SP)


def fmt_dt(dt):
    return dt.astimezone(SP).strftime("%d/%m %H:%M")


def caminho_env():
    return os.path.join(SEGREDO, "expedicao.env")


def ler_env():
    env = {}
    try:
        with open(caminho_env(), encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                k, v = linha.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return env


def _seguro(v):
    v = str(v if v is not None else "").replace(";", " ").replace("\r", " ").replace("\n", " ")
    return (" " + v) if v[:1] in ("=", "+", "-", "@") else v


def registrar_csv(id_, rede, evento, agendado="", resultado="", link="", legenda=""):
    novo = not os.path.exists(CSV_PUBLICACOES)
    try:
        os.makedirs(ENVIADOS, exist_ok=True)
        with open(CSV_PUBLICACOES, "a", encoding="utf-8-sig" if novo else "utf-8", newline="") as f:
            w = csv.writer(f, delimiter=";")
            if novo:
                w.writerow(["registrado_em", "id", "rede", "evento", "agendado_para", "resultado", "link", "legenda_inicio"])
            w.writerow([agora().isoformat(timespec="seconds"), _seguro(id_), rede, evento,
                        agendado, _seguro(resultado), link, _seguro((legenda or "")[:80])])
    except OSError as e:
        log(f"nao consegui escrever a planilha: {e}")


# ---------------------------------------------------------------- Postiz

def _postiz_base(env):
    return (env.get("POSTIZ_URL") or "http://postiz:5000").rstrip("/") + "/api/public/v1"


def postiz(env, metodo, caminho, corpo=None, arquivo=None, params=None, timeout=60):
    chave = env.get("POSTIZ_API_KEY")
    if not chave:
        raise ErroPostiz("falta POSTIZ_API_KEY (rode: expedicao.py configurar)")
    url = _postiz_base(env) + caminho
    if params:
        url += "?" + urllib.parse.urlencode(params)
    cab = {"Authorization": chave, "User-Agent": "predio-expedicao/1"}
    dados = None
    if arquivo:
        nome, conteudo, mime = arquivo
        dados, cab["Content-Type"] = _multipart({}, {"file": (nome, conteudo, mime)})
    elif corpo is not None:
        dados = json.dumps(corpo).encode("utf-8")
        cab["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=dados, method=metodo, headers=cab)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            txt = r.read().decode("utf-8") or "null"
            return json.loads(txt)
    except urllib.error.HTTPError as e:
        try:
            detalhe = e.read().decode("utf-8")[:300]
        except Exception:
            detalhe = ""
        raise ErroPostiz(f"Postiz respondeu {e.code}: {detalhe}")
    except Exception as e:  # rede, DNS, tempo esgotado
        raise ErroPostiz(f"falha de rede ao falar com o Postiz: {type(e).__name__}")


def canal_da_rede(env, rede):
    """Acha o id do canal conectado no Postiz. POSTIZ_CANAL_INSTAGRAM / _LINKEDIN forca um id."""
    forcado = env.get(f"POSTIZ_CANAL_{rede.upper()}")
    if forcado:
        return forcado
    lista = postiz(env, "GET", "/integrations")
    certos = [c for c in lista if not c.get("disabled") and str(c.get("identifier", "")).startswith(rede)]
    if not certos:
        raise ErroPostiz(f"nenhum canal de {rede} conectado no Postiz")
    if len(certos) > 1:
        nomes = ", ".join(f"{c.get('name')} ({c.get('id')})" for c in certos)
        raise ErroPostiz(f"mais de um canal de {rede}: {nomes}. Defina POSTIZ_CANAL_{rede.upper()}")
    return certos[0]["id"]


def utc_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def enviar_ao_postiz(env, pasta, post, rede, dt, tipo):
    """Sobe as imagens (ja em JPEG) e cria o post no Postiz. Devolve o id do post."""
    dados = post[rede]
    texto = dados.get("legenda") if rede == "instagram" else dados.get("texto")
    nomes = dados.get("imagens") or []
    canal = canal_da_rede(env, rede)
    imagens = []
    if nomes:
        tmp = os.path.join("/tmp", f"envio-{rede}-{secrets.token_hex(4)}")
        try:
            for arq in preparar_imagens(pasta, nomes, tmp):
                with open(arq, "rb") as f:
                    r = postiz(env, "POST", "/upload", arquivo=(os.path.basename(arq), f.read(), "image/jpeg"))
                if not isinstance(r, dict) or not r.get("id") or not r.get("path"):
                    raise ErroPostiz("o Postiz nao devolveu o id da imagem")
                imagens.append({"id": r["id"], "path": r["path"]})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    settings = ({"__type": "instagram", "post_type": "post"} if rede == "instagram"
                else {"__type": "linkedin", "post_as_images_carousel": False})
    corpo = {"type": tipo, "date": utc_z(dt), "shortLink": False, "tags": [],
             "posts": [{"integration": {"id": canal}, "value": [{"content": texto, "image": imagens}],
                        "settings": settings}]}
    r = postiz(env, "POST", "/posts", corpo=corpo)
    if not isinstance(r, list) or not r or not r[0].get("postId"):
        raise ErroPostiz("o Postiz nao confirmou o post")
    return r[0]["postId"]


def estado_no_postiz(env, post_id, agenda):
    ini, fim = agenda - timedelta(days=2), agenda + timedelta(days=2)
    r = postiz(env, "GET", "/posts", params={"startDate": utc_z(ini), "endDate": utc_z(fim)})
    for p in (r or {}).get("posts", []):
        if p.get("id") == post_id:
            return p.get("state"), p.get("releaseURL")
    return None, None


# ---------------------------------------------------------------- Telegram

def _multipart(campos, arquivos):
    b = uuid.uuid4().hex
    partes = []
    for k, v in campos.items():
        partes.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for nome, (fn, conteudo, mime) in arquivos.items():
        partes.append((f'--{b}\r\nContent-Disposition: form-data; name="{nome}"; filename="{fn}"\r\n'
                       f'Content-Type: {mime}\r\n\r\n').encode() + conteudo + b"\r\n")
    partes.append(f"--{b}--\r\n".encode())
    return b"".join(partes), f"multipart/form-data; boundary={b}"


def tg(env, metodo, campos, arquivos=None):
    token, chat = env.get("TELEGRAM_BOT_TOKEN"), env.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        log("Telegram nao configurado (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)")
        return False
    campos = dict(campos)
    campos["chat_id"] = chat
    url = f"{TELEGRAM}/bot{token}/{metodo}"
    try:
        if arquivos:
            corpo, tipo = _multipart(campos, arquivos)
        else:
            corpo, tipo = urllib.parse.urlencode(campos).encode(), "application/x-www-form-urlencoded"
        req = urllib.request.Request(url, data=corpo, headers={"Content-Type": tipo})
        with urllib.request.urlopen(req, timeout=60) as r:
            return bool(json.loads(r.read().decode()).get("ok"))
    except urllib.error.HTTPError as e:
        try:
            desc = json.loads(e.read().decode()).get("description", "")
        except Exception:
            desc = ""
        log(f"Telegram {metodo}: HTTP {e.code} {desc}")
    except Exception as e:
        log(f"Telegram {metodo}: {type(e).__name__}")  # sem URL: tem o token
    return False


def tg_texto(env, texto):
    ok = True
    while texto:
        pedaco, texto = texto[:3800], texto[3800:]
        ok = tg(env, "sendMessage", {"text": pedaco}) and ok
    return ok


def tg_fotos(env, caminhos):
    caminhos = caminhos[:10]
    try:
        if len(caminhos) == 1:
            with open(caminhos[0], "rb") as f:
                return tg(env, "sendPhoto", {}, {"photo": (os.path.basename(caminhos[0]), f.read(), "image/jpeg")})
        midia, arquivos = [], {}
        for i, c in enumerate(caminhos):
            with open(c, "rb") as f:
                arquivos[f"f{i}"] = (os.path.basename(c), f.read(), "image/jpeg")
            midia.append({"type": "photo", "media": f"attach://f{i}"})
        return tg(env, "sendMediaGroup", {"media": json.dumps(midia)}, arquivos)
    except OSError as e:
        log(f"foto nao enviada: {e}")
        return False


# ---------------------------------------------------------------- imagens

def preparar_imagens(pasta, nomes, destino):
    """Converte para JPEG e ajusta a proporcao para a faixa que o Instagram aceita (4:5 a 1,91:1).
    Nada e cortado: o que sobra vira margem da cor da borda."""
    from PIL import Image
    os.makedirs(destino, exist_ok=True)
    saidas = []
    alvo = None
    for i, nome in enumerate(nomes, 1):
        im = Image.open(os.path.join(pasta, nome)).convert("RGB")
        w, h = im.size
        if alvo is None:
            r = w / h
            if r < 0.8:
                alvo = (int(round(h * 0.8)), h)        # mais estreito que 4:5: alarga com margem
            elif r > 1.91:
                alvo = (w, int(round(w / 1.91)))       # mais largo que 1,91:1: aumenta a altura
            else:
                alvo = (w, h)
            if alvo[0] > 1440:                          # limite de largura da Meta
                f = 1440 / alvo[0]
                alvo = (1440, int(alvo[1] * f))
        tela = Image.new("RGB", alvo, im.getpixel((0, 0)))
        im.thumbnail(alvo)
        tela.paste(im, ((alvo[0] - im.size[0]) // 2, (alvo[1] - im.size[1]) // 2))
        arq = os.path.join(destino, f"slide-{i:02d}.jpg")
        q = 92
        while True:
            tela.save(arq, "JPEG", quality=q, optimize=True)
            if os.path.getsize(arq) <= 7 * 1024 * 1024 or q <= 60:
                break
            q -= 8
        saidas.append(arq)
    return saidas


# ---------------------------------------------------------------- trabalhos

def validar_post(pasta):
    erros = []
    post = ler_json(os.path.join(pasta, "post.json"))
    if not isinstance(post, dict):
        return None, ["post.json ausente ou invalido"]
    ig, lk = post.get("instagram"), post.get("linkedin")
    if not ig and not lk:
        erros.append("post.json sem instagram nem linkedin")
    if ig:
        tipo = ig.get("tipo")
        if tipo not in ("imagem", "carrossel"):
            erros.append(f"Instagram '{tipo}' ainda nao e publicado automaticamente (so imagem e carrossel)")
        imgs = ig.get("imagens") or []
        if not imgs or len(imgs) > 10:
            erros.append("Instagram precisa de 1 a 10 imagens")
        for n in imgs:
            if n != os.path.basename(n) or not n.lower().endswith((".png", ".jpg", ".jpeg")):
                erros.append(f"imagem invalida: {n}")
            elif not os.path.isfile(os.path.join(pasta, n)):
                erros.append(f"imagem nao encontrada: {n}")
            elif os.path.getsize(os.path.join(pasta, n)) > MAX_IMAGEM_BYTES:
                erros.append(f"imagem grande demais: {n}")
        leg = ig.get("legenda", "")
        if not isinstance(leg, str) or not leg.strip():
            erros.append("legenda vazia")
        elif len(leg) > MAX_LEGENDA:
            erros.append(f"legenda com {len(leg)} caracteres (maximo {MAX_LEGENDA})")
        elif len(re.findall(r"#\w", leg)) > MAX_HASHTAGS:
            erros.append(f"mais de {MAX_HASHTAGS} hashtags")
    if lk:
        if not isinstance(lk.get("texto", ""), str) or not lk.get("texto", "").strip():
            erros.append("texto do LinkedIn vazio")
        for n in lk.get("imagens") or []:
            if n != os.path.basename(n) or not os.path.isfile(os.path.join(pasta, n)):
                erros.append(f"imagem do LinkedIn nao encontrada: {n}")
    return post, erros


def codigo_novo(jobs):
    usados = {j.get("codigo") for _, j in jobs}
    while True:
        c = f"{secrets.randbelow(10000):04d}"
        if c not in usados:
            return c


def arq_estado(id_):
    return os.path.join(JOBS_DIR, f"{id_}.json")


def salvar_estado(job):
    salvar_json(arq_estado(job["id"]), job, 0o600)


def listar_jobs():
    """(pasta em prontos/, estado). Estado concluido ja saiu de prontos/ e nao aparece."""
    jobs = []
    try:
        nomes = sorted(f[:-5] for f in os.listdir(JOBS_DIR) if f.endswith(".json"))
    except OSError:
        return jobs
    for nome in nomes:
        pasta = os.path.join(PRONTOS, nome)
        j = ler_json(arq_estado(nome))
        if ID_RE.match(nome) and os.path.isdir(pasta) and isinstance(j, dict):
            jobs.append((pasta, j))
    return jobs


def impressao(pasta, post):
    """Impressao digital do conteudo (post.json + imagens citadas). Muda se qualquer coisa mudar."""
    h = hashlib.sha256()
    nomes = ["post.json"] + [n for r in ("instagram", "linkedin") for n in ((post.get(r) or {}).get("imagens") or [])]
    for n in nomes:
        with open(os.path.join(pasta, n), "rb") as f:
            h.update(hashlib.sha256(f.read()).digest())
    return h.hexdigest()


def publicacao_pausada():
    try:
        with open(os.path.join(CONFIG, "publicacao.md"), encoding="utf-8") as f:
            return re.search(r"^\s*publicacao:\s*pausada\b", f.read(), re.M | re.I) is not None
    except OSError:
        return False


def pedir_revisao(pasta, job, post):
    job["impressao"] = impressao(pasta, post)
    job["status"], job["codigo"] = "aguardando_revisao", None
    job["revisao_pedida_em"] = agora().isoformat()
    job.pop("revisao_demorada_avisada", None)
    salvar_estado(job)
    salvar_json(os.path.join(pasta, "revisao-pendente.json"), {
        "id": job["id"], "etapa": "publicacao", "impressao": job["impressao"],
        "pedido_em": job["revisao_pedida_em"],
        "instrucao": "Revise (skill guardiao-publicacao) e grave revisoes/<id>-publicacao.json copiando esta impressao."})


def mandar_previa(env, pasta, job, post, motivo=""):
    ig, lk = post.get("instagram"), post.get("linkedin")
    linhas = [f"{motivo}Prévia {job['id']}  |  código {job['codigo']}"]
    if ig:
        linhas.append(f"\nINSTAGRAM ({ig['tipo']}, {len(ig['imagens'])} imagem(ns)). Legenda:\n{ig['legenda']}")
    if lk:
        linhas.append(f"\nLINKEDIN. Texto:\n{lk['texto']}")
    if job.get("alertas"):
        linhas.append("\nALERTAS DO REVISOR (não bloqueiam, mas olhe):\n- " + "\n- ".join(job["alertas"]))
    linhas.append(f"\nPara aprovar, escreva ao skip: ok {job['codigo']} insta hoje 19h"
                  f"\nPara ajustar: ajustar {job['codigo']}: o que mudar"
                  f"\nPara descartar: descartar {job['codigo']}"
                  f"\n(vale até {fmt_dt(parse_dt(job['valida_ate']))})")
    if ig:
        tmp = os.path.join("/tmp", f"previa-{job['id']}")
        try:
            fotos = preparar_imagens(pasta, ig["imagens"], tmp)
            tg_fotos(env, fotos)
        except Exception as e:
            log(f"previa sem imagens: {type(e).__name__}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    tg_texto(env, "\n".join(linhas))


def receber_novos(env):
    if publicacao_pausada():
        return
    try:
        nomes = sorted(os.listdir(PRONTOS))
    except OSError:
        return
    for nome in nomes:
        pasta = os.path.join(PRONTOS, nome)
        if not ID_RE.match(nome) or not os.path.isdir(pasta):
            continue
        if not os.path.exists(os.path.join(pasta, "pronto")):
            continue
        if os.path.exists(arq_estado(nome)):
            # ajuste pedido pelo medico: o carteiro refaz e entrega a pasta de novo (pronto mais novo que o pedido)
            job = ler_json(arq_estado(nome), {})
            try:
                nova = job.get("status") == "ajuste_pedido" and os.path.getmtime(os.path.join(pasta, "pronto")) > \
                    parse_dt(job["ajuste_em"]).timestamp()
            except Exception:
                nova = False
            if not nova:
                continue
            post, erros = validar_post(pasta)
            if erros:
                job["status"], job["erros"] = "invalido", erros
                salvar_estado(job)
                tg_texto(env, f"⚠️ A versão ajustada de {nome} não pode ser publicada:\n- " + "\n- ".join(erros))
                continue
            pedir_revisao(pasta, job, post)
            tg_texto(env, f"📥 Versão ajustada de {nome} recebida. Aguardando de novo a revisão de conformidade do skip.")
            log(f"recebida versao ajustada de {nome}")
            continue
        post, erros = validar_post(pasta)
        if erros:
            salvar_estado({"id": nome, "status": "invalido", "erros": erros})
            tg_texto(env, f"⚠️ {nome} não pode ser publicado:\n- " + "\n- ".join(erros) +
                     "\n\nCorrija a pasta e rode: docker exec predio-expedicao python /app/expedicao.py reabrir " + nome)
            registrar_csv(nome, "-", "invalido", resultado="; ".join(erros))
            continue
        pedir_revisao(pasta, {"id": nome}, post)
        tg_texto(env, f"📥 {nome} recebido. Aguardando a revisão de conformidade (LGPD e CFM) do skip.")
        log(f"recebido {nome}: aguardando revisao")


def ler_revisao(id_, impr):
    rev = ler_json(os.path.join(REVISOES, f"{id_}-publicacao.json"))
    if not isinstance(rev, dict) or rev.get("impressao") != impr:
        return None
    if rev.get("resultado") not in ("aprovado", "reprovado", "parar"):
        return None
    return rev


def _txt(x, n=300):
    return str(x if x is not None else "").replace("\n", " ").strip()[:n]


def _ponto(p):
    if isinstance(p, dict):
        return " | ".join(_txt(p.get(k), 200) for k in ("peca", "regra", "problema", "correcao") if p.get(k))
    return _txt(p)


def aguardar_revisoes(env):
    t = agora()
    for pasta, job in listar_jobs():
        st = job.get("status")
        if st not in ("aguardando_revisao", "revisao_reprovada"):
            continue
        post, erros = validar_post(pasta)
        if erros:
            job["status"], job["erros"] = "invalido", erros
            salvar_estado(job)
            tg_texto(env, f"⚠️ {job['id']} mudou e ficou inválido: " + "; ".join(erros))
            continue
        if impressao(pasta, post) != job.get("impressao"):  # o conteudo mudou: nova revisao
            pedir_revisao(pasta, job, post)
            if st == "revisao_reprovada":
                tg_texto(env, f"♻️ {job['id']} foi alterado depois da reprovação. Pedi nova revisão ao skip.")
            continue
        if st == "revisao_reprovada":
            continue
        rev = ler_revisao(job["id"], job["impressao"])
        if not rev:
            if (t - parse_dt(job["revisao_pedida_em"]) > timedelta(hours=REVISAO_DEMORADA_H)
                    and not job.get("revisao_demorada_avisada")):
                job["revisao_demorada_avisada"] = True
                salvar_estado(job)
                tg_texto(env, f"⏳ {job['id']} espera a revisão do skip há mais de {REVISAO_DEMORADA_H} h. "
                              "Peça a ele: revisa os prontos.")
            continue
        if rev["resultado"] != "aprovado":
            job["status"] = "revisao_reprovada"
            salvar_estado(job)
            pontos = [_ponto(p) for p in (rev.get("pontos") or [])][:8]
            tg_texto(env, f"🚫 O skip {'reprovou' if rev['resultado'] == 'reprovado' else 'parou'} {job['id']}:\n- "
                          + "\n- ".join(pontos or ["(sem detalhes)"])
                          + "\n\nNada foi enviado. Corrija a pasta e a revisão roda de novo sozinha.")
            registrar_csv(job["id"], "-", "revisao_" + rev["resultado"], resultado="; ".join(pontos))
            continue
        t0 = agora()
        job.update({"status": "aguardando_aprovacao", "codigo": codigo_novo(listar_jobs()), "previa_em": t0.isoformat(),
                    "valida_ate": (t0 + timedelta(hours=VALIDADE_CODIGO_H)).isoformat(), "redes": {},
                    "alertas": [_txt(a) for a in (rev.get("alertas") or [])][:8]})
        salvar_estado(job)
        mandar_previa(env, pasta, job, post)
        log(f"revisao aprovada e previa enviada: {job['id']}")


def horario_padrao(env, rede):
    hhmm = env.get(f"HORARIO_PADRAO_{rede.upper()}") or ("19:00" if rede == "instagram" else "08:00")
    try:
        h, m = [int(x) for x in hhmm.split(":")]
    except Exception:
        h, m = (19, 0) if rede == "instagram" else (8, 0)
    t = agora()
    dt = t.replace(hour=h, minute=m, second=0, microsecond=0)
    while dt < t + timedelta(minutes=30):
        dt += timedelta(days=1)
    return dt


def mover(pasta, base, id_):
    os.makedirs(base, exist_ok=True)
    destino = os.path.join(base, id_)
    if os.path.exists(destino):
        destino += agora().strftime("-%Y%m%d%H%M%S")
    shutil.move(pasta, destino)
    return destino


def processar_decisoes(env):
    proc = ler_json(PROCESSADOS, [])
    try:
        arquivos = sorted(f for f in os.listdir(DECISOES) if f.endswith(".json"))
    except OSError:
        return
    novos = [f for f in arquivos if f not in proc]
    for fn in novos:
        proc.append(fn)
        d = ler_json(os.path.join(DECISOES, fn))
        if not isinstance(d, dict):
            continue
        codigo, acao = str(d.get("codigo", "")), d.get("acao")
        alvo = None
        for pasta, j in listar_jobs():
            if j.get("status") == "aguardando_aprovacao" and j.get("codigo") == codigo:
                alvo = (pasta, j)
        if not alvo or not re.fullmatch(r"\d{4}", codigo):
            tg_texto(env, f"Código {codigo or '?'} não confere com nenhuma prévia aberta. Copie o código da mensagem da prévia.")
            continue
        pasta, job = alvo
        try:
            if parse_dt(d["recebido_em"]) < parse_dt(job["previa_em"]) - timedelta(seconds=60):
                tg_texto(env, f"A decisão do código {codigo} é anterior à prévia. Escreva de novo.")
                continue
        except Exception:
            tg_texto(env, f"Decisão do código {codigo} sem data válida. Escreva de novo.")
            continue
        post, _ = validar_post(pasta)
        if acao == "descartar":
            mover(pasta, REJEITADOS, job["id"])
            registrar_csv(job["id"], "-", "descartado")
            tg_texto(env, f"Descartado: {job['id']}.")
        elif acao == "ajustar":
            salvar_json(os.path.join(AVISOS, f"ajuste-{job['id']}.json"), {
                "id": job["id"], "comentario": d.get("comentario", ""),
                "texto_original": d.get("texto_original", ""), "em": agora().isoformat()})
            job["status"], job["codigo"], job["ajuste_em"] = "ajuste_pedido", None, agora().isoformat()
            salvar_estado(job)
            registrar_csv(job["id"], "-", "ajuste_pedido", resultado=d.get("comentario", ""))
            tg_texto(env, f"Ajuste de {job['id']} registrado em avisos/. Quem leva ao marketing é o carteiro.")
        elif acao == "aprovar":
            aprovar(env, pasta, job, post, d)
    salvar_json(PROCESSADOS, proc[-2000:], 0o600)


def aprovar(env, pasta, job, post, d):
    if publicacao_pausada():
        tg_texto(env, "As publicações estão pausadas. Diga ao skip: retoma as publicações, e mande a aprovação de novo "
                      f"(ok {job['codigo']} ...).")
        return
    if impressao(pasta, post) != job.get("impressao"):
        pedir_revisao(pasta, job, post)
        tg_texto(env, f"⚠️ O conteúdo de {job['id']} mudou depois da prévia. Voltou para a revisão do skip; "
                      "você receberá uma nova prévia e um novo código.")
        return
    quer = d.get("redes") or [r for r in ("instagram", "linkedin") if post.get(r)]
    horarios, planos = d.get("horarios") or {}, {}
    for rede in quer:
        if rede not in ("instagram", "linkedin") or not post.get(rede):
            continue
        try:
            dt = parse_dt(horarios[rede]) if horarios.get(rede) else horario_padrao(env, rede)
        except Exception:
            tg_texto(env, f"Não entendi o horário de {rede}. Escreva de novo, por exemplo: ok {job['codigo']} insta hoje 19h")
            return
        t = agora()
        if dt < t + timedelta(minutes=MIN_ANTECEDENCIA_MIN) or dt > t + timedelta(days=MAX_ANTECEDENCIA_DIAS):
            tg_texto(env, f"O horário de {rede} ({fmt_dt(dt)}) já passou, é em menos de {MIN_ANTECEDENCIA_MIN} min "
                          f"ou está longe demais. Mande outro: ok {job['codigo']} insta hoje 19h")
            return
        planos[rede] = dt
    if not planos:
        tg_texto(env, "Nenhuma rede para publicar nessa aprovação.")
        return
    modo = env.get("MODO", "teste")
    redes, resumo = {}, []
    for rede, dt in planos.items():
        nome = "Instagram" if rede == "instagram" else "LinkedIn"
        try:
            if modo == "teste":
                pid, st = None, "simulado"
            else:
                pid = enviar_ao_postiz(env, pasta, post, rede, dt, "schedule" if modo == "agendar" else "draft")
                st = "agendado" if modo == "agendar" else "rascunho"
        except ErroPostiz as e:
            tg_texto(env, f"❌ Não consegui levar o {nome} ao Postiz: {e.mensagem}\n"
                          f"Nada ficou agendado em {nome}. Escreva de novo: ok {job['codigo']} insta hoje 19h")
            for r in redes.values():  # o que ja foi criado nesta rodada fica registrado para conferir no Postiz
                r["aviso"] = "criado antes de outra rede falhar"
            if redes:
                job["redes"] = redes
                salvar_estado(job)
            return
        redes[rede] = {"agenda": dt.isoformat(), "status": st, "postiz_id": pid}
        resumo.append(f"{nome} {fmt_dt(dt)}")
    final = all(r["status"] != "agendado" for r in redes.values())
    job.update({"status": "concluido" if final else "agendado", "redes": redes, "codigo_usado": job["codigo"],
                "codigo": None, "aprovado_em": agora().isoformat()})
    salvar_estado(job)
    etiqueta = {"teste": "\n(modo TESTE: nada foi enviado ao Postiz)",
                "rascunho": "\n(modo RASCUNHO: criado no Postiz sem agendar; abra o calendário para conferir)",
                "agendar": "\nO Postiz publica no horário. Eu aviso quando sair."}[modo if modo in ("teste", "rascunho") else "agendar"]
    tg_texto(env, f"✅ {job['id']}: " + "; ".join(resumo) + etiqueta)
    for rede, r in redes.items():
        registrar_csv(job["id"], rede, r["status"], agendado=r["agenda"],
                      legenda=(post[rede].get("legenda") or post[rede].get("texto") or ""))
    if final:
        mover(pasta, ENVIADOS, job["id"])


def conferir_publicacoes(env):
    t = agora()
    for pasta, job in listar_jobs():
        st = job.get("status")
        if st == "aguardando_aprovacao" and t > parse_dt(job["valida_ate"]):
            job["status"], job["codigo"] = "expirado", None
            salvar_estado(job)
            registrar_csv(job["id"], "-", "expirado")
            tg_texto(env, f"A prévia {job['id']} expirou sem decisão. Para receber de novo: docker exec predio-expedicao python /app/expedicao.py reabrir {job['id']}")
            continue
        if st != "agendado":
            continue
        mudou = False
        for rede, r in job["redes"].items():
            if r["status"] != "agendado":
                continue
            agenda = parse_dt(r["agenda"])
            if t < agenda + timedelta(minutes=CONFERIR_APOS_MIN):
                continue
            if r.get("verificado_em") and t < parse_dt(r["verificado_em"]) + timedelta(minutes=2):
                continue
            r["verificado_em"] = t.isoformat()
            mudou = True
            try:
                estado, link = estado_no_postiz(env, r["postiz_id"], agenda)
            except ErroPostiz as e:
                log(f"{job['id']}: nao consegui conferir no Postiz ({e.mensagem})")
                continue
            nome = "Instagram" if rede == "instagram" else "LinkedIn"
            if estado == "PUBLISHED":
                r["status"], r["link"] = "publicado", link or ""
                tg_texto(env, f"✅ Publicado no {nome}: {link or '(sem link)'}")
                registrar_csv(job["id"], rede, "publicado", agendado=r["agenda"], link=link or "")
            elif estado == "ERROR":
                r["status"] = "erro"
                tg_texto(env, f"❌ O Postiz não conseguiu publicar {job['id']} no {nome}. Abra o Postiz para ver o motivo e tentar de novo.")
                registrar_csv(job["id"], rede, "erro", agendado=r["agenda"], resultado="erro no Postiz")
            elif t > agenda + timedelta(minutes=ALERTAR_ATRASO_MIN) and not r.get("alertado"):
                r["alertado"] = True
                tg_texto(env, f"⚠️ {job['id']} ({nome}) ainda não saiu, {ALERTAR_ATRASO_MIN} min depois do horário "
                              f"(estado no Postiz: {estado or 'não encontrado'}). Confira o Postiz.")
        if all(r["status"] != "agendado" for r in job["redes"].values()):
            job["status"] = "concluido"
            salvar_estado(job)
            mover(pasta, ENVIADOS, job["id"])
        elif mudou:
            salvar_estado(job)


# ---------------------------------------------------------------- manutencao

def escrever_status():
    linhas = [f"# Expedição - {agora():%Y-%m-%d %H:%M}", "", "| trabalho | estado | detalhe |", "| --- | --- | --- |"]
    for _, j in listar_jobs():
        det = "; ".join(f"{k}: {v['status']} {fmt_dt(parse_dt(v['agenda']))}" for k, v in (j.get("redes") or {}).items())
        linhas.append(f"| {j['id']} | {j.get('status')} | {det or '-'} |")
    if len(linhas) == 4:
        linhas.append("| (nada na fila) | | |")
    try:
        salvar_texto(os.path.join(AVISOS, "expedicao.md"), "\n".join(linhas) + "\n")
    except OSError:
        pass


def tick(estado):
    env = ler_env()
    receber_novos(env)
    aguardar_revisoes(env)
    processar_decisoes(env)
    conferir_publicacoes(env)
    escrever_status()


def cmd_loop():
    log(f"expedicao no ar (modo {ler_env().get('MODO', 'teste')})")
    estado = {}
    while True:
        try:
            tick(estado)
        except Exception as e:  # nunca morre por um erro de um trabalho
            log(f"erro no ciclo: {type(e).__name__}: {e}")
        time.sleep(TICK)


# ---------------------------------------------------------------- comandos de uso

CAMPOS = [("POSTIZ_URL", "Endereço interno do Postiz (Enter = http://postiz:5000)", False),
          ("POSTIZ_API_KEY", "Chave da API pública do Postiz", True),
          ("TELEGRAM_BOT_TOKEN", "Token do bot do Telegram", True),
          ("TELEGRAM_CHAT_ID", "Seu ID no Telegram", False),
          ("MODO", "Modo (teste, rascunho ou agendar)", False)]


def cmd_configurar():
    env = ler_env()
    print("Enter mantém o valor atual. Campos secretos não aparecem na tela.")
    for k, rotulo, secreto in CAMPOS:
        atual = env.get(k, "")
        mostra = "(já tem)" if (atual and secreto) else (f"[{atual}]" if atual else "")
        pergunta = f"{rotulo} {mostra}: "
        v = (getpass.getpass(pergunta) if secreto else input(pergunta)).strip()
        if v:
            env[k] = v
    env.setdefault("POSTIZ_URL", "http://postiz:5000")
    env.setdefault("MODO", "teste")
    if env["MODO"] not in ("teste", "rascunho", "agendar"):
        print("MODO precisa ser teste, rascunho ou agendar. Gravei teste.")
        env["MODO"] = "teste"
    corpo = "# gerado por expedicao.py configurar. Nao compartilhe.\n" + "".join(f"{k}={v}\n" for k, v in env.items())
    os.makedirs(SEGREDO, exist_ok=True)
    fd = os.open(caminho_env(), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(corpo)
    print("Gravado. Próximo: expedicao.py teste")
    return 0


def cmd_teste():
    env = ler_env()
    ok = True
    for k in ("POSTIZ_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        if not env.get(k):
            print(f"[falta] {k}")
            ok = False
    if env.get("POSTIZ_API_KEY"):
        try:
            canais = postiz(env, "GET", "/integrations")
            if not canais:
                print("postiz: responde, mas nenhum canal conectado ainda")
                ok = False
            for c in canais:
                print(f"canal: {c.get('identifier')} - {c.get('name')} ({c.get('id')})"
                      + (" [DESLIGADO]" if c.get("disabled") else ""))
            for rede in ("instagram", "linkedin"):
                try:
                    canal_da_rede(env, rede)
                except ErroPostiz as e:
                    print(f"[atenção] {e.mensagem}")
                    ok = False
        except ErroPostiz as e:
            print(f"[erro] postiz: {e.mensagem}")
            ok = False
    if env.get("TELEGRAM_BOT_TOKEN"):
        print("telegram:", "mensagem enviada" if tg_texto(env, "🧪 Teste da expedição: o Telegram está funcionando.")
              else "[erro] não enviou")
    print(f"modo: {env.get('MODO', 'teste')}")
    return 0 if ok else 1


def cmd_exemplo():
    from PIL import Image, ImageDraw, ImageFont
    id_ = "exemplo-" + agora().strftime("%Y%m%d-%H%M")
    pasta = os.path.join(PRONTOS, id_)
    os.makedirs(pasta, exist_ok=True)
    cores = [(24, 62, 99), (46, 125, 110), (160, 82, 45)]
    nomes = []
    for i, c in enumerate(cores, 1):
        im = Image.new("RGB", (1080, 1440), c)
        d = ImageDraw.Draw(im)
        try:
            fonte = ImageFont.load_default(size=72)
        except TypeError:
            fonte = ImageFont.load_default()
        d.text((90, 600), f"Teste {i}/3", fill="white", font=fonte)
        n = f"slide-{i:02d}.png"
        im.save(os.path.join(pasta, n))
        nomes.append(n)
    salvar_json(os.path.join(pasta, "post.json"), {
        "id": id_,
        "instagram": {"tipo": "carrossel", "legenda": "Teste da expedição. Pode apagar este post.", "imagens": nomes},
        "linkedin": {"tipo": "imagem", "texto": "Teste da expedição no LinkedIn. Pode ignorar.", "imagens": [nomes[0]]},
    })
    open(os.path.join(pasta, "pronto"), "w").close()
    print(f"Criado {pasta}. Peça ao skip: revisa os prontos. Depois da revisão aprovada a prévia chega no Telegram.")
    return 0


def cmd_reabrir():
    if len(sys.argv) < 3 or not ID_RE.match(sys.argv[2]):
        print("Use: expedicao.py reabrir <id>")
        return 1
    try:
        os.remove(arq_estado(sys.argv[2]))
        print("Estado apagado. A pasta será recebida de novo em até 30 segundos.")
        return 0
    except OSError:
        print("Esse trabalho não tem estado guardado.")
        return 1


def cmd_status():
    for _, j in listar_jobs():
        print(j["id"], j.get("status"), {k: v["status"] for k, v in (j.get("redes") or {}).items()})
    return 0


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "loop"
    if comando == "loop":
        cmd_loop()
    else:
        funcoes = {"configurar": cmd_configurar, "teste": cmd_teste,
                   "exemplo": cmd_exemplo, "status": cmd_status, "reabrir": cmd_reabrir}
        f = funcoes.get(comando)
        if not f:
            print(__doc__)
            sys.exit(2)
        sys.exit(f())
