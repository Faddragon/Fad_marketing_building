# Migração: dos Hermes atuais para o prédio

Situação de partida (19/10/2026): dois contêineres soltos, criados à mão.

| Hoje | Vira | Memória atual | Nova memória |
|---|---|---|---|
| `hermes` (skip) | `predio-skip` | `/opt/medico/hermes/data` | `/opt/predio-dados/skip` |
| `andar-teste` (marketing) | `predio-marketing` | `/opt/tower/andar-teste/data` | `/opt/predio-dados/marketing` |

Regra: **um andar por vez, o antigo só é apagado depois de uma semana.** Não mexa em `/home/bmed-shield` nem no painel Hestia.
Dois Hermes nunca podem usar o mesmo bot ao mesmo tempo: o antigo é parado antes de o novo subir.

## 0. Antes de tudo
```bash
du -sh /opt/medico /opt/tower
tar czf /root/backup-hermes-$(date +%Y%m%d).tgz /opt/medico /opt/tower
```

## 1. Trazer o repositório (chave só de leitura)
```bash
ssh-keygen -t ed25519 -f /root/.ssh/fad_building -N "" -C "vps-fad-building"
cat /root/.ssh/fad_building.pub
```
No GitHub: repositório → Settings → Deploy keys → Add deploy key (deixe "Allow write access" desmarcado). Depois:
```bash
ssh-keyscan github.com >> /root/.ssh/known_hosts
printf 'Host github-fad\n  HostName github.com\n  User git\n  IdentityFile /root/.ssh/fad_building\n  IdentitiesOnly yes\n' >> /root/.ssh/config
chmod 600 /root/.ssh/config
git clone git@github-fad:Faddragon/Fad_marketing_building.git /opt/predio
cd /opt/predio && chmod +x predio && ./predio instalar
```

## 2. Porteiro
```bash
./predio subir porteiro
./predio status
```
Teste (o proxy deve deixar passar o OpenRouter e negar o resto):
```bash
docker run --rm --network predio_interna curlimages/curl -sS -o /dev/null -w "%{http_code}\n" -x http://predio-porteiro:8888 https://openrouter.ai
docker run --rm --network predio_interna curlimages/curl -sS -o /dev/null -w "%{http_code}\n" -x http://predio-porteiro:8888 https://example.com
```
O primeiro deve dar 200 (ou 3xx); o segundo deve falhar ou dar 403.

## 3. Marketing
O marketing continua falando com o dono pelo Telegram: o `filtro.txt` já libera `api.telegram.org`. Se o bot não responder depois da subida, veja `./predio logs marketing` (o Hermes pode ter configuração própria de proxy para o Telegram).
```bash
docker stop andar-teste && docker update --restart=no andar-teste
cp -a /opt/tower/andar-teste/data/. /opt/predio-dados/marketing/
./predio subir marketing
./predio conversar marketing          # digite /skills: devem aparecer as 12 skills do marketing
./predio logs marketing
```
Voltar atrás: `./predio parar marketing && docker start andar-teste`.

## 4. Skip
```bash
docker stop hermes && docker update --restart=no hermes
cp -a /opt/medico/hermes/data/. /opt/predio-dados/skip/
./predio subir skip
./predio conversar skip               # /skills: devem aparecer as 8 skills do skip
```
Voltar atrás: `./predio parar skip && docker start hermes`.

## 5. Auditar
```bash
./predio auditar
```
Deve terminar com "nenhum alerta". Guarde a saída como comprovante do isolamento.

## 6. Uma semana depois
```bash
docker rm andar-teste hermes
```
E arquive (não apague) `/opt/medico` e `/opt/tower` depois de conferir os backups.

## Pontos a conferir na primeira subida (não testados)
- Se o Hermes aceita `SOUL.md` e a pasta de skills montados como **somente leitura** (se escrever neles e falhar, o log mostra).
- Se o comando `hermes chat` existe dentro da imagem (usado por `./predio conversar`).
- Se o marketing consegue falar com o OpenRouter pelo proxy (variáveis `HTTPS_PROXY`).
- O Telegram do marketing passa pelo porteiro (`api.telegram.org`). Confirme que o bot responde. Como o carteiro vai acioná-lo (API interna do Hermes) será definido junto com o carteiro, que ainda não existe.
- Skills novas criadas pelo Telegram nascem em `/opt/predio-dados/<andar>/skills/` (escrita). Crie uma de teste em cada Hermes para confirmar que o resto da pasta de skills aceita escrita, apesar da subpasta do repositório ser só leitura.
- A pasta `/opt/tower/caixa` (pedidos, rascunhos, métricas, aprovados) usa nomes antigos; as skills novas usam `correio/`. Não é migrada automaticamente.
- Os contêineres atuais rodam como `root`. O endurecimento (`no-new-privileges`, usuário sem privilégios) está comentado no `compose.yml` do skip, para testar depois.
