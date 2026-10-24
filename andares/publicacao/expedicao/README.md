# Andar PUBLICAÇÃO

A saída do prédio para as redes. Nada vai para o Instagram ou o LinkedIn sem passar por aqui, e nada passa sem o parecer do skip **e** o código que o médico digita no Telegram.

## Quem mora aqui

| Contêiner | O que é | Internet |
|---|---|---|
| `predio-expedicao` | Script sem IA. Pega o que o carteiro deixou em `prontos/`, pede a revisão ao skip, manda a prévia com código pelo Telegram, agenda no Postiz depois do "ok" e confere se saiu | Só o Telegram |
| `predio-postiz` | O agendador open-source. Guarda as conexões com as redes e publica no horário | Meta e LinkedIn |
| `predio-postiz-postgres`, `predio-postiz-redis` | Banco e fila do Postiz | Não |
| `predio-temporal`, `predio-temporal-postgresql`, `predio-temporal-elasticsearch` | A agenda dos posts (o Postiz exige o Temporal) | Não |

A expedição **não guarda token de rede social**: quem guarda é o Postiz. O skip não enxerga a chave do Postiz nem os códigos.

Nenhuma porta fica aberta para a internet. O Postiz escuta só em `127.0.0.1:4007`; quem o leva ao público é o Cloudflare.

## Memória da VPS

Com este andar, o prédio soma uns 3 GB de limite a mais (Postiz 1,5 GB, Elasticsearch 0,75 GB, Temporal 0,5 GB, bancos e fila). Some com o skip (3 GB) e o marketing (2 GB) e confira com `free -h`. O uso real costuma ficar abaixo dos limites.

## Passo a passo

### 1. Preparar (uma vez)
```bash
cd /opt/predio && git pull && chmod +x predio && ./predio instalar
./predio postiz-preparar postiz.drfranciscodias.com.br
```
Ele cria as senhas em `/opt/predio-dados/segredos/postiz/` e pergunta, sem mostrar na tela, o ID e o segredo do app Meta ("Predio Hermes") e do LinkedIn. Pode deixar em branco e preencher depois no arquivo.

### 2. Subir
```bash
./predio subir publicacao
./predio status
```
A primeira subida demora alguns minutos (baixa as imagens). O Postiz leva até 2 minutos para ficar "healthy".

### 3. Abrir o Postiz para a internet pelo Cloudflare
O Meta precisa alcançar o Postiz por HTTPS: para o login do Instagram e para baixar as imagens do post.

- **Túnel (recomendado):** instale o `cloudflared` na VPS e crie um túnel com o nome `postiz.drfranciscodias.com.br` apontando para `http://localhost:4007`. Não mexe no site que já roda na VPS.
- **Cuidado com o bloqueio de robôs:** se o Cloudflare estiver com "Bot Fight Mode" ou regras de WAF, crie uma exceção para este subdomínio, senão o Meta não consegue baixar as imagens e o post falha com erro de mídia.

### 4. Criar a conta e fechar o cadastro
Abra `https://postiz.drfranciscodias.com.br`, crie a sua conta e rode:
```bash
./predio postiz-fechar
```

### 5. Conectar o Instagram
No Meta for Developers, no app "Predio Hermes":
- **Login for Business** ativo e este redirecionamento em OAuth: `https://postiz.drfranciscodias.com.br/integrations/social/instagram`
- Permissões: `instagram_basic`, `pages_show_list`, `pages_read_engagement`, `business_management`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_insights`
- Enquanto o app não passar pela revisão da Meta, só publicam as contas com papel no app (administrador, desenvolvedor ou testador). Para a conta do Dr. Francisco isso basta; se aparecer "Insufficient developer role", adicione a conta como testadora do Instagram em Funções do app.

No Postiz, em **Canais > Adicionar canal > Instagram** (o de Facebook Business, ligado à Página "Dr Francisco Dias") e autorize.

Não conecte os dois tipos de Instagram ao mesmo tempo: a expedição para com "mais de um canal de instagram". Se precisar, defina `POSTIZ_CANAL_INSTAGRAM=<id>` no `expedicao.env`.

### 6. Ligar a expedição ao Postiz e ao Telegram
No Postiz, em Configurações, gere a chave da API pública. Depois:
```bash
./predio expedicao configurar     # Postiz (Enter = padrão), chave, token do bot, seu ID no Telegram, modo
./predio expedicao teste          # confere canais e manda uma mensagem de teste
```
O `MODO` começa em `teste`.

### 7. Testar o caminho todo, do mais seguro ao real
1. `./predio expedicao exemplo` cria um post de exemplo em `prontos/`.
2. Em `teste` a prévia e o código funcionam, mas o Postiz não é chamado.
3. Troque para `rascunho` (`./predio expedicao configurar`): cria o rascunho no Postiz, sem agendar. Confira lá.
4. Troque para `agendar`. A expedição nunca publica na hora: o mínimo é 10 minutos à frente.

## Modos da expedição

| Modo | O que acontece |
|---|---|
| `teste` | Prévia e código funcionam; o Postiz não é usado |
| `rascunho` | Cria rascunho no Postiz, sem agendar |
| `agendar` | Agenda de verdade depois da segunda aprovação |

Se o médico aprova e nada é agendado, o modo está em `teste` ou `rascunho`.

## Pausar a publicação
O skip pausa e retoma pelo Telegram ("pausa as publicações"). Ele grava `config/publicacao.md` com `publicacao: pausada`.

## Se algo não funciona

| Sintoma | O que fazer |
|---|---|
| `./predio subir publicacao` pede para preparar o Postiz | Rodar `./predio postiz-preparar <dominio>` |
| Postiz não fica "healthy" | `./predio logs publicacao` e ver o `predio-postiz` |
| `Postiz respondeu 401` | A chave da API pública está errada ou foi refeita: `./predio expedicao configurar` |
| `nenhum canal de instagram conectado` | Conectar o Instagram em Canais no Postiz |
| `mais de um canal` | Desconectar o que sobra ou definir `POSTIZ_CANAL_INSTAGRAM` |
| `Postiz respondeu 429` | Limite de 30 posts por hora; esperar |
| Erro de mídia ao publicar | O Meta não alcançou as imagens: conferir o túnel e o bloqueio de robôs do Cloudflare |
| Trabalho preso | `./predio expedicao status`; para receber de novo: `./predio expedicao reabrir <id>` |
| Prévia não chega | Conferir `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`: `./predio expedicao teste` |

## Backup
Os dados do Postiz (contas conectadas, imagens, agenda) ficam em volumes Docker, **fora** de `/opt/predio-dados`. Uma cópia simples de `/opt/predio-dados` não os inclui. Para guardar o banco do Postiz:
```bash
docker exec predio-postiz-postgres pg_dump -U postiz-user postiz-db-local > /opt/predio-dados/postiz-$(date +%F).sql
```
As senhas ficam em `/opt/predio-dados/segredos/postiz/` e entram no backup normal.
