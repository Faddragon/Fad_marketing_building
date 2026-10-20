# Pacote: carteiro (v1) + API do Hermes

Copie estas pastas e arquivos por cima, nos mesmos caminhos. Nada para apagar.

| Arquivo | Mudança |
| --- | --- |
| `predio` | andar `carteiro`; comandos `carteiro-preparar` (cria a chave) e `carteiro <comando>` |
| `andares/carteiro/` (novo) | `carteiro.py`, `Dockerfile`, `compose.yml`, `README.md` |
| `andares/marketing/compose.yml` | liga a API do Hermes só na rede interna; lê a chave de `segredos/api-marketing/` |
| `andares/marketing/skills/marketing/processar-ficha/` | `SKILL.md` e `references/` com os nomes de pasta que o carteiro usa (`conceito-v<N>`, `arte-v<N>`, `post.json`) |
| `andares/publicacao/expedicao/expedicao.py` | quando o médico pede ajuste, a pasta refeita pelo carteiro volta sozinha para a revisão |
| `andares/skip/skills/skip/guardiao-publicacao` (1.1.0) | revisa também conceito e arte dos trabalhos; avisa trabalho `parado` ou `erro` |
| `andares/skip/skills/skip/manual-do-predio` (3.5.0) | descreve o caminho real com o carteiro e uma única aprovação do médico |

Comandos na VPS, depois de enviar ao GitHub:

```
git pull
./predio atualizar
./predio carteiro-preparar
./predio reconstruir skip
./predio reconstruir marketing
./predio reconstruir publicacao
./predio subir carteiro
./predio carteiro teste
```

No Telegram: `/reload-skills` no skip.
