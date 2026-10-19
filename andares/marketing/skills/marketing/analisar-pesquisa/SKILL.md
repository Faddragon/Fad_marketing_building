---
name: analisar-pesquisa
description: Analisa a pesquisa que o skip trouxe (sem internet) junto com as métricas e as lições, e entrega o que funciona, as lacunas e o ângulo do conteúdo. Primeiro passo da etapa conceito, chamado pelo processar-ficha.
---

# analisar-pesquisa

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

Você não busca nada. Trabalha só com o que o skip já trouxe em `pesquisa.md`.

## Entrada
- `pesquisa.md` da ficha (temas em alta, posts de referência, fontes).
- `correio/metricas/` mais recente (o que deu resultado nas redes do médico).
- `correio/licoes.md`.
- `marca/perfil.json` (temas que pode divulgar e que deve evitar), `marca/manifesto.md` e `marca/tom-de-voz.md`.
- `devolutiva` da versão anterior, se houver.

## O que fazer
1. Descubra o que está funcionando nos materiais da pesquisa: formatos, ganchos, temas, profundidade.
2. Marque as lacunas: o que ninguém explica bem, dúvidas comuns sem resposta clara, mitos sem correção.
3. Cruze com as métricas: o que já funcionou com o público do médico.
4. Confira o tema contra `temas.evitar` de `perfil.json`. Se o tema estiver na lista, pare e escreva em `avisos.md`.
5. Proponha **um ângulo principal** e até dois alternativos. Cada ângulo: promessa de valor para o leitor (sem prometer resultado de saúde), por que é diferente do que já existe, e o gancho em uma frase.

## Saída: `conceito-v<N>/analise.md`
```
# Análise
## O que funciona
## Lacunas
## Métricas relevantes
## Ângulo principal
## Alternativos
## Fatos que podem ser usados (com a fonte de pesquisa.md)
## Pontos sem fonte (não usar como fato)
```

## Regras
- Dado, número, estudo e citação só entram com a fonte que está em `pesquisa.md`. Sem fonte, vai para "Pontos sem fonte".
- Não copie texto de posts de referência. Analise a estrutura e a ideia.
- Se a pesquisa vier fraca, diga isso no início do arquivo e registre em `avisos.md`.
- Se `marca/manifesto.md` existir, o ângulo tem que ser coerente com ele.
