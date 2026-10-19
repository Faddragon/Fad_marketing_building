---
name: rotina-diaria
description: Pesquisa automática diária - roda a pesquisa de temas sozinha e manda as sugestões cedo no Telegram (ou já encomenda o pacote, se o modo for "encomendar"). Use quando a tarefa agendada disparar, quando o médico pedir "roda a rotina" ou quando ele quiser pausar, voltar ou mudar o horário da rotina.
version: 1.0.0
---

# Rotina diária (skip)

## Ajustes (edite aqui)

| Ajuste | Padrão | Opções |
| --- | --- | --- |
| Horário | 06:30 (São Paulo) | qualquer hora; a mensagem chega nesse horário |
| Dias | segunda a sexta | todo dia, dias específicos |
| Modo | `sugerir` | `sugerir`: só manda os temas. `encomendar`: já faz o pedido do tema de maior nota |
| Peças no modo `encomendar` | pacote padrão | qualquer lista de `pacote-padrao.md` |
| Fazer a rotina se houver trabalhos esperando o médico | não | sim / não |

O padrão é `sugerir` porque encomendar gasta trabalho do marketing num tema que ele pode não querer.

## 1. Quando a tarefa disparar

1. **Evite acumular.** Se o ajuste acima for "não" e houver 2 ou mais trabalhos em `/opt/correio/trabalhos/*/ficha.json` com etapa `voce-conceito` ou `voce-final`, não pesquise. Mande só: "Bom dia. Há 2 prévias esperando você; hoje não puxei temas novos."
2. **Pesquise.** Rode a skill `pesquisar-tema` no **modo aberto**, com a Apify se disponível (pesquisa barata e sempre igual) e com o pedido "rotina diária". Ela já lê as métricas e evita temas repetidos.
3. **Modo `sugerir`:** mande a mensagem da pesquisa, começando por "Bom dia." e terminando com "Responda 'faz o 1' (ou 2, 3) para encomendar."
4. **Modo `encomendar`:** rode a skill `pedir-pacote` com o tema de maior nota, `"origem": "rotina"` e as peças do ajuste. Mande: "Bom dia. Encomendei o pacote de '<tema>'. Outras opções: 2. ... 3. ... O conceito chega com um código."
5. Se a pesquisa falhar (sem internet, sem fontes), mande uma linha honesta: "Bom dia. A pesquisa de hoje falhou (motivo curto). Tento amanhã."

Fora disso, não mande mensagens. Uma por dia, no máximo.

## 2. Ligar, pausar e mudar

Use a ferramenta de tarefas agendadas do Hermes (cron).

| O médico diz | Faça |
| --- | --- |
| "liga a rotina" (e não existe tarefa) | Crie a tarefa: nos dias e horário dos ajustes, "use a skill rotina-diaria", entregando neste chat. Confirme o horário. |
| "pausa a rotina" | Pause ou desative a tarefa. Confirme: "Rotina pausada. 'volta a rotina' para religar." |
| "volta a rotina" | Reative. Confirme o próximo disparo. |
| "muda a rotina para 7h" | Reagende e confirme. Avise que o padrão do arquivo continua 06:30, se ele quiser tornar fixo no GitHub. |
| "roda a rotina agora" | Execute a seção 1 agora, sem mexer na tarefa. |
| "rotina em modo encomendar" | Use esse modo a partir de agora (memória) e avise que, para ficar fixo, deve editar esta skill no GitHub. |

Mantenha uma tarefa só. Antes de criar, liste as tarefas e veja se já existe uma da rotina.

## Não faça
- Não mande mensagem de madrugada nem mais de uma por dia.
- Não encomende no modo `sugerir`.
- Não crie tarefas duplicadas.
