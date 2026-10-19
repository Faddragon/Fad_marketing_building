---
name: analisar-referencia
description: Transforma o material de uma referência (post, link ou print que o médico mandou, já extraído pelo skip em referencia-bruta.md) em uma ficha de estrutura reaproveitável, sem copiar texto nem imagem. Use na etapa conceito quando houver referencia-bruta.md, ou quando o médico pedir "um post igual a este".
---

# analisar-referencia

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

O skip é os olhos: ele lê o link ou o print e grava `referencia-bruta.md`. Você é a análise: extrai a **estrutura** e descarta o conteúdo. Você não tem internet e não abre links.

## Entrada
`correio/trabalhos/<id>/referencia-bruta.md`, que pode trazer: tipo de post, texto transcrito, descrição visual, número de slides, ordem dos elementos, métricas visíveis, link original. Se houver imagens da referência na pasta da ficha e o modelo aceitar imagem, pode olhá-las.

## Saída: `conceito-v<N>/referencia/estrutura.md`
```
# Estrutura da referência
- Formato: (carrossel, reels, post único, texto)
- Quantidade de slides ou duração:
- Gancho: (tipo: pergunta, dado, afirmação forte, promessa... e por que prende)
- Desenvolvimento: (sequência de blocos, de um em um)
- Chamada para ação: (tipo e posição)
- Tom: (formal, didático, provocador...)
- Estilo visual: (cores, tipografia, densidade de texto, uso de imagem, layout)
- Ritmo: (frases curtas, listas, perguntas...)
- Por que funciona:
- O que NÃO reaproveitar: (texto, imagens, marca, frases, exemplos da referência)
- Adaptação para este médico: (como aplicar a estrutura ao tema do pedido com o tom de marca/tom-de-voz.md)
```

## Regras
- Nunca copie frases, imagens, nome de marca, exemplos ou personagens da referência. Só estrutura, formato e ritmo.
- Se a referência trouxer rosto, depoimento ou caso de paciente, não descreva essa parte: registre "conteúdo com paciente, ignorado".
- Se a referência for de outro profissional de saúde, não imite as promessas ou afirmações dela; aplique as regras de `perfil.json`.
- Referência incompleta (print cortado, link sem texto): faça o que der e liste o que faltou em `avisos.md`, para o skip pedir ao médico.
- Guarde cópia de `estrutura.md` em `marca/referencias/<id>-estrutura.md` apenas se o médico tiver pedido para salvar a referência; caso contrário, só na pasta da versão.
