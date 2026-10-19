# Frases de decisão (edite e acrescente)

Exemplos de como o médico costuma escrever e como o skip registra. Acrescente aqui os jeitos novos que ele usar.

| O médico escreve | acao | horarios / redes | comentario |
| --- | --- | --- | --- |
| ok 4821 | aprovar | {} / null | |
| aprovado 4821, pode seguir | aprovar | {} / null | |
| 4821 ok, só insta | aprovar | {} / ["instagram"] | |
| ok 5190 hoje 19h | aprovar | instagram e linkedin às 19h de hoje / null | |
| ok 5190 insta qui 19h linkedin sex 8h | aprovar | cada rede no seu horário / null | |
| ajustar 4821: gancho 2 alarmista | ajustar | {} / null | gancho 2 alarmista |
| 4821 refaz o slide 3 com menos texto | ajustar | {} / null | refaz o slide 3 com menos texto |
| 4821 troca a cor do fundo para o azul da marca | ajustar | {} / null | troca a cor do fundo para o azul da marca |
| descarta 4821 | descartar | {} / null | |
| 4821 não, tema errado | descartar | {} / null | tema errado |

## Casos em que o skip pergunta antes
- Só o número: "Quer aprovar, ajustar ou descartar o 4821?"
- "ajustar 4821" sem dizer o quê: "O que ajusto no 4821?"
- "ok 5190 de manhã": "Que horas de manhã?"
- "ok 5190 ontem 19h" (no passado): "Esse horário já passou. Qual horário?"
- Código com 3 ou 5 dígitos: "O código tem 4 dígitos. Pode conferir na prévia?"
