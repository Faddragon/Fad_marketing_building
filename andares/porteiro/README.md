# Porteiro de saída

- **Papel:** única porta de saída do marketing. Um proxy (tinyproxy) que só deixa passar os endereços de `filtro.txt`.
- **Como o marketing usa:** variáveis `HTTPS_PROXY` e `HTTP_PROXY` apontando para `predio-porteiro:8888` (veja `andares/marketing/compose.yml`). A rede do marketing é interna, então o porteiro é o único caminho.
- **Liberar um endereço novo:** edite `filtro.txt` no GitHub, depois `./predio atualizar && ./predio reconstruir porteiro`.
- **Liberado hoje:** `openrouter.ai` (modelo de IA) e `api.telegram.org` (o dono conversa com o marketing pelo Telegram). Nada mais.
- **Conferir:** `./predio auditar` confirma que o marketing só está em rede interna.
- **Status:** configuração ainda não testada na VPS. Teste: de dentro do marketing, `openrouter.ai` e o Telegram respondem e qualquer outro site é negado.
