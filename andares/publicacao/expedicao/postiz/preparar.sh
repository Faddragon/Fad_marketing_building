#!/usr/bin/env bash
# Prepara o Postiz do andar de publicação: cria as senhas e o endereço público em segredos/postiz/.
# Chamado pelo painel:
#   ./predio postiz-preparar postiz.SEUDOMINIO.com.br   (uma vez, antes de subir a publicação)
#   ./predio postiz-fechar                              (depois de criar a sua conta no Postiz)
# Nada daqui vai para o GitHub: os arquivos ficam em /opt/predio-dados/segredos/postiz/.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PREDIO_DADOS="${PREDIO_DADOS:-/opt/predio-dados}"
DIR="$PREDIO_DADOS/segredos/postiz"
COMPOSE="$RAIZ/andares/publicacao/compose.yml"

erro() { echo "ERRO: $*" >&2; exit 1; }
sorteio() { openssl rand -hex "$1"; }   # só letras e números: não quebra a URL do banco

fechar_cadastro() {
  [[ -f "$DIR/postiz.env" ]] || erro "o Postiz ainda não foi preparado. Rode: ./predio postiz-preparar postiz.SEUDOMINIO.com.br"
  if grep -q '^DISABLE_REGISTRATION=' "$DIR/postiz.env"; then
    sed -i 's/^DISABLE_REGISTRATION=.*/DISABLE_REGISTRATION=true/' "$DIR/postiz.env"
  else
    echo 'DISABLE_REGISTRATION=true' >> "$DIR/postiz.env"
  fi
  echo "Cadastro fechado no arquivo. Recriando o Postiz para valer..."
  docker compose -p predio-publicacao -f "$COMPOSE" up -d --no-deps --force-recreate postiz
  echo "Pronto: ninguém mais consegue criar conta nova no Postiz."
}

if [[ "${1:-}" == "--fechar-cadastro" ]]; then
  fechar_cadastro
  exit 0
fi

DOMINIO="${1:-}"
[[ -n "$DOMINIO" ]] || erro "use: ./predio postiz-preparar postiz.SEUDOMINIO.com.br  (o endereço público que você vai abrir no Cloudflare)"
DOMINIO="${DOMINIO#https://}"; DOMINIO="${DOMINIO#http://}"; DOMINIO="${DOMINIO%%/*}"
[[ "$DOMINIO" =~ ^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,}$ ]] || erro "endereço inválido: '$DOMINIO'. Exemplo: postiz.drfranciscodias.com.br"
command -v openssl >/dev/null || erro "openssl não encontrado (apt install openssl)"

if [[ -f "$DIR/postiz.env" ]]; then
  echo "O Postiz já foi preparado ($DIR/postiz.env). Nada foi alterado."
  echo "Para mudar o endereço ou as chaves das redes: nano $DIR/postiz.env  e depois  ./predio reconstruir publicacao"
  exit 0
fi

mkdir -p "$DIR"; chmod 700 "$DIR"

echo "Chaves das redes (pode deixar em branco e preencher depois no arquivo; nada aparece na tela)."
echo "Instagram pela Página do Facebook: ID e segredo do app Meta (Configurações > Básico)."
read -rsp "  FACEBOOK_APP_ID (Meta): " FB_ID; echo
read -rsp "  FACEBOOK_APP_SECRET (Meta): " FB_SECRET; echo
echo "LinkedIn (o app precisa estar aprovado; pode deixar em branco por enquanto)."
read -rsp "  LINKEDIN_CLIENT_ID: " LI_ID; echo
read -rsp "  LINKEDIN_CLIENT_SECRET: " LI_SECRET; echo

PG_SENHA="$(sorteio 24)"
TEMPORAL_SENHA="$(sorteio 24)"
JWT="$(sorteio 48)"

( umask 077
  cat > "$DIR/postgres.env" <<EOF
POSTGRES_USER=postiz-user
POSTGRES_PASSWORD=$PG_SENHA
POSTGRES_DB=postiz-db-local
EOF
  cat > "$DIR/temporal-db.env" <<EOF
POSTGRES_USER=temporal
POSTGRES_PASSWORD=$TEMPORAL_SENHA
POSTGRES_PWD=$TEMPORAL_SENHA
EOF
  cat > "$DIR/postiz.env" <<EOF
# Gerado por ./predio postiz-preparar em $(date +%F). Não compartilhe. Para mudar algo: edite e rode ./predio reconstruir publicacao
MAIN_URL=https://$DOMINIO
FRONTEND_URL=https://$DOMINIO
NEXT_PUBLIC_BACKEND_URL=https://$DOMINIO/api
JWT_SECRET=$JWT
DATABASE_URL=postgresql://postiz-user:$PG_SENHA@postiz-postgres:5432/postiz-db-local
# Depois de criar a sua conta no Postiz, rode ./predio postiz-fechar (vira true).
DISABLE_REGISTRATION=false
FACEBOOK_APP_ID=$FB_ID
FACEBOOK_APP_SECRET=$FB_SECRET
LINKEDIN_CLIENT_ID=$LI_ID
LINKEDIN_CLIENT_SECRET=$LI_SECRET
EOF
)
chmod 600 "$DIR/postgres.env" "$DIR/temporal-db.env" "$DIR/postiz.env"

cat <<TXT

Pronto. Arquivos criados em $DIR (só o dono lê).

Próximos passos:
  1. ./predio subir publicacao                 (a primeira subida demora alguns minutos: baixa as imagens)
  2. No Cloudflare, aponte https://$DOMINIO para http://localhost:4007 desta VPS
     (túnel cloudflared é o jeito mais simples e não mexe no outro site). Veja andares/publicacao/README.md.
  3. Abra https://$DOMINIO, crie a sua conta e rode ./predio postiz-fechar
  4. No Meta for Developers, cadastre o redirecionamento:
     https://$DOMINIO/integrations/social/instagram
  5. No Postiz, em Canais, conecte o Instagram. Depois gere a chave da API pública (Configurações) e rode:
     ./predio expedicao configurar     e depois     ./predio expedicao teste
TXT
