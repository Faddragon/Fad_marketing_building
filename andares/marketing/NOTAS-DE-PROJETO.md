# Andar do marketing: skills (rascunho 1)

Cada skill é uma pasta com um `SKILL.md`. Só `onboarding` tem arquivos de apoio.

```
skills/
  manual-do-predio/SKILL.md     papel do marketing, regras de partida
  processar-ficha/SKILL.md      chefe: etapa conceito e etapa arte
  onboarding/                   entrada do usuário (SKILL.md, references/blocos.md, briefing-tribo.modelo.md)
  kit-marca/SKILL.md            organiza e propõe o kit de marca
  analisar-pesquisa/SKILL.md    ângulo a partir da pesquisa do skip
  analisar-referencia/SKILL.md  estrutura de um post de referência
  roteiro-carrossel/SKILL.md    slides e legenda
  roteiro-video/SKILL.md        roteiro de vídeo
  ganchos-reels/SKILL.md        3 ganchos de reels
  post-linkedin/SKILL.md        texto de LinkedIn
  otimizar/SKILL.md             autorrevisão (lições, LGPD, conselho, rodapé, redes)
  arte-final/SKILL.md           slides, capa de vídeo e imagem de LinkedIn
marca/                          formato da pasta de marca, uma subpasta por marca (README e exemplos)
```

## Ordem de chamada
Etapa `conceito`: processar-ficha → analisar-pesquisa → (analisar-referencia) → roteiro-carrossel, roteiro-video, ganchos-reels, post-linkedin → otimizar → previa.md → `pronto`.
Etapa `arte`: processar-ficha → arte-final → otimizar → previa.md → `pronto`.
Antes de tudo: a marca da ficha com onboarding completo (`marca/<marca_id>/onboarding-estado.json`).

## Combinados de arquivo (a confirmar com o carteiro do kit)
- Pasta da ficha: `correio/trabalhos/<id>/` com `ficha.json`, `pedido.json`, `pesquisa.md`, `referencia-bruta.md`, `devolutiva-<etapa>-v<N>.md`.
- Entregas: `conceito-v<N>/` e `arte-v<N>/`, cada uma com `previa.md` (ou `arte.md`), `otimizacao.md`, `mudancas.md` (v2+) e o arquivo vazio `pronto`. Erro: `erro.txt`, sem `pronto`. Avisos: `avisos.md`.
- O campo `conceito_aprovado` em `ficha.json` indica qual versão do conceito a etapa arte deve usar.

## Decisões já tomadas
- `marca/` mora dentro do marketing (volume gravável com backup), uma subpasta por marca: `marca/<marca_id>/`.
- O concierge (skip) recolhe as informações do médico e leva ao marketing. O onboarding roda **uma vez por marca**; não se repete, salvo para criar outra marca ou se o médico pedir para mudar um dado.
- Toda ficha e todo pedido têm `marca_id`. Com mais de uma marca, o concierge pergunta sempre a qual produto ou empresa o pedido pertence.

## Pontos em aberto
1. **Skip como ponte** (próximo passo): perguntar a marca, entregar as perguntas do onboarding, receber arquivos e prints, ler links e gravar `referencia-bruta.md`. Exige mudanças no carteiro (chamar o marketing para o onboarding quando não houver ficha) e na expedição.
2. **Arquivos da ficha**: `marca_id`, `conceito_aprovado`, `devolutiva-<etapa>-v<N>.md` e `previa.md` são propostas minhas; conferir com o script do carteiro. As métricas e as lições também precisam ser separadas por marca (`correio/metricas/<marca_id>/`; no livro de lições, uma coluna de marca).
3. **Squad do OpenSquad**: os `.md` entram em `references/squad.md` de cada skill (e `references/design.md` do arte-final).
4. **Regras de publicidade**: a `otimizar` traz regras de partida do CFM; confirmar com a norma vigente. Para outros conselhos, ainda não há regras cadastradas.
5. **Pacote padrão**, horários por rede e revistas preferidas da pesquisa: pendentes do médico.
6. **Teste**: nada foi rodado no Hermes. O primeiro teste é com uma ficha de mentira, só até a etapa conceito.
