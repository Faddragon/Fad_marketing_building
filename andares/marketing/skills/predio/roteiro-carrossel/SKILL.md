---
name: roteiro-carrossel
description: Escreve o texto de cada slide do carrossel de Instagram, um esboço de layout e a legenda. Use na etapa conceito, depois de analisar-pesquisa, quando o pacote incluir carrossel.
---

# roteiro-carrossel

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

## Entrada
`analise.md` (ângulo), `referencia/estrutura.md` (se houver), `marca/perfil.json`, `marca/tom-de-voz.md`, `marca/manifesto.md`, `correio/licoes.md` e o pedido (número de slides, se informado).

Se existir `references/squad.md` nesta skill (conteúdo do squad de carrossel do OpenSquad), ele manda no método de criação. Este arquivo garante o formato e as regras.

## Método
- Quantidade: a do pedido; se omitida, 7 slides (capa, 5 de conteúdo, fechamento). Para economizar custo na primeira semana, 5 é aceitável.
- Capa: o gancho do ângulo, em até 10 palavras.
- Um conceito por slide. Texto curto: até 30 palavras por slide, frases curtas.
- Ordem: gancho, problema ou dúvida, explicação em passos, correção de mito (se couber), resumo, fechamento.
- Fechamento: chamada para ação de baixo atrito (salvar, compartilhar, conversar na consulta). Sem pressão, sem urgência artificial.
- Se houver estrutura de referência, siga formato e ritmo, nunca o texto.

## Saída: `conceito-v<N>/carrossel.md`
```
# Carrossel: <título>
Ângulo: ...
Slides: N

## Slide 1 (capa)
Título:
Texto:
Esboço visual: (posição do texto, tipo de imagem ou ícone, destaque)

## Slide 2
...

## Último slide
Texto de fechamento:
Rodapé: (rodape_obrigatorio de perfil.json, quando for saúde)
```

## Saída: `conceito-v<N>/legenda-instagram.md`
- Primeira linha forte (aparece antes do "ver mais").
- Corpo curto, em parágrafos de 1 a 2 linhas.
- Chamada para ação.
- Rodapé de identificação profissional (`rodape_obrigatorio`).
- Hashtags: poucas e específicas (a lista segue o que `otimizar` conferir para a rede).

## Regras
- Fatos só os de `analise.md` com fonte. Sem fonte, não afirme.
- Sem promessa de resultado, garantia, "cura", antes e depois, comparação com colegas, nem dado de paciente.
- Esboço visual pensa na marca: usa a paleta e as fontes de `marca/`, sem inventar cor.
- Respeite as lições. Cada lição vale mais do que sua preferência de estilo.
