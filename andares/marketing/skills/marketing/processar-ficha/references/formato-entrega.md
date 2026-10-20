# Formato da entrega

Pasta: `/opt/correio/trabalhos/<id>/<etapa>-v<versão>/`, dentro da pasta da ficha. A versão e a etapa vêm do pedido do carteiro e de `ficha.json` (campos `etapa` e `versao`). O carteiro confere a pasta e leva ao skip para revisão. Mantenha os nomes exatamente assim.

Sempre crie o arquivo vazio `pronto` por último. Sem `pronto`, o carteiro entende que o trabalho não terminou.

## Etapa `conceito`

```
conceito-v1/
  pacote.md          obrigatório (texto de todas as peças pedidas)
  previa.md          obrigatório (resumo de até 3.500 caracteres, ver a skill)
  otimizacao.md      o que a autorrevisão corrigiu
  rascunho-01.png    opcional: esboço simples do 1º slide (e de outros, se ajudar)
  mudancas.md        só da v2 em diante
  pronto             vazio, gravado por último
```

`pacote.md` (só as seções das peças pedidas, com estes títulos):

```markdown
# Pacote 2026-10-19-071500: Nódulo de tireoide: nem todo é câncer
Mensagem central: A maioria dos nódulos é benigna; o importante é saber quando investigar.

## Fontes usadas
- [1] Diretriz ... — SBEM, 2025 — link
- [2] ...

## Carrossel (Instagram)
### Slide 1 (capa)
Título: ...
Apoio: ...
Visual: o que a imagem mostra, em uma linha
### Slide 2
...
### Legenda
texto da legenda...
#hashtags (até 5)
Dr. Francisco ... | CRM ... | RQE ...

## Roteiro de vídeo (Instagram, 60 s)
| Tempo | Fala | Texto na tela | Cena |
| --- | --- | --- | --- |
| 0-3 s | ... | ... | ... |
Legenda: ...

## Ganchos de reels
1. "..." — ideia do reel em uma linha
2. ...
3. ...

## LinkedIn
texto do post...
Rodapé: ...
Capa: o que a imagem mostra, em uma linha

## Pendências
- o que não foi possível resolver, ou "nenhuma"
```

Cada número no texto leva a marca da fonte, `[1]`, **só no pacote**. Na peça final a marca sai e a fonte vai para a legenda, quando couber.

## Etapa `arte`

```
arte-v1/
  post.json                        obrigatório: a expedição usa para agendar
  slide-01.png ... slide-08.png    carrossel, 1080x1440
  slides.html                      fonte dos slides (o skip confere as fontes aqui)
  linkedin-capa.png                se houver post-linkedin
  previa.md                        lista dos arquivos e o que mudou
  otimizacao.md
  mudancas.md                      só da v2 em diante
  pronto
```

`post.json` (só inclua as redes e as peças pedidas; o texto é o do conceito aprovado):

```json
{
  "id": "2026-10-19-071500",
  "instagram": {
    "tipo": "carrossel",
    "legenda": "texto final, com hashtags e rodapé",
    "imagens": ["slide-01.png", "slide-02.png"]
  },
  "linkedin": {
    "tipo": "imagem",
    "texto": "texto final, com rodapé",
    "imagens": ["linkedin-capa.png"]
  },
  "roteiro_video": "copiado do conceito aprovado",
  "ganchos_reels": ["...", "...", "..."]
}
```

Regras do `post.json`: `instagram.tipo` é `imagem` ou `carrossel` (de 1 a 10 imagens, PNG ou JPEG, só o nome do arquivo, sem pasta); legenda de até 2.200 caracteres e até 5 hashtags; `linkedin.texto` não pode ficar vazio. O carteiro acrescenta `marca_id` e `pesquisa` na entrega.
