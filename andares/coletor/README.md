# Andar coletor (script sem IA)

**Papel:** ler perfis profissionais do Instagram pela API oficial da Meta (Business Discovery) e gravar os dados para o skip analisar. Roda sozinho todo dia (padrão 06:00, São Paulo).

**Por que existe:** o token da Meta é um segredo poderoso. Ele fica aqui, num código curto e sem IA, e nunca com um agente que lê páginas da internet.

## O que ele faz
1. Lê a lista em `correio/config/referencias.md` (seção Instagram) e o ritmo em `correio/config/instagram.md` (`perfis_por_dia`, padrão 3, máximo 5).
2. Pega os perfis coletados há mais tempo e consulta a API da Meta, 1 por vez, com pausa entre eles.
3. Grava `correio/pesquisas/referencias/<perfil>/dados.json` (legenda, tipo, link, data, curtidas e comentários dos posts mais recentes, seguidores).
4. Escreve o estado em `correio/avisos/coletor.md` (último resultado, dias até o token vencer, erros).
5. Renova o token sozinho quando faltam menos de 20 dias.

## Limites
- Só perfis **profissionais** (comercial ou criador). Perfil pessoal ou privado dá erro, e o aviso diz qual.
- Não traz salvamentos, compartilhamentos nem alcance de perfis de terceiros, e não traz o visual (slides, vídeo). Para o visual, use prints com a skill `estudar-post`.
- Não faz login, não publica, não curte, não comenta. Só lê.

## Segurança
- Contêiner com sistema de arquivos só leitura, sem privilégios, 128 MB, usuário 10000.
- Pastas montadas: `config` (só leitura), `referencias` e `avisos` (escrita) e o segredo dele. Não enxerga o resto do correio nem os Hermes.
- Só chama `graph.facebook.com` (o código tem esse endereço fixo). A rede dele é a `predio_externa`, então essa restrição é do código, não da rede.
- O token nunca aparece em log nem em arquivo de estado.

## Configurar (uma vez)
Depois de `./predio instalar`:

```bash
# 1. IDs e chave do app (no painel do app: Configurações, Básico). Não cole aqui nem no Telegram.
nano /opt/predio-dados/segredos/coletor/instagram.env
```
Conteúdo do arquivo (3 linhas, sem aspas):
```
APP_ID=...
APP_SECRET=...
IG_USER_ID=17841408401067530
```
```bash
chown 10000:10000 /opt/predio-dados/segredos/coletor/instagram.env
chmod 600 /opt/predio-dados/segredos/coletor/instagram.env
cd /opt/predio && ./predio subir coletor

# 2. Token (gerado no Explorador da Graph API; a entrada some do histórico por causa do -s)
read -rsp "Cole o token: " T; echo
printf '%s' "$T" | docker exec -i predio-coletor python /app/coletor.py iniciar
unset T
```
O comando responde "Token de longa duracao guardado. Conta: @... Vence em N dias."

## Dia a dia
| Quero... | Comando |
| --- | --- |
| Ver o estado | `docker exec predio-coletor python /app/coletor.py status` |
| Coletar agora | `docker exec predio-coletor python /app/coletor.py agora` |
| Ver o que fez | `./predio logs coletor` |
| Mudar a hora | `COLETA_HORA=07:30 ./predio reconstruir coletor` |
| Token vencido | gerar outro no Explorador e repetir o passo 2 |
