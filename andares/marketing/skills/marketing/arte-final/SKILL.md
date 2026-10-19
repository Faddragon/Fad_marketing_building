---
name: arte-final
description: Designer do marketing. Gera os slides finais do carrossel, a capa do vídeo e a imagem do LinkedIn a partir do conceito aprovado e da pasta marca/. Use na etapa arte, chamado pelo processar-ficha.
---

# arte-final

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

## Entrada
- Conceito aprovado: `conceito-v<N>/carrossel.md`, `video.md` (capa sugerida), `linkedin.md` (ideia de imagem).
- `marca/`: `paleta.md` (ou `perfil.json` > `marca.paleta`), fontes em `ativos/fontes/`, logo em `ativos/logo/`, fotos do próprio profissional em `ativos/fotos/`, exemplos de artes, `manual/` se houver.
- `marca/perfil.json`: `rodape_obrigatorio`.
- `correio/licoes.md` e `devolutiva` da versão anterior, se houver.

`references/design.md`, se existir (método de design do squad), manda no método. Se não existir, siga este arquivo.

## Antes de começar
Se faltar paleta, fonte ou logo em `marca/`, não invente. Chame `kit-marca` para propor um kit mínimo e escreva `erro.txt` ("marca incompleta, aguardando aprovação do kit"). O carteiro leva o pedido de aprovação ao médico.

## Método
1. Formatos:
   - Slides do carrossel: 1080 x 1350.
   - Capa do vídeo: 1080 x 1920 (zona segura: mantenha o texto longe das bordas).
   - Imagem do LinkedIn: 1200 x 627.
2. Texto da arte = texto do conceito aprovado, palavra por palavra. Não reescreva.
3. Cores e fontes só as da marca. Contraste legível (texto claro em fundo escuro ou o contrário; nunca cinza sobre cinza).
4. Consistência: mesma grade, mesmas margens e mesma hierarquia (título, texto, rodapé) em todos os slides.
5. Último slide: logo, `rodape_obrigatorio` e chamada para ação.
6. Fotos: só as de `ativos/fotos/` (do próprio profissional). Nunca foto de paciente, de banco com rosto identificável de paciente, nem "antes e depois".

## Como gerar
Preferência: se o container tiver Python com Pillow, componha o texto por código sobre o fundo (cor sólida, gradiente simples, textura ou imagem gerada **sem texto**), usando as fontes de `marca/ativos/fontes/`. Isso evita erros de português que modelos de imagem cometem ao desenhar texto.
Alternativa: a ferramenta de imagem do Hermes, pedindo só o fundo ou a ilustração, sem texto. Se a ferramenta não tiver acesso (o porteiro só libera o openrouter.ai), escreva `erro.txt` com "ferramenta de imagem sem acesso" e o que precisaria ser liberado. Prefira um modelo de imagem do próprio OpenRouter.
Custo: imagem é a parte mais cara. Gere só o necessário e não refaça slide que já está bom.

## Saída: `arte-v<N>/`
```
slides/slide-01.png ... slide-NN.png
capa-video.png
linkedin.png
legenda-instagram.md   (cópia da aprovada no conceito)
arte.md                (lista de arquivos, formato e observações)
```

## Regras
- Não use imagem, logo, personagem ou ilustração que você não tenha certeza de que pode usar. Nada de marca de terceiros, ícone com direitos reservados ou cópia de arte de referência.
- Nada de dado de paciente, nem de imagem que sugira diagnóstico individual.
- Versão 2 em diante: mude só o que foi apontado e descreva em `mudancas.md`.
- Revise cada imagem antes de entregar: texto cortado, erro de português, contraste, logo no lugar.
