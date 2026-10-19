# Blocos de perguntas do onboarding

Use como roteiro. Todas as respostas valem para a marca em andamento (`marca_id`). Faça uma pergunta (ou grupo curto) por vez. Todas aceitam "não sei", "depois" e "pular". Campos entre colchetes são o destino em `perfil.json`.

## 0. Qual é a marca
- Para qual produto ou empresa vamos criar conteúdo? Qual o nome? [marcas.json, entidade.nome]
- É você como profissional, uma empresa ou um produto? [entidade.tipo]
- Pergunte sempre, mesmo que já exista outra marca: o conteúdo de uma marca nunca é misturado com o de outra.

## A. Tipo de perfil
- Você é médico, outro profissional de saúde ou outro tipo de negócio? [tipo_perfil]

## B. Identificação profissional e conformidade
Se médico:
- Como quer aparecer nas artes (nome público)? [nome_publico]
- Qual a sua especialidade? Tem subespecialidade ou área de foco? [especialidades, areas_de_atuacao]
- Qual o RQE de cada especialidade? [especialidades[].rqe]
- Qual o seu CRM e a UF? [conselho]
- Formação, títulos e sociedades de que faz parte (só o que pode comprovar). [formacao_titulos]
- Confirma este rodapé? "<nome> | CRM-<UF> <número> | RQE <número>" [rodape_obrigatorio]

Se outro profissional de saúde: conselho (sigla), número, UF, especialidade ou área, formação, rodapé.
Se outro negócio: nome público, área de atuação, formação ou credenciais que quer divulgar.

## C. Onde e como atua; público e posicionamento
- Onde atende (consultório, clínicas, hospitais), cidade e região? [atuacao]
- Presencial, online ou ambos? Particular ou convênios? Idiomas? [atuacao]
- Que perfil de pessoa quer atrair? E qual não quer? (em termos gerais, sem casos reais) [publico]
- Que temas e serviços pode divulgar? Que temas não quer abordar de jeito nenhum? [temas]
- O que você faz de diferente, sem prometer resultado? [diferenciais]
- Quanto tempo por semana tem para aprovar conteúdo? [tempo_semanal_aprovacao_min]

## D. Redes e integrações
Para Instagram, LinkedIn e YouTube: usa? Qual o endereço? Que tipo de conta? Já está conectada ao Postiz? [redes]
- Quais são as redes prioritárias, em ordem? [redes[].prioridade]
- Perfis que você admira e perfis que não quer imitar. [referencias_admiradas, referencias_evitar]
- Orientar: referências entram por link ou print enviado no chat.

## E. Marca
- Você tem manual de marca? Se sim, envie o arquivo. [marca.tem_manual, manual/]
- Quais são as cores da sua marca? [marca.paleta]
- Quais fontes usa? [marca.fontes]
- Tem logo? Envie nas versões que tiver. [marca.tem_logo, ativos/logo/]
- Tem fotos profissionais suas? Envie as melhores. Só fotos suas, nunca de pacientes. [marca.tem_fotos_profissionais, ativos/fotos/]
- Mande 2 ou 3 artes que você gosta (link ou print). [referencias/]
- Sem manual: acionar `kit-marca`.

## F. Tribalização, parte 1 (seções 1 a 3 do briefing)
Seção 1, líder:
- Qual o seu nome/marca e o seu papel? (já sabemos pelo bloco B; só confirme)
- Por que você lidera este tema? Que credibilidade e histórico tem?
- O que você já faz que gera confiança hoje?
- Que recursos já tem (lista, newsletter, redes, eventos)?
- Teste de motivação: faz isso pela tribo ou pelo ganho? O que continuaria fazendo sem crédito? Qual o impacto real se for criticado?

Seção 2, status quo:
- Que regra do seu setor precisa ser desafiada?
- O que "todo mundo sabe" que poderia ser diferente? Quem se beneficia do jeito atual?
- Qual a mudança concreta que quer provocar (1 frase)?
- Como seria o seu nicho em 3 anos se der certo? Que ideia contra a corrente você defende? Por que agir agora?

Seção 3, tribo:
- Nome ou apelido da tribo? Quem são?
- O que une essas pessoas? Em que acreditam? O que querem e ainda não encontraram? Do que têm medo?
- Onde já se reúnem? Que linguagem ou códigos usam?
- Quem são os "buscadores" (nas bordas, sem tribo ainda)? Quem não é da tribo?
- Tribo ampla ou exclusiva? Quantos "verdadeiros fãs" sustentam o projeto?

## G. Tribalização, parte 2 (seções 4 a 6)
Seção 4, fluxos de comunicação (canal atual, desejado e frequência):
- Você → tribo; tribo → você; membro → membro; membro → pessoas de fora.
- Como a tribo já espalha ideias? Que ferramenta é natural para eles? O que impede os membros de se falarem?

Seção 5, manifesto:
- Em que acreditamos (3 a 5 crenças)? Contra o que lutamos? Quem somos?
- Que futuro estamos construindo? O que cada membro pode fazer agora?
- Valores inegociáveis. Frase-mantra. Tom de voz. Formato preferido de publicação.
- Se não souber: gere um rascunho com o que já tem e peça aprovação.

Seção 6, movimento:
- Narrativa em 5 linhas. Mecanismos de conexão. Ações que a tribo pode fazer sem pedir permissão.

## H. Tribalização, parte 3 (seções 7 a 9) — opcional
- Seção 7: as 5 ações do micromovimento (manifesto, conexão com você, conexão entre si, papel do dinheiro, progresso público), com o que fará e o prazo.
- Seção 8: os 6 princípios, com como aplicará cada um.
- Seção 9: nota de 0 a 10 para os 7 elementos de liderança e como vai ouvir a tribo.

## I. Tribalização, parte 4 (seções 10 e 11) — opcional
- Seção 10: ritual recorrente, espaço de conversa, código da tribo, como apresentar membros, desviantes positivos, microlíderes, ferramentas.
- Seção 11: primeiros 10 a 50 integrantes, gesto de generosidade gratuito, como cada membro recruta outro, teste de "vender um", plataforma para a ideia se espalhar.

## J. Tribalização, parte 5 (seções 12 a 15) — opcional
- Seção 12: maior medo, crítica mais temida, impacto real, onde diz "ainda não", concessão que não fará.
- Seção 13: 5 ações para 30 dias (ação, responsável, data, como saberá que funcionou).
- Seção 14: métricas de saúde da tribo e meta de 90 dias.
- Seção 15: o que quer que seja gerado (manifesto, identidade verbal, plano de comunicação, calendário 30/60/90, roteiro de lançamento, estrutura da comunidade, painel, plano de ação).

## Observações de conformidade
- Perguntas de público e diferenciais ficam em termos gerais; nada de caso, dado ou foto de paciente.
- Promessa de resultado, "antes e depois" e preço/promoção não entram em `diferenciais` nem no manifesto (publicidade médica). Se o usuário pedir, explique e proponha alternativa.
- Para `saude_outro`, aplique as regras do conselho informado.
