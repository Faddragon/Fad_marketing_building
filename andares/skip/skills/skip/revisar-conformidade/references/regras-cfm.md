---
name: regras-cfm
description: Boas práticas de publicidade médica do prédio, para revisar conteúdo de Instagram e LinkedIn.
version: 1.1.0
---

# Regras de publicidade médica (CFM)

**Bases:** Resolução CFM 2.336/2023 (publicidade médica) e Resolução CFM 2.454/2026, art. 7º, §3º (uso de IA para fins publicitários segue as normas de publicidade médica). Este arquivo **não é parecer jurídico**. Na dúvida, mande como alerta para o médico.

Algumas regras daqui são **mais rígidas que a norma**, por decisão do prédio. Elas estão marcadas como "casa". Exemplo: a 2.336/2023 permite antes e depois educativo e divulgação de preço, sob condições; o prédio não faz nenhum dos dois de forma automática.

## Princípios
- Conteúdo educativo, baseado em evidência, que ajuda o público a entender e a procurar avaliação médica.
- O médico assina e responde por tudo. O tom é de médico, não de vendedor.

## Bloqueia

| Id | Regra | Exemplos |
| --- | --- | --- |
| CFM-01 | Nenhuma promessa ou garantia de resultado | "cura garantida", "100% eficaz", "resolve de vez" |
| CFM-02 | Nenhum sensacionalismo nem medo exagerado | "o câncer silencioso que vai te matar", "corra antes que seja tarde" |
| CFM-03 | Nenhum antes e depois (casa) | qualquer comparação de imagens de paciente |
| CFM-04 | Nenhum preço, desconto ou promoção (casa) | "consulta por R$...", "condição especial" |
| CFM-05 | Nenhuma superioridade ou comparação com colegas | "o melhor endocrinologista", "único que faz", "diferente dos outros médicos" |
| CFM-06 | Nenhum diagnóstico ou conduta individual a distância | "se você sente isso, tem hipotireoidismo", "tome X mg" |
| CFM-07 | Nenhum título de especialista sem RQE; curso sem residência ou título só com "NÃO ESPECIALISTA" | citar especialidade não registrada |
| CFM-08 | Nenhum nome comercial de medicamento ou equipamento em tom de propaganda | "use a marca X" (o princípio ativo pode, em contexto educativo) |
| CFM-09 | Nenhum depoimento de paciente (casa) | "veja o que a paciente disse" |
| CFM-10 | Nenhuma imagem manipulada para sugerir resultado | foto "melhorada" de pele, corpo ou cicatriz |
| CFM-11 | Nenhuma afirmação clínica sem base na pesquisa | número sem fonte, "estudos mostram" sem estudo |
| CFM-12 | Nenhum chamado para consulta disfarçado de urgência | "agende hoje ou vai piorar" |
| CFM-13 | Rodapé com nome, CRM e RQE (veja abaixo) | legenda ou post sem o rodapé |

## Pode (com cuidado)
- Chamado neutro: "converse com seu médico", "procure um endocrinologista". Convite ao próprio consultório só se o médico pedir, e sempre sóbrio.
- Números com fonte e arredondados com honestidade ("cerca de 9 em cada 10").
- Ilustração ou imagem de banco, com origem citada quando a regra pedir.
- Bastidores e rotina do médico, sem paciente na imagem.
- Opinião do médico marcada como opinião.

## Palavras de alerta (conferir o contexto)
cura, garantido, definitivo, milagre, revolucionário, sem riscos, sem dor, o melhor, único, exclusivo, imperdível, urgente, promoção, antes e depois, emagreça X kg.

## Rodapé obrigatório
Na legenda do Instagram e no fim do LinkedIn, uma linha com nome do médico, CRM e RQE. A linha certa é o campo `rodape_obrigatorio` de `/opt/marca/<marca_id>/perfil.json`. A falta do rodapé **bloqueia** (CFM-13).
