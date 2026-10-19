# Andar marketing (estúdio de criação)

- **Papel:** cria o pacote de conteúdo. Não publica, não fala com o médico.
- **Internet:** não. Só alcança o modelo de IA pelo porteiro de saída (lista branca: openrouter.ai).
- **Lê:** `correio/trabalhos/<id>/` e `marca/<marca_id>/`. **Escreve:** entregas `conceito-vN/` e `arte-vN/`, `avisos.md`, `erro.txt`.
- **LGPD e CFM:** a revisão oficial é do skip. A skill `otimizar` faz só uma conferência de partida antes de entregar.
- **Personalidade e regras:** `SOUL.md`. **Notas do projeto e pontos em aberto:** `NOTAS-DE-PROJETO.md`.

- **Contêiner:** `predio-marketing` (`andares/marketing/compose.yml`), rede `predio_interna` (sem internet), saída só pelo porteiro. Memória em `/opt/predio-dados/marketing`; pastas `correio` e `marca` com escrita; skills e SOUL só leitura.

## Skills (`skills/marketing/`)
| Skill | Para quê |
|---|---|
| processar-ficha | chefe: etapa conceito e etapa arte |
| onboarding | entrada do usuário (perfil, redes, marca, briefing de tribo); uma vez por marca |
| kit-marca | organiza e propõe o kit de marca |
| analisar-pesquisa | ângulo a partir da pesquisa do skip |
| analisar-referencia | estrutura de um post de referência |
| roteiro-carrossel | slides e legenda |
| roteiro-video | roteiro de vídeo curto |
| ganchos-reels | 3 ganchos de reels |
| post-linkedin | texto de LinkedIn |
| otimizar | autorrevisão antes de entregar |
| arte-final | slides, capa de vídeo e imagem de LinkedIn |
| manual-do-predio | papel do marketing no prédio |

## Ordem de chamada
Etapa `conceito`: processar-ficha → analisar-pesquisa → (analisar-referencia) → roteiro-carrossel, roteiro-video, ganchos-reels, post-linkedin → otimizar → previa.md → `pronto`.
Etapa `arte`: processar-ficha → arte-final → otimizar → previa.md → `pronto`.
