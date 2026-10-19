# marca/: a identidade de cada marca, dentro do marketing

Pasta do Hermes de marketing, gravável (volume do próprio andar, com backup). Cada marca (profissional, empresa ou produto) tem a sua subpasta. As skills `onboarding` e `kit-marca` gravam; as demais só leem.

## Estrutura

```
marca/
  marcas.json                    índice: id, nome, tipo, padrão
  <marca_id>/
    perfil.json                  dados estruturados (entidade, tipo de perfil, identificação, redes, preferências)
    briefing-tribo.md            briefing de tribalização preenchido
    manifesto.md                 manifesto aprovado
    tom-de-voz.md                tom, lema, vocabulário, o que nunca dizer
    paleta.md, fontes.md         resultado do manual ou do kit de marca aprovado
    manual/                      manual de marca enviado (PDF, imagens)
    ativos/
      logo/  fotos/  fontes/     fotos só do próprio profissional, nunca de pacientes
    referencias/                 estruturas de referência salvas a pedido
    kit-proposto/                proposta do kit-marca, até a aprovação
    onboarding-estado.json       progresso do onboarding da marca
```

## Como funciona
1. **Onboarding uma vez por marca.** O concierge (skip) recolhe as respostas e os arquivos do médico e leva ao marketing. O médico não repete nada. Só volta a haver onboarding quando ele quiser criar outra marca, ou pedir expressamente para mudar algum dado.
2. **Todo pedido tem marca.** `pedido.json` e `ficha.json` trazem `marca_id`. Com mais de uma marca, o concierge pergunta sempre a qual produto ou empresa o pedido pertence. Com uma só marca, ela é o padrão.
3. **Nada se mistura.** Paleta, tom, perfil, métricas e lições de uma marca não entram em outra.

## Regras
1. Nenhum dado, caso ou foto de paciente entra aqui. O filtro de LGPD do carteiro barra o que passar.
2. `perfil.json` manda na conformidade: a `otimizar` e a revisão do skip leem `tipo_perfil` e `regras_conformidade`.
3. Fotos só do próprio profissional. Imagem de paciente, inclusive "antes e depois", não entra no kit.
4. Credenciais (chaves de API, tokens, senhas) nunca ficam aqui nem passam pelo Telegram. As redes se conectam por OAuth no Postiz; aqui só se registra o status.
5. Toda alteração relevante vai para o livro de lições.
6. O `processar-ficha` só aceita pedido de uma marca com `onboarding-estado.json` em `completo: true`.

## perfil.json (campos)

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `versao` | número | sim | versão do esquema |
| `atualizado_em` | data ISO | sim | |
| `marca_id` | texto | sim | slug da marca, igual ao nome da pasta |
| `entidade` | objeto | sim | `{nome, tipo}`; `tipo`: `profissional`, `empresa` ou `produto` |
| `tipo_perfil` | `medico` \| `saude_outro` \| `outro_negocio` | sim | define o bloco regulatório |
| `nome_publico` | texto | sim | como aparece nas artes |
| `conselho` | objeto | se saúde | `{sigla, numero, uf}` (CRM, CRO, CRP, CRN...) |
| `regras_conformidade` | texto | sim | `cfm`, sigla de outro conselho ou `nenhuma_especifica` |
| `especialidades` | lista | se médico | cada item: `{nome, rqe}`; RQE obrigatório para anunciar a especialidade |
| `areas_de_atuacao` | lista de texto | não | subespecialidades e focos |
| `formacao_titulos` | lista de texto | não | só o que for comprovável |
| `atuacao` | objeto | sim | `{locais, cidade_regiao, modalidade, convenios, idiomas}` |
| `publico` | objeto | sim | `{atrair, nao_atrair}` em termos gerais, sem casos reais |
| `temas` | objeto | sim | `{pode_divulgar, evitar}` |
| `diferenciais` | lista de texto | não | sem promessa de resultado |
| `redes` | lista | sim | itens: `{rede, usuario, tipo_conta, conectada_postiz, prioridade}` |
| `referencias_admiradas`, `referencias_evitar` | lista de texto | não | |
| `tempo_semanal_aprovacao_min` | número | sim | |
| `marca` | objeto | sim | `{tem_manual, paleta, fontes, tem_logo, tem_fotos_profissionais}` |
| `rodape_obrigatorio` | texto | se saúde | montado do conselho e RQE; a revisão confere |

Ver `perfil.exemplo.json`, `marcas.exemplo.json` e `onboarding-estado.exemplo.json`.
