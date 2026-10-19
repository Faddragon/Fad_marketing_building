# Formato da ficha de pedido

Arquivo: `/opt/correio/pedidos/<id>.json`. O carteiro e o marketing leem estes campos pelo nome: não renomeie nenhum.

```json
{
  "id": "2026-10-19-071500",
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
  "criado_em": "2026-10-19T07:15:00-03:00"
}
```

## Campos
- `angulo`: o recorte do tema, numa frase. Vem da pesquisa ou do médico.
- `publico`: padrão "adultos leigos"; use "médicos e gestores" quando o pedido for só para o LinkedIn profissional.
- `pecas`: só as pedidas. Campos extras (`slides`, `duracao_seg`) só quando diferentes do padrão, ou para deixar claro.
- `pesquisa`: o id da pasta em `/opt/correio/pesquisas/`. Obrigatório.
- `pedidos_do_medico`: o que ele pediu com as palavras dele, sem dado de paciente. Vazio se nada.
- `proibido`: o que ele disse para evitar neste trabalho. Lista vazia se nada.
- `origem`: `medico` ou `rotina`.
