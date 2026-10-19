---
name: post-linkedin
description: Escreve o texto do post de LinkedIn no tom profissional do médico. Use na etapa conceito quando o pacote incluir LinkedIn.
---

# post-linkedin

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

## Entrada
`analise.md`, `referencia/estrutura.md` (se houver), `marca/perfil.json`, `marca/tom-de-voz.md`, `marca/manifesto.md`, `correio/licoes.md`.

`references/squad.md`, se existir, manda no método.

## Método
- Público: colegas, gestores de saúde, pacientes que buscam informação séria. Tom profissional e humano, sem jargão desnecessário.
- Primeira linha forte (o LinkedIn corta o texto depois das primeiras linhas).
- Parágrafos de 1 a 2 linhas, com espaço entre eles.
- Corpo: uma ideia central, desenvolvida em 3 a 5 blocos. Pode usar uma lista curta.
- Fechamento com uma pergunta ou chamada para ação leve.
- Extensão: de 900 a 1.500 caracteres, salvo pedido diferente.
- Hashtags: 3 a 5, específicas.
- Se o pedido incluir imagem para o LinkedIn, descreva a ideia em uma linha; a arte é do `arte-final`.

## Saída: `conceito-v<N>/linkedin.md`
```
# Post de LinkedIn
Ângulo: ...

<texto do post>

Hashtags: ...
Identificação profissional: (rodape_obrigatorio, quando aplicável)
Ideia de imagem: ...
```

## Regras
- Fatos só com fonte de `analise.md`. Sem fonte, não afirme.
- Sem promessa de resultado, sem "antes e depois", sem sensacionalismo, sem dado ou caso de paciente.
- Não escreva como se fosse outra pessoa nem invente cargo, título ou premiação do médico. Só o que está em `perfil.json`.
- Não use "eu atendi um paciente que...". Use situação genérica ("muita gente pergunta...").
