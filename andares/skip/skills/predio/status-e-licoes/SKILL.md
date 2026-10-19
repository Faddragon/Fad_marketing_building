---
name: status-e-licoes
description: Responde ao médico onde está cada trabalho ("status", "cadê meu post?", "detalhe do de tireoide") e mostra o que o marketing aprendeu ("mostra as lições"), além de propor, uma vez por mês, transformar lições repetidas em regras fixas. Use para qualquer pergunta sobre andamento, pendências ou aprendizado.
version: 1.0.0
---

# Status e lições (skip)

Aqui você só **lê**: as fichas e o livro de lições. A única coisa que você grava é a proposta de promoção (seção 3).

## 1. Status

### "status", "o que está pendente?", "cadê meu post?"
1. Leia `/opt/correio/trabalhos/*/ficha.json`.
2. Mostre no máximo 5 trabalhos, primeiro os que esperam o médico e depois os mais recentes, um por linha: `• <tema curto>: <etapa em palavras>`.

| `etapa` na ficha | Diga |
| --- | --- |
| `pedido`, `conceito` | "em criação no marketing (conceito)" |
| `revisao-conceito` | "em revisão de LGPD e CFM (conceito)" |
| `voce-conceito` | "esperando você aprovar o conceito (código na prévia)" |
| `arte` | "arte final em produção" |
| `revisao-arte` | "em revisão de LGPD e CFM (arte)" |
| `voce-final` | "esperando sua aprovação final (código na prévia)" |
| `agendado` | "agendado: Instagram 20/10 19h; LinkedIn 21/10 8h" (use `agendamentos` da ficha) |
| `parado` | "parado: reprovado 2 vezes, precisa da sua decisão" |
| `descartado` | não liste, salvo se ele pedir "descartados" |

3. Se houver trabalho em `pedido` ou `conceito` há mais de 2 horas (campo `atualizado_em`), acrescente: "O de <tema> está demorando; se quiser, rode `./predio logs marketing`."
4. Sem fichas: "Nenhum trabalho em andamento."

### "detalhe do de tireoide"
Mostre do trabalho: tema, peças, etapa, rodada, data de criação e, se houver, o `resumo` do último parecer em `/opt/correio/revisoes/<id>-*.json`. Até 6 linhas.

### "perdi o código"
Você não vê códigos. Diga: "O código está na mensagem da prévia, aqui no chat. Procure por '<tema>'. Se não achar, peça 'reenvia a prévia de <tema>' e eu aviso a expedição." Para reenviar, grave `/opt/correio/decisoes/<ts>-reenviar.json` com `{"acao": "reenviar", "trabalho": "<id>", "texto_original": "...", "recebido_em": "..."}`. A expedição gera um código novo e invalida o antigo.

## 2. Lições

O carteiro escreve as lições em `/opt/correio/licoes.md` sempre que uma revisão reprova ou o médico pede ajuste. Cada lição é uma linha:

```
- 2026-10-19 | carrossel | CFM-02 | Título alarmista no slide 1 → usar tom informativo ("quando investigar")
- 2026-10-19 | post-linkedin | AJUSTE | Médico pediu texto mais curto → manter até 1.300 caracteres
```

### "mostra as lições"
Mostre as 10 mais recentes, sem a data: `• carrossel: título alarmista no slide 1 → usar tom informativo`.

### "lições do carrossel", "lições de CFM"
Filtre pela peça ou pelo começo do id da regra e mostre até 10.

### "quantas lições?"
Total, as 3 regras que mais aparecem e o número de vezes de cada uma.

## 3. Promover lições (uma vez por mês, ou quando ele pedir)

Lição repetida vira regra fixa, para o marketing acertar de primeira. É o método do Best-Practice Creator do OpenSquad.

**Quando sugerir:** quando o livro passar de 100 linhas ou quando uma mesma regra aparecer 3 ou mais vezes no mês. Sugira uma vez: "Há lições repetidas (CFM-02 apareceu 5 vezes). Quer que eu prepare a promoção?"

**Se ele aceitar:**
1. Agrupe as lições pela regra e pela peça. Fique só com os grupos de 3 ou mais.
2. Para cada grupo, escreva uma regra curta, positiva e testável ("Títulos informam; nunca usam medo ou ameaça"), com 1 exemplo de errado e 1 de certo, tirados das lições.
3. Diga onde cada regra deve morar:
   - regra de texto: skill do marketing da peça (ex.: `marketing/skills/roteiro-carrossel/SKILL.md`, seção "Regras aprendidas")
   - regra de conformidade nova: `skip/skills/revisar-conformidade/references/regras-cfm.md`
   - regra visual: `marketing/marca/identidade.md`
4. Grave a proposta em `/opt/correio/propostas/licoes-AAAA-MM.md`, neste formato:

```markdown
# Promoção de lições: outubro de 2026
versão-alvo: roteiro-carrossel 1.1.0

## Para: marketing/skills/roteiro-carrossel/SKILL.md → "Regras aprendidas"
- Títulos informam; nunca usam medo ou ameaça. (CFM-02, 5 vezes)
  - Errado: "O câncer silencioso que pode te matar"
  - Certo: "Nódulo na tireoide: quando investigar"

## Lições que podem sair do livro depois de aplicar
- as linhas de CFM-02 de 01/10 a 28/10
```

5. Mande ao médico um resumo de até 6 linhas e diga: "A proposta está em `correio/propostas/`. Aplique no GitHub e rode `./predio atualizar`; depois, `./predio licoes arquivar` limpa o livro."

Você não edita skills nem o livro: o médico aplica, porque é ele quem aprova o que o prédio aprende.
