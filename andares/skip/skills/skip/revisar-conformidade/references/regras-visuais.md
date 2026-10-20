# Regras visuais (só na arte final)

Vêm das skills image-creator e template-designer do OpenSquad. As medidas valem para uma arte de 1080 px de largura. A paleta, as fontes e o logo da marca estão em `/opt/marca/<marca_id>/` (`paleta.md`, `fontes.md`, `ativos/logo/`), que prevalece sobre este arquivo.

## Bloqueia

| Id | Regra | Como conferir |
| --- | --- | --- |
| VIS-01 | Medida certa: carrossel do Instagram 1080x1440; capa do LinkedIn 1200x1500 ou a medida definida na marca | tamanho do PNG |
| VIS-02 | Fonte mínima: título de capa 58 px, título 43 px, texto 34 px, legenda pequena e rodapé 24 px | `slides.html`, se houver; senão, a olho: texto que não dá para ler no celular bloqueia |
| VIS-03 | Contraste: texto legível sobre o fundo (pelo menos 4,5:1) | cores do `slides.html` ou a olho |
| VIS-04 | Nada de texto cortado, fora da margem (60 px) ou sobreposto | ver cada slide |
| VIS-05 | Erro de português visível na arte | ler cada slide |
| VIS-06 | Cores e fontes da marca; logo ou assinatura no último slide | comparar com `paleta.md`, `fontes.md` e `ativos/logo/` da marca |
| VIS-07 | Imagem gerada por IA que pareça foto clínica real ou paciente real | ver cada imagem |

## Alerta (não bloqueia)

| Id | Sugestão |
| --- | --- |
| VIS-A1 | Mais de 40 palavras num slide |
| VIS-A2 | Contador de slides ("1/8") ocupando espaço de conteúdo |
| VIS-A3 | Primeiro slide sem um gancho claro |
| VIS-A4 | Último slide sem chamada (salvar, compartilhar, seguir) |
| VIS-A5 | Estilo muito diferente das últimas artes aprovadas |
