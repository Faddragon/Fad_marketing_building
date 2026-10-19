---
name: pedir-pacote
description: Transforma o "faz" do médico numa ficha de pedido para o andar de marketing (tema, ângulo, peças, redes, pesquisa e prints). Use quando ele escolher um tema sugerido ("faz o 1") ou encomendar conteúdo ("faz um carrossel sobre X", "pacote completo de Y").
version: 1.0.0
---

# Pedir pacote ao marketing (skip)

Você não cria o conteúdo. Você entrega ao marketing uma ficha clara, com tudo o que ele precisa, porque ele não tem internet e não pode perguntar nada ao médico.

## 1. Descubra o tema e a pesquisa

| O médico disse... | Faça |
| --- | --- |
| "faz o 2" | Abra a pesquisa mais recente em `/opt/correio/pesquisas/` e pegue o tema 2. |
| "faz sobre X" e já existe pesquisa de X dos últimos 7 dias | Use essa pesquisa. |
| "faz sobre X" sem pesquisa | Rode antes a skill `pesquisar-tema` no **modo focado**, sem perguntar o ângulo: escolha o de maior nota e diga qual escolheu na confirmação. |

Se o tema exigir caso de paciente, antes e depois ou promessa de resultado, pare e proponha a versão educativa (SOUL.md, regras 1 e 2).

## 2. Defina as peças

O padrão está em `references/pacote-padrao.md`. "Pacote completo" ou só "faz" significa todas as peças do padrão. Se ele citar peças ("só carrossel e LinkedIn"), peça apenas essas.

Só pergunte o que mudaria o trabalho e não dá para deduzir, e no máximo **uma** pergunta. Exemplo: "Carrossel para o Instagram e o LinkedIn, ou só Instagram?".

## 3. Grave a ficha

1. Gere o id `AAAA-MM-DD-HHMMSS` com a hora de São Paulo.
2. Grave `/opt/correio/pedidos/<id>.json` no formato de `references/ficha-pedido.md`.
3. Leia o arquivo de volta e confira que o JSON é válido e que a pasta da pesquisa citada existe.

O carteiro pega a ficha, abre a pasta `/opt/correio/trabalhos/<id>/` e chama o marketing. Daí em diante o andamento fica na `ficha.json` do trabalho (veja a skill `status-e-licoes`).

## 4. Pedido de ajuste vindo do médico sem código

Se ele pedir para mudar algo de um trabalho em andamento, mas sem código ("muda o tom daquele de tireoide"), **não** grave ficha nova: peça o código da prévia (o ajuste passa pela skill `decidir`).

## 5. Confirme em uma ou duas linhas

"Anotado: carrossel, roteiro de vídeo, 3 ganchos de reels e LinkedIn sobre nódulo de tireoide (ângulo: nem todo é câncer). O conceito chega aqui com um código para você aprovar."

## Não faça
- Não escreva legenda, roteiro nem slide: isso é do marketing.
- Não grave fora de `/opt/correio/pedidos/`.
- Não ponha na ficha nada que não esteja na pesquisa ou na fala do médico.
- Não prometa prazo.
