# A ficha do trabalho (o que o marketing lê)

Arquivo: `/opt/correio/trabalhos/<id>/ficha.json`. O carteiro cria a ficha a partir do pedido do skip e a atualiza a cada etapa. O marketing só lê.

```json
{
  "id": "2026-10-19-071500",
  "marca_id": "francisco-dias",
  "tema": "Nódulo de tireoide: nem todo é câncer",
  "angulo": "tranquilizar e explicar quando investigar",
  "publico": "adultos leigos, 30 a 60 anos",
  "pecas": [
    {"tipo": "carrossel", "rede": "instagram", "slides": 8},
    {"tipo": "roteiro-video", "rede": "instagram", "duracao_seg": 60},
    {"tipo": "ganchos-reels", "rede": "instagram", "quantidade": 3},
    {"tipo": "post-linkedin", "rede": "linkedin"}
  ],
  "pesquisa": "P-2026-10-19-0710",
  "tema_da_pesquisa": 1,
  "pedidos_do_medico": "tom calmo; citar a diretriz da SBEM",
  "proibido": ["citar marca de medicamento"],
  "origem": "medico",
  "etapa": "conceito",
  "versao": 2,
  "rodada": 2,
  "conceito_aprovado": null,
  "ajustes": [
    {"etapa": "arte", "comentario": "gancho 2 alarmista", "em": "2026-10-19T09:10:00-03:00"}
  ],
  "status": "conceito_producao",
  "criado_em": "2026-10-19T07:15:00-03:00",
  "atualizado_em": "2026-10-19T09:10:00-03:00"
}
```

## Campos que mudam o trabalho
- `pecas`: só produza estas. `slides`, `duracao_seg` e `quantidade` têm prioridade sobre o padrão da skill de cada peça.
- `pedidos_do_medico`: obrigatório seguir.
- `proibido`: nunca use.
- `etapa` e `versao` (`rodada` é igual): devem bater com o pedido do carteiro. Se não baterem, grave `erro.txt`. A pasta de entrega é `<etapa>-v<versao>/`.
- `conceito_aprovado`: nome da pasta do conceito aprovado (ex.: `conceito-v2`). A etapa `arte` usa o texto dela.
- `ajustes`: pedidos do médico depois de ver a prévia. Quando houver, a `devolutiva-<etapa>-v<N>.md` mais recente os repete: cada um precisa aparecer em `mudancas.md`.
- `marca_id`: pode ser `null` quando o pedido não trouxe marca; veja o passo 0 da skill.
