---
name: kit-marca
description: Propõe um kit de marca mínimo (2 cores, 2 fontes, logo simples de texto) quando o médico não tem manual, paleta, fontes ou logo, e organiza os arquivos de marca recebidos em marca/. Use quando o onboarding registrar lacuna de marca ou quando o arte-final não encontrar paleta, fonte ou logo.
---

# kit-marca

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

## Quando agir
- O onboarding (bloco E) registrou `marca.tem_manual`, `paleta`, `fontes` ou `tem_logo` como ausentes.
- O `arte-final` não achou paleta, fonte ou logo.
- O médico enviou materiais novos de marca (arquivos em `correio/onboarding/` ou `marca/manual/`) e é preciso organizá-los.

## 1. Organizar o que já existe
- Leia `marca/manual/` e `marca/ativos/`. Extraia do manual: cores (hex), fontes, usos do logo, tom, o que não fazer.
- Escreva `marca/paleta.md` (cores em hex e onde usar cada uma), `marca/fontes.md` (nomes, pesos, quando usar) e atualize `perfil.json` > `marca`.
- Se algo estiver ilegível ou ambíguo (print de baixa qualidade, fonte sem nome), registre como lacuna.

## 2. Propor o kit mínimo (o que faltar)
Entregue uma proposta, nunca um fato consumado. Escreva `marca/kit-proposto/proposta.md`:
```
# Kit de marca proposto
## Paleta (2 cores + neutros)
- Cor principal: #XXXXXX (uso: títulos, destaques)
- Cor de apoio: #XXXXXX (uso: fundos, detalhes)
- Neutros: fundo claro #XXXXXX, texto escuro #XXXXXX
- Razão da escolha: (coerente com tom de voz e especialidade; contraste legível)
## Fontes (2, gratuitas e de licença livre)
- Títulos: <nome> (peso)
- Texto: <nome> (peso)
## Logo simples
- Versão de texto: nome público em fonte de título, com a especialidade abaixo em menor tamanho
- Arquivo: marca/kit-proposto/logo-texto.svg
## Estilo
- Margens, hierarquia, uso de ícones e fotos (só do profissional)
## O que falta do médico
- Logo próprio, fotos profissionais, cores que ele já usa
```
- Escolha cores com contraste legível (texto sobre fundo, mínimo de contraste razoável para leitura em celular). Evite cores berrantes e combinações que pareçam alarme ou promoção.
- Fontes de licença livre, fáceis de instalar. Se não puder garantir a licença, não proponha.
- O logo de texto é só o nome do médico em fonte; não desenhe símbolo com direitos duvidosos nem copie logo de terceiros.
- Gere uma amostra visual (`kit-proposto/amostra.png`) se a ferramenta de imagem ou o Pillow estiverem disponíveis, mostrando um slide-modelo.

## 3. Aprovação
Grave a proposta como rascunho com `origem: "kit-marca"` para o fluxo de aprovação com código de 4 dígitos. Só depois da aprovação:
1. Copie para `marca/paleta.md`, `marca/fontes.md` e `marca/ativos/` (fontes e logo).
2. Atualize `perfil.json` > `marca` (`paleta`, `fontes`, `tem_logo: true`, e `kit: "minimo-aprovado"`).
3. Registre no livro de lições (via aviso ao carteiro): kit de marca definido.

## Regras
- Não registre como "marca do médico" nada que ele não aprovou.
- Se o médico depois enviar o manual real, o kit mínimo é substituído; guarde o antigo em `marca/kit-proposto/anterior/`.
- Nada de fotos de paciente. Fotos só do próprio profissional.
