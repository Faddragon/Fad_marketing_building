# Como usar a Apify (adaptado do OpenSquad)

A Apify roda "robôs" (actors) que leem páginas públicas e devolvem dados organizados: posts, datas, números de engajamento. Ela poupa o skip de navegar perfil por perfil e dá números confiáveis.

## Ligar (uma vez, no kit; não é tarefa do skip)
1. Crie uma conta em apify.com. O plano grátis dá créditos mensais suficientes para uma rotina diária pequena.
2. Copie o token em Settings → API & Integrations.
3. Ponha `APIFY_TOKEN=...` em `segredos/skip.env` (nunca no GitHub).
4. Registre o servidor MCP da Apify no `config.yaml` do skip. O servidor hospedado (`https://mcp.apify.com`, com o token no cabeçalho) dispensa Node no contêiner. A configuração exata fica no tutorial do Andar 1; confirme na primeira vez com `./predio conversar skip` e a pergunta "quais ferramentas da apify você tem?".

## Robôs (actors) usados

| Para quê | Actor | Entrada mínima |
| --- | --- | --- |
| Posts de perfis do Instagram | `apify/instagram-scraper` | `directUrls`: links dos perfis; `resultsType`: `posts`; `resultsLimit`: 10; `onlyPostsNewerThan`: `14 days` |
| Posts de uma hashtag | `apify/instagram-hashtag-scraper` | `hashtags`: ["tireoide"]; `resultsLimit`: 20 |
| Busca no Google | `apify/google-search-scraper` | `queries`: "nódulo tireoide diretriz 2025"; `maxPagesPerQuery`: 1 |
| Posts públicos do LinkedIn | escolher na Apify Store (anote aqui o nome do actor escolhido) | link do perfil; limite 10 |

## Regras
- Use sempre limites pequenos (os da tabela). Cada item custa crédito.
- Uma chamada por perfil ou por busca. Não repita a mesma chamada na mesma pesquisa.
- Se a Apify der erro de crédito ou de token, siga sem ela (busca na web) e escreva na pesquisa: "Apify indisponível: <erro curto>".
- Grave um resumo dos dados úteis em `/opt/correio/pesquisas/<id>/dados.json`: perfil, data, formato, primeira linha, curtidas, comentários, visualizações e link. Não grave nome nem foto de quem comentou.
- Comentários de seguidores: leia, se precisar, para entender dúvidas do público, mas não grave nomes nem textos inteiros.
