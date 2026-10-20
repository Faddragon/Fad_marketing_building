# Andar Carteiro

Script sem IA e **sem internet**. Leva cada trabalho de uma etapa à outra e nunca julga conteúdo: quem julga é o skip, quem aprova é o médico.

```
pedidos/<id>.json  (skip)
   -> trabalhos/<id>/            ficha.json, pedido.json, pesquisa.md
   -> marketing (API do Hermes)  conceito-v1/  com 'pronto'
   -> parecer do skip            revisoes/<id>-conceito-v1.json
   -> marketing                  arte-v1/  (post.json + imagens) com 'pronto'
   -> parecer do skip            revisoes/<id>-arte-v1.json
   -> prontos/<id>/              a expedição assume (revisão final, código, Postiz)
```

- **Reprovado**: grava `devolutiva-<etapa>-v<N+1>.md`, anota a lição em `licoes.md` e o marketing refaz. Duas reprovações na mesma etapa: `parado`.
- **Ajuste do médico** (depois da prévia): recomeça pelo conceito, com o pedido dele na devolutiva.
- **Dado de paciente** (CPF, "paciente Nome Sobrenome", nº de prontuário): barra o pedido ou a entrega, oculta o texto e não copia o trecho para lugar nenhum.
- **Falha do marketing**: tenta de novo até 3 vezes; depois vira `erro`.
- **Resumo**: `correio/avisos/carteiro.md`.

## Como o marketing é acordado

O Hermes tem um servidor de API próprio. Ele fica ligado **só dentro da rede interna** (`API_SERVER_HOST=0.0.0.0`, sem `ports:`). O carteiro chama `POST /v1/runs` (com `Idempotency-Key`, para uma repetição não duplicar o trabalho) e acompanha `GET /v1/runs/<id>`. A chave fica em `segredos/api-marketing/api.env` e só o carteiro e o marketing a recebem. **O skip nunca a vê.** A chave dá acesso à ferramenta completa do marketing (inclusive terminal), por isso não sai dessa pasta.

## Instalar

```
git pull
./predio atualizar
./predio carteiro-preparar
./predio reconstruir skip
./predio reconstruir marketing
./predio subir carteiro
./predio carteiro teste
```

`carteiro teste` confere a chave e faz um pedido de uma palavra ao marketing. Se falhar em `health`, a API do Hermes não está escutando em `0.0.0.0` (veja `./predio logs marketing`).

## Primeiro teste de ponta a ponta (sem publicar nada)

```
./predio carteiro exemplo
./predio carteiro status
```

No Telegram, peça ao skip: `revisa as etapas`. Repita a cada etapa (ou deixe a tarefa agendada do guardião fazer). Antes disso, deixe a expedição em `MODO=teste`.

## Comandos

```
./predio carteiro status
./predio carteiro reabrir <id>
./predio carteiro descartar <id>
./predio carteiro teste
./predio carteiro exemplo
```
