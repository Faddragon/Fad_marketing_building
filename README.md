# Prédio Hermes FAD

Cada **andar** é uma função e tem o seu próprio Hermes, em contêiner isolado. Tudo o que um andar precisa fica dentro da pasta dele em `andares/`.

| Andar | Função | Internet | Pasta |
|---|---|---|---|
| skip | Concierge: conversa com o médico no Telegram, pesquisa, revisa LGPD e CFM, registra decisões | Sim (única porta do prédio) | `andares/skip` |
| marketing | Cria o pacote de conteúdo (carrossel, roteiros, ganchos, LinkedIn, arte) | Não (só o modelo de IA, pelo porteiro) | `andares/marketing` |

## Regras de organização
1. Um andar = uma pasta em `andares/<nome>/` com `README.md`, `SOUL.md` e `skills/<nome>/`.
2. As skills do andar ficam todas em `andares/<nome>/skills/<nome>/<skill>/SKILL.md`. O Hermes lê essas skills **só para leitura**. Quem muda é você, pelo GitHub.
3. O que o agente aprende vai para o livro de lições (`correio/licoes.md`), nunca para dentro das skills.
4. A memória de cada Hermes (`dados/`), os segredos e os dados do médico (`marca/`, correio) **não** vão para o GitHub.
5. LGPD e CFM moram só no skip (`revisar-conformidade`). Os outros andares não guardam cópia dessas regras.
6. Nome de skill sem acento e único dentro do andar. Uma skill cita outra pelo nome, nunca pelo caminho.
7. Andar novo: copie `andares/_modelo`, troque `NOME-DO-ANDAR` e preencha o README.
