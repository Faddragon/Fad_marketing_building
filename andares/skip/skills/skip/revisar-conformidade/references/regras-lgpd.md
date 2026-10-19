# Regras LGPD e privacidade (edite com cuidado)

Base: LGPD (Lei 13.709/2018), art. 5º, II (dado de saúde é sensível) e art. 11; CFM 2.454/2026, art. 6º. Regra do prédio: **nenhum dado de paciente entra nem sai**. Todas as regras abaixo **bloqueiam**.

| Id | Regra | Exemplos que bloqueiam |
| --- | --- | --- |
| LGPD-01 | Nenhum nome, iniciais ou apelido de paciente | "a paciente M.S.", "dona Maria" |
| LGPD-02 | Nenhuma combinação que identifique alguém | idade + cidade + diagnóstico; profissão rara + doença; data da cirurgia |
| LGPD-03 | Nenhum documento ou contato | CPF, RG, telefone, e-mail, número de prontuário |
| LGPD-04 | Nenhuma imagem clínica real | foto de exame, laudo, ultrassom, cicatriz, cirurgia, mesmo "anônima" |
| LGPD-05 | Nenhum rosto real que não seja do médico ou da equipe com autorização | foto de paciente, print de conversa, depoimento com foto |
| LGPD-06 | "Caso clínico" só se for inventado, genérico e dito como ilustrativo | "Imagine uma pessoa de 40 anos..." é aceito; "atendi ontem uma..." bloqueia |
| LGPD-07 | Nenhum print de mensagem, comentário ou avaliação com nome de terceiros | print de WhatsApp, comentário com @ |

Na dúvida, bloqueie com `parar` e deixe o médico decidir. Nunca copie o dado suspeito para o parecer: diga só onde está.
