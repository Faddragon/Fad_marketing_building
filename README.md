# Prédio Hermes FAD

Um conjunto de agentes Hermes, cada um num **andar** (contêiner Docker isolado) com uma função só. Este repositório é a planta do prédio: o que cada andar é, o que pode acessar e como ligá-lo. Os dados privados (memória dos agentes, chaves, conversas, marca do médico) **não ficam aqui**.

## Os andares

| Andar | Função | Internet | Fala com o médico? |
|---|---|---|---|
| `skip` | Concierge: pesquisa, revisa LGPD e CFM, registra decisões | Sim | Sim (Telegram) |
| `marketing` | Cria carrossel, roteiros, ganchos, LinkedIn e arte | **Não**; só o modelo de IA, pelo porteiro | Não |
| `porteiro` | Proxy de saída com lista branca | Só o que está em `filtro.txt` | Não |

```
 médico <-Telegram-> [ skip ]                     internet
                        |  correio (pastas)           ^
                        v                             |
                    [ marketing ] --proxy--> [ porteiro ] --só openrouter.ai--> modelo de IA
        rede predio_externa: skip, porteiro    rede predio_interna (sem internet): marketing, porteiro
```

## Onde fica cada coisa na VPS

| Pasta | O que é | Vai para o GitHub? |
|---|---|---|
| `/opt/predio` | Este repositório (planta, skills, SOULs, composes). Os Hermes só **leem** daqui | Sim |
| `/opt/predio-dados` | Tudo que muda e é privado: `skip/` e `marketing/` (memória dos Hermes), `correio/` (troca entre andares), `marca/`, `segredos/` | **Não** |

Para backup, basta copiar `/opt/predio-dados`. Para reconstruir o prédio, basta clonar este repositório de novo.

## Estrutura do repositório

```
predio                 painel de controle (./predio ajuda)
andares/
  <andar>/
    README.md          papel, internet, pastas que lê e escreve, lista de skills
    SOUL.md            personalidade e regras que nunca quebram (somente leitura para o agente)
    compose.yml        como o contêiner é montado, comentado
    skills/<andar>/    as skills do andar (somente leitura para o agente)
  porteiro/            Dockerfile, tinyproxy.conf, filtro.txt (a lista branca)
  _modelo/             esqueleto para criar um andar novo
docs/MIGRACAO.md       como trazer os Hermes que já existem para este desenho
```

## Como conferir tudo (para quem for avaliar)

```bash
cd /opt/predio
./predio status     # andares, se estão no ar, se têm internet
./predio auditar    # para cada contêiner: imagem, usuário, redes, montagens (escrita ou só leitura),
                    # nomes das variáveis (nunca os valores) e alertas das regras abaixo
```

O `auditar` dá **alerta** se: um contêiner for privilegiado; houver porta publicada no servidor; um andar marcado "sem internet" estiver numa rede que não é interna; ou as skills de um Hermes estiverem com escrita.

## Regras do prédio
1. Um andar = uma função = uma pasta em `andares/` = um contêiner `predio-<andar>`.
2. Skills e SOUL são **só leitura** para o agente. Quem muda é o dono, pelo GitHub, e depois `./predio atualizar` e `./predio reconstruir <andar>`.
3. O que o agente aprende vai para o livro de lições (`correio/licoes.md`), nunca para dentro das skills.
4. Dados e segredos ficam em `/opt/predio-dados`. O `.gitignore` é uma segunda trava.
5. LGPD e CFM moram só no skip (`revisar-conformidade`). Os outros andares não guardam cópia dessas regras.
6. Só o skip tem internet livre; o marketing alcança apenas o modelo de IA, pelo porteiro.
7. Nome de skill sem acento e único dentro do andar. Uma skill cita outra pelo nome, nunca pelo caminho.
8. Andar novo: copie `andares/_modelo`, troque `NOME-DO-ANDAR`, preencha o README e inclua o nome na lista `ANDARES` do `predio`.

## Estado atual
Montagem **ainda não testada na VPS**. Pontos a conferir na primeira subida estão em `docs/MIGRACAO.md`.
