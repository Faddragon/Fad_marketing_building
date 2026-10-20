#!/usr/bin/env python3
"""coletor - le perfis profissionais do Instagram pela API oficial da Meta (Business Discovery).

Sem IA. Sem login de conta. O token fica so em /segredo. Grava so em /dados.
Uso:
  coletor.py loop      (padrao) espera a hora marcada e coleta todo dia
  coletor.py agora     coleta uma vez, ja
  coletor.py iniciar   le o token curto da entrada padrao e troca pelo de 60 dias
  coletor.py status    mostra o estado (sem mostrar o token)
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

VERSAO_API = os.environ.get("META_API_VERSION", "v26.0")
GRAPH = "https://graph.facebook.com"
SP = timezone(timedelta(hours=-3))  # Sao Paulo (sem horario de verao desde 2019)
DADOS = os.environ.get("DADOS_DIR", "/dados")
SEGREDO = os.environ.get("SEGREDO_DIR", "/segredo")
HORA = os.environ.get("COLETA_HORA", "06:00")
POSTS = int(os.environ.get("POSTS_POR_PERFIL", "25"))
PAUSA = float(os.environ.get("PAUSA_ENTRE_PERFIS", "5"))
RENOVAR_COM_MENOS_DE_DIAS = 20
AVISAR_COM_MENOS_DE_DIAS = 10
CAMPOS_BASE = "caption,media_type,permalink,timestamp,like_count,comments_count"
CAMPOS_EXTRA = CAMPOS_BASE + ",media_product_type,view_count"


class ErroGraph(Exception):
    def __init__(self, codigo, mensagem):
        super().__init__(mensagem)
        self.codigo = codigo
        self.mensagem = mensagem


def log(msg):
    print(f"{datetime.now(SP):%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def graph_get(caminho, params):
    url = f"{GRAPH}/{VERSAO_API}/{caminho}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "predio-coletor/1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            erro = json.loads(e.read().decode("utf-8")).get("error", {})
        except Exception:
            erro = {}
        raise ErroGraph(erro.get("code"), erro.get("message", f"HTTP {e.code}"))
    except Exception as e:  # rede, DNS, tempo esgotado. Nunca inclui a URL (tem o token).
        raise ErroGraph(None, f"falha de rede: {type(e).__name__}")


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


def ler_env():
    env = {}
    caminho = os.path.join(SEGREDO, "instagram.env")
    if not os.path.exists(caminho):
        return env
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def caminho_token():
    return os.path.join(SEGREDO, "token.json")


def ler_token():
    try:
        with open(caminho_token(), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def dias_restantes(info):
    try:
        expira = datetime.fromisoformat(info["expira_em"])
    except Exception:
        return None
    return (expira - datetime.now(SP)).total_seconds() / 86400


def trocar_por_longo(env, token_atual):
    r = graph_get("oauth/access_token", {
        "grant_type": "fb_exchange_token",
        "client_id": env["APP_ID"],
        "client_secret": env["APP_SECRET"],
        "fb_exchange_token": token_atual,
    })
    segundos = int(r.get("expires_in") or 60 * 86400)
    agora = datetime.now(SP)
    return {
        "token": r["access_token"],
        "obtido_em": agora.isoformat(),
        "expira_em": (agora + timedelta(seconds=segundos)).isoformat(),
    }


def cmd_iniciar():
    env = ler_env()
    faltam = [k for k in ("APP_ID", "APP_SECRET", "IG_USER_ID") if not env.get(k)]
    if faltam:
        print("Faltam no instagram.env: " + ", ".join(faltam))
        return 1
    curto = sys.stdin.read().strip()
    if not curto:
        print("Nenhum token recebido.")
        return 1
    try:
        info = trocar_por_longo(env, curto)
        salvar_json(caminho_token(), info)
        r = graph_get(env["IG_USER_ID"], {"fields": "username", "access_token": info["token"]})
    except ErroGraph as e:
        print(f"Falhou: {e.mensagem}")
        return 1
    print(f"Token de longa duracao guardado. Conta: @{r.get('username', '?')}. "
          f"Vence em {dias_restantes(info):.0f} dias.")
    return 0


def ler_perfis_por_dia():
    n = 3
    try:
        with open(os.path.join(DADOS, "config", "instagram.md"), encoding="utf-8") as f:
            m = re.search(r"perfis_por_dia:\s*(\d+)", f.read())
        if m:
            n = int(m.group(1))
    except Exception:
        pass
    return max(1, min(n, 5))


def ler_perfis():
    """Perfis da secao '## Instagram' de config/referencias.md (ignora Removidos)."""
    perfis, dentro = [], False
    try:
        with open(os.path.join(DADOS, "config", "referencias.md"), encoding="utf-8") as f:
            for linha in f:
                if linha.startswith("## "):
                    dentro = linha.strip().lower() == "## instagram"
                    continue
                if dentro:
                    m = re.match(r"^\s*-\s*@([A-Za-z0-9._]{1,30})\b", linha)
                    if m and m.group(1).lower() not in perfis:
                        perfis.append(m.group(1).lower())
    except Exception:
        pass
    return perfis


def arquivo_dados(perfil):
    return os.path.join(DADOS, "referencias", perfil, "dados.json")


def idade_dados(perfil):
    try:
        return os.path.getmtime(arquivo_dados(perfil))
    except OSError:
        return 0.0  # nunca coletado: vai primeiro


def consultar_perfil(ig_id, perfil, token):
    def consulta(campos):
        bd = (f"business_discovery.username({perfil})"
              f"{{followers_count,media_count,media.limit({POSTS}){{{campos}}}}}")
        return graph_get(ig_id, {"fields": bd, "access_token": token})
    try:
        r, campos = consulta(CAMPOS_EXTRA), CAMPOS_EXTRA
    except ErroGraph as e:
        if e.codigo != 100:  # campo nao aceito: tenta so com os basicos
            raise
        r, campos = consulta(CAMPOS_BASE), CAMPOS_BASE
    bd = r.get("business_discovery")
    if not bd:
        raise ErroGraph(None, "resposta sem business_discovery")
    posts = (bd.get("media") or {}).get("data", [])
    return {
        "perfil": perfil,
        "coletado_em": datetime.now(SP).isoformat(),
        "fonte": "meta-business-discovery",
        "campos": campos.split(","),
        "seguidores": bd.get("followers_count"),
        "total_posts": bd.get("media_count"),
        "posts": posts,
    }


def escrever_status(linhas_resultado, token_info, extra_avisos):
    dias = dias_restantes(token_info) if token_info else None
    linhas = [
        "# Coletor do Instagram",
        f"Ultima execucao: {datetime.now(SP):%Y-%m-%d %H:%M} (Sao Paulo)",
        "Token: " + ("nao configurado" if dias is None else f"vence em {dias:.0f} dias"),
        "",
        "## Resultado",
    ] + (linhas_resultado or ["(nenhum perfil na lista)"])
    avisos = list(extra_avisos)
    if dias is not None and dias < AVISAR_COM_MENOS_DE_DIAS:
        avisos.append(f"O token vence em {dias:.0f} dias. Gere um novo (docs do coletor).")
    if avisos:
        linhas += ["", "## Avisos"] + [f"- {a}" for a in avisos]
    salvar_texto(os.path.join(DADOS, "avisos", "coletor.md"), "\n".join(linhas) + "\n")


def rodar_uma_vez():
    env = ler_env()
    info = ler_token()
    avisos, resultado = [], []
    if not env.get("IG_USER_ID") or not info:
        avisos.append("Coletor sem token ou sem IG_USER_ID. Rode a configuracao (README do coletor).")
        escrever_status([], info, avisos)
        log("sem token: nada a coletar")
        return
    dias = dias_restantes(info)
    if dias is not None and dias < RENOVAR_COM_MENOS_DE_DIAS and env.get("APP_ID") and env.get("APP_SECRET"):
        try:
            info = trocar_por_longo(env, info["token"])
            salvar_json(caminho_token(), info)
            log("token renovado")
        except ErroGraph as e:
            avisos.append(f"Nao consegui renovar o token: {e.mensagem}")
    token = info["token"]
    perfis = sorted(ler_perfis(), key=idade_dados)[:ler_perfis_por_dia()]
    for i, perfil in enumerate(perfis):
        if i:
            time.sleep(PAUSA)
        try:
            dados = consultar_perfil(env["IG_USER_ID"], perfil, token)
            salvar_json(arquivo_dados(perfil), dados)
            resultado.append(f"- @{perfil}: ok, {len(dados['posts'])} posts")
            log(f"@{perfil}: ok ({len(dados['posts'])} posts)")
        except ErroGraph as e:
            resultado.append(f"- @{perfil}: erro: {e.mensagem}")
            log(f"@{perfil}: erro {e.codigo}")
            if e.codigo == 190:  # token invalido ou vencido: nao adianta continuar
                avisos.append("Token invalido ou vencido. Gere um novo (README do coletor).")
                break
    escrever_status(resultado, info, avisos)


def proxima_execucao():
    h, m = (int(x) for x in HORA.split(":"))
    agora = datetime.now(SP)
    alvo = agora.replace(hour=h, minute=m, second=0, microsecond=0)
    if alvo <= agora:
        alvo += timedelta(days=1)
    return alvo


def cmd_loop():
    log(f"coletor no ar. Coleta diaria as {HORA} (Sao Paulo).")
    while True:
        alvo = proxima_execucao()
        log(f"proxima coleta: {alvo:%Y-%m-%d %H:%M}")
        while datetime.now(SP) < alvo:
            time.sleep(min(60, max(1, (alvo - datetime.now(SP)).total_seconds())))
        try:
            rodar_uma_vez()
        except Exception as e:  # nunca derruba o loop
            log(f"erro inesperado: {type(e).__name__}")


def cmd_status():
    info = ler_token()
    dias = dias_restantes(info) if info else None
    print("Token:", "nao configurado" if dias is None else f"vence em {dias:.0f} dias")
    print("Perfis na lista:", ", ".join("@" + p for p in ler_perfis()) or "(nenhum)")
    print("Perfis por dia:", ler_perfis_por_dia())
    return 0


if __name__ == "__main__":
    acao = sys.argv[1] if len(sys.argv) > 1 else "loop"
    if acao == "loop":
        cmd_loop()
    elif acao == "agora":
        rodar_uma_vez()
    elif acao == "iniciar":
        sys.exit(cmd_iniciar())
    elif acao == "status":
        sys.exit(cmd_status())
    else:
        print(__doc__)
        sys.exit(2)
