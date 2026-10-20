# Pacote de atualização: Instagram pelo Telegram + correções

Base: o conteúdo atual da pasta do repositório. Copie estas pastas e arquivos por cima, nos mesmos caminhos. Não há nada para apagar.

## O que muda

| Arquivo | Mudança |
| --- | --- |
| `predio` | `instalar` cria também `revisoes`, `propostas` e `config`; `atualizar` refaz o chmod e roda o `instalar` sozinho |
| `andares/skip/compose.yml` | monta `/opt/marca` (só leitura); a conta e as referências agora ficam em `correio/config/` |
| `andares/skip/SOUL.md` | seção Instagram; `config/` editável só pelo dono no Telegram; `metricas/` só leitura |
| `andares/marketing/SOUL.md` | seção Instagram; lê `correio/config/instagram.md` |
| `skills/skip/concierge` (1.3.0) | roteia `estudar-post`, `avaliar-referencias`, `configurar-instagram` |
| `skills/skip/pesquisar-tema` (1.1.0) | lê `correio/config/referencias.md` e as fichas; critério "Variedade" |
| `skills/skip/avaliar-referencias` (novo, 2.0.0) | rodízio de 3 perfis por dia |
| `skills/skip/estudar-post` (novo) | estuda um post enviado pelo dono |
| `skills/skip/configurar-instagram` (novo) | muda conta, referências e ritmo pelo Telegram |
| `skills/skip/revisar-conformidade` (1.1.0) + `regras-cfm.md` + `regras-visuais.md` | a marca vem de `/opt/marca/<marca_id>/` (o caminho antigo `/opt/predio/marca/identidade.md` não existe) |
| `skills/skip/manual-do-predio` (3.1.0) | pastas, skills e comandos reais; avisa o que ainda não existe |

## Depois do upload (na VPS)

```bash
cd /opt/predio && git pull && chmod +x predio && ./predio instalar
./predio reconstruir skip && ./predio reconstruir marketing
./predio auditar
```

## No Telegram do skip

```
minha conta é @SEU_PERFIL, da marca X
adiciona @perfil1 nas referências, carrosséis didáticos
liga a avaliação diária
```
