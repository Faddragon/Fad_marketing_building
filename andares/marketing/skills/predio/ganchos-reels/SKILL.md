---
name: ganchos-reels
description: Cria 3 ganchos de reels, cada um com abertura, desenvolvimento e chamada para ação, para o médico escolher e gravar. Use na etapa conceito quando o pacote incluir ganchos.
---

# ganchos-reels

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

## Entrada
`analise.md`, `referencia/estrutura.md` (se houver), `marca/tom-de-voz.md`, `marca/perfil.json`, `correio/licoes.md`.

`references/squad.md`, se existir, manda no método.

## O que entregar
Três ganchos com abordagens **diferentes** entre si (por exemplo: pergunta que quebra um mito, dado ou fato verificável da pesquisa, situação do dia a dia). Cada reel dura de 20 a 40 segundos.

## Saída: `conceito-v<N>/ganchos.md`
```
# Ganchos de reels
Ângulo: ...

## Gancho 1: <nome curto>
Abordagem: (mito, dado, situação...)
Abertura (0-3s): (frase falada + texto na tela)
Desenvolvimento (3-25s): (2 a 3 pontos em frases curtas)
Chamada para ação: (uma frase)
Legenda sugerida: (2 a 3 linhas + rodapé_obrigatorio)

## Gancho 2
...
## Gancho 3
...

## Recomendação
(qual gravar primeiro e por quê, em 2 linhas)
```

## Regras
- A abertura tem que funcionar sozinha, sem contexto.
- Nada de clickbait que a entrega não cumpra, nem alarmismo. Se o gancho promete algo, o desenvolvimento entrega.
- Fatos só com fonte de `analise.md`. Dado sem fonte não entra.
- Sem promessa de resultado, sem "antes e depois", sem caso de paciente.
- Os 3 ganchos devem ser diferentes de verdade: se dois forem parecidos, troque um.
