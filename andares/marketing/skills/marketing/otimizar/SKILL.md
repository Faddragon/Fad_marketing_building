---
name: otimizar
description: Autorrevisão do marketing antes de entregar. Confere o conceito ou a arte contra as lições, LGPD, regras de publicidade do conselho do usuário, identificação obrigatória e limites de cada rede, e corrige o que puder. Use no fim das etapas conceito e arte, chamado pelo processar-ficha.
---

# otimizar

> Nesta skill, `marca/` significa `marca/<marca_id>/`, a marca da ficha (`marca_id` em `ficha.json`). Nunca misture arquivos de marcas diferentes.

Você é o revisor da sua própria entrega. O skip também revisa depois, mas você deve entregar o melhor possível e dizer com clareza o que ainda não conseguiu resolver.

## Entrada
Tudo o que foi criado na pasta da versão (`conceito-v<N>/` ou `arte-v<N>/`), `correio/licoes.md`, `marca/perfil.json`, `marca/tom-de-voz.md`, `marca/manifesto.md`.

## Checklist

### 1. Lições
Percorra `licoes.md`. Cada lição é uma regra. Se alguma foi violada, corrija.

### 2. LGPD
- Nenhum dado de paciente (nome, idade que identifique, caso, imagem, exame, depoimento).
- Nenhum caso real contado com detalhes que permitam identificar alguém, nem como "exemplo".
- Nenhuma foto de paciente na arte.

### 3. Publicidade do conselho (conforme `perfil.json`)
Use `regras_conformidade`. Para `cfm`, regras de partida: sem promessa ou garantia de resultado, sem "antes e depois", sem sensacionalismo, sem comparação com colegas ou autopromoção de superioridade, sem divulgação de preço ou promoção, sem estimular consulta por medo, sem recomendação clínica individual. Especialidade só se tiver RQE em `perfil.json`; sem RQE, use "área de atuação".
Para outro conselho, use as regras cadastradas para ele. Se não houver regras cadastradas, avise em `pendencias` e aplique só os itens gerais acima.
Estas são regras de partida; a lista oficial e atual deve ser confirmada pelo médico ou assessor (veja `README.md` do andar).

### 4. Identificação obrigatória
Textos de saúde precisam do `rodape_obrigatorio` onde a rede e o formato permitirem (legenda, último slide, texto do LinkedIn). Confira a presença e se bate com `perfil.json`. Nunca complete credenciais que não estejam lá.

### 5. Limites de cada rede (conferir sempre; as redes mudam)
Valores de partida, a confirmar: legenda do Instagram até 2.200 caracteres; carrossel até 20 slides; post de LinkedIn até 3.000 caracteres. Hashtags conforme a regra atual da rede. Formato de arte: slides 1080 x 1350.

### 6. Coerência
Tom de voz, vocabulário, valores inegociáveis e manifesto. Texto de slides e legenda não podem se contradizer. Fatos têm fonte em `analise.md`.

### 7. Modo arte (só na etapa arte)
Texto dos slides idêntico ao conceito aprovado (sem erro de português nem letra trocada). Cores e fontes só as de `marca/`. Logo e rodapé presentes. Sem texto cortado nas bordas. Sem imagem de paciente.

## Saída: `<pasta da versão>/otimizacao.md`
```
# Otimização
## Corrigido
- (o que foi corrigido, onde, por quê)
## Pendências
- (o que não deu para resolver e por quê; o médico ou o skip precisam ver)
## Conferido
- Lições: ok / n itens
- LGPD: ok
- Publicidade (conselho): ok / pendente
- Identificação: ok
- Limites de rede: ok
```

## Regras
- Corrija diretamente nos arquivos da própria versão. Não toque em versões anteriores.
- Se a correção mudar o sentido, registre em `Corrigido` o antes e o depois.
- Pendência que não pode ser corrigida vai também para `previa.md`, em `Pontos de atenção`.
- Se você achar que a peça inteira viola uma regra (por exemplo, o tema pede promessa de cura), não maquie: marque como pendência grave e escreva `erro.txt`.
