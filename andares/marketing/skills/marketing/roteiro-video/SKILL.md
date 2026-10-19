---
name: roteiro-video
description: Escreve o roteiro de um vídeo curto de Instagram (cenas, fala, tempo, texto na tela e legenda) para o médico gravar. Use na etapa conceito quando o pacote incluir vídeo. O prédio entrega roteiro, não grava nem edita vídeo.
---

# roteiro-video

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

## Entrada
`analise.md`, `referencia/estrutura.md` (se houver), `marca/perfil.json`, `marca/tom-de-voz.md`, `correio/licoes.md`, o pedido (duração, se informada).

`references/squad.md`, se existir, manda no método. Este arquivo garante formato e regras.

## Método
- Duração padrão: 45 a 60 segundos, falada para câmera por uma pessoa só, em local simples.
- Gancho nos 3 primeiros segundos: uma frase que o médico fala já com o rosto na câmera.
- Estrutura: gancho, uma ideia principal, dois ou três pontos, fechamento com chamada para ação.
- Fala natural, do jeito que o médico falaria (use `tom-de-voz.md`). Frases curtas. Evite jargão sem explicar.
- Texto na tela: palavras-chave, não a fala inteira.
- O médico grava no celular. Não peça equipamento, cenário caro nem figurante.

## Saída: `conceito-v<N>/video.md`
```
# Vídeo: <título>
Duração: ~X s · Ângulo: ...

| Tempo | Cena | Fala | Texto na tela |
|---|---|---|---|
| 0-3s | ... | ... | ... |

## Legenda
(primeira linha forte, corpo curto, chamada para ação, rodapé_obrigatorio)

## Capa sugerida
(ideia de capa: frase e visual simples; a arte final é do arte-final)

## Dicas de gravação
(3 itens: luz, enquadramento, ritmo)
```

## Regras
- Fatos só com fonte de `analise.md`. Sem fonte, não afirme.
- Sem promessa de resultado, "antes e depois", sensacionalismo, nem dado ou caso de paciente. Não use paciente como personagem, nem fictício que pareça real. Para exemplos, use situação genérica.
- Sem orientação clínica individual. O vídeo informa; não substitui consulta.
- O médico é o responsável final pelo que fala. Sinalize em `previa.md` qualquer afirmação clínica que ele deve conferir.
