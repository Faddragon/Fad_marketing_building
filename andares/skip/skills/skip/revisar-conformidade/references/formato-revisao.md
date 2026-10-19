# Formato do parecer

Arquivo: `/opt/correio/revisoes/<id>-<etapa>-r<rodada>.json`. A expedição e o carteiro leem estes campos pelo nome.

```json
{
  "id": "2026-10-19-071500",
  "etapa": "conceito",
  "rodada": 1,
  "resultado": "reprovado",
  "pontos": [
    {
      "peca": "carrossel",
      "local": "slide 1",
      "regra": "CFM-02",
      "problema": "Título 'O câncer silencioso que pode te matar' é alarmista.",
      "como_corrigir": "Trocar por tom informativo, por exemplo 'Nódulo na tireoide: quando investigar'."
    },
    {
      "peca": "post-linkedin",
      "local": "parágrafo 2",
      "regra": "CFM-11",
      "problema": "'95% dos nódulos são benignos' não está na pesquisa (a fonte diz 90 a 95%).",
      "como_corrigir": "Usar 'cerca de 9 em cada 10', como na fonte ATA."
    }
  ],
  "alertas": [
    {"peca": "ganchos-reels", "local": "gancho 3", "nota": "Pode soar informal demais para o perfil."}
  ],
  "resumo": "Dois pontos: título alarmista e número sem fonte. Resto ok.",
  "revisado_em": "2026-10-19T08:02:00-03:00"
}
```

## Valores
- `etapa`: `conceito` ou `arte`.
- `resultado`: `aprovado`, `reprovado` ou `parar`.
- `pontos`: lista vazia quando aprovado.
- `regra`: o id da regra (LGPD-xx, CFM-xx, VIS-xx) ou `PED-01` (fora do pedido) e `PED-02` (arquivo faltando ou ilegível).
- `resumo`: uma frase. A expedição mostra ao médico junto da prévia ou do aviso de parada.
