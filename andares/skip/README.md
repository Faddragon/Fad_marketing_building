# Andar skip (concierge)

- **Papel:** única porta do prédio. Fala com o médico no Telegram, pesquisa na internet, revisa LGPD e CFM, registra as decisões.
- **Internet:** sim, só informação pública. Sem login, sem formulários, sem baixar programas.
- **Contêineres:** skip (Hermes) e, mais adiante, expedição (script sem IA: prévias, Postiz, métricas; ainda não existe).
- **Contêiner:** `predio-skip` (`andares/skip/compose.yml`), rede `predio_externa`. Memória em `/opt/predio-dados/skip`; skills e SOUL montados só leitura.
- **Lê:** `correio/` (marketing, carteiro). **Escreve:** `correio/pesquisas`, `correio/pedidos`, `correio/decisoes`, `correio/avisos`.
- **Personalidade e regras que nunca quebram:** `SOUL.md`.

## Skills (`skills/skip/`)
| Skill | Para quê |
|---|---|
| concierge | roteiro de conversa; decide qual skill usar |
| pesquisar-tema | pesquisa em perfis, revistas e sociedades médicas |
| pedir-pacote | transforma o pedido do médico em ficha para o marketing |
| revisar-conformidade | LGPD, publicidade médica (CFM) e regras visuais |
| decidir | registra aprovar, ajustar ou descartar, com código de 4 dígitos |
| rotina-diaria | pesquisa diária automática e sugestões cedo no Telegram |
| status-e-licoes | onde está cada trabalho; lições aprendidas |
| manual-do-predio | manual do prédio para o skip |
