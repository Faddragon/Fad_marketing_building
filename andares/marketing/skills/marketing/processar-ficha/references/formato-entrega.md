# Formato da entrega

Pasta: `/opt/correio/rascunhos/<id>/<etapa>-r<rodada>/`. O carteiro move a pasta para `trabalhos/<id>/conceito/` ou `trabalhos/<id>/arte/`, e o skip revisa a partir dela. Mantenha os nomes exatamente assim.

## Etapa `conceito`

```
conceito-r1/
  pacote.md          obrigatório
  rascunho-01.png    opcional: esboço simples do 1º slide (e de outros, se ajudar)
  correcoes.md       só na rodada 2
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
arte-r1/
  post.json
  slide-01.png ... slide-08.png    carrossel, 1080x1440
  slides.html                      fonte dos slides (o skip confere as fontes aqui)
  linkedin-capa.png                se houver post-linkedin
  correcoes.md                     só na rodada 2
  pronto
```

`post.json` (a expedição usa para agendar):

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

Só inclua as redes e as peças pedidas na ficha.
