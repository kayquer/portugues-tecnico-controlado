# AGENTS.md — desenvolvimento da skill PTC

> **PARE.** Se você chegou aqui para **reescrever um texto do usuário**, você está no arquivo errado — leia `SKILL.md` e aplique as regras. Este arquivo é para quem vai **editar a skill em si**.

---

## ⚠️ Este repositório contém português errado de propósito

**Não corrija o português deste repositório.**

Os arquivos abaixo contêm violações deliberadas das próprias regras PTC. Elas são o material de trabalho da skill, não defeitos:

| Arquivo | O que tem de errado de propósito |
|---|---|
| `tests/casos/*.md` | **texto 100% ruim.** É a entrada dos testes. Corrigir aqui faz os testes pararem de testar. |
| `SKILL.md` | os exemplos marcados `❌` — `Faz-se a validação`, `o mesmo`, `micro-serviços`, `1.5 GB`, `um simples teste` |
| `README.md` | os blocos `diff` com linhas `-`, e a seção "O problema" |
| `references/*.md` | as colunas "Evite" e "Errado" das tabelas |

Um agente que "melhora a qualidade do texto" deste repo quebra a skill **em silêncio**: os testes continuam rodando e passam a não detectar nada.

**Regra prática:** neste repositório, texto ruim dentro de exemplo, tabela de "evite→use" ou caso de teste é **conteúdo**. Só mexa nele se a tarefa for explicitamente "adicionar/alterar um caso de teste" ou "corrigir um exemplo que está ensinando a regra errada".

### Como saber em que modo você está

| Sinal | Modo | O que fazer |
|---|---|---|
| O usuário colou um texto e quer ele melhor | **uso** | aplique `SKILL.md` ao texto dele |
| O usuário fala em regra, PTC-N, nível, caso de teste, README, publicar | **desenvolvimento** | siga este arquivo; não reescreva nada do repo |
| Você está prestes a editar `SKILL.md`/`references/`/`tests/` | **desenvolvimento** | sempre |

Na dúvida, pergunte. O custo de perguntar é uma frase; o custo de errar é uma skill que deixou de funcionar sem ninguém perceber.

---

## Definition of done

Uma mudança na skill só está pronta quando **as quatro** valem:

1. `./init.sh` termina verde (exit 0).
2. A mudança tem caso de teste — novo, ou um existente atualizado.
3. Se a mudança criou ou ampliou uma regra, existe entrada em `nao-marca` de algum caso cobrindo o falso positivo correspondente.
4. A regra continua com exemplo antes/depois no `SKILL.md`.

O item 3 é o que mais escapa. Ampliar uma regra quase sempre cria falso positivo, e um caso que só testa o acerto positivo não pega isso. Exemplo real: ampliar a PTC-8 para hifenizar mais prefixos pode fazer a skill "corrigir" `front-end`, que é convenção de estilo e não erro.

## Escopo

**Uma regra PTC por sessão.** Mexer em duas ao mesmo tempo impede saber qual delas quebrou o caso — o runner só diz que a regra não disparou, não por quê.

Se a mudança toca mais de uma regra, quebre em sessões e rode `./init.sh` entre elas.

## Não mexa sem intenção explícita

| Item | Por quê |
|---|---|
| `description` do frontmatter | É o que faz a skill disparar. Alterar muda quando ela é invocada. |
| Numeração `PTC-N` | Os casos de teste referenciam por número. Renumerar quebra todos de uma vez. |
| Tabela de níveis | PTC-1, PTC-7 e PTC-8 são obrigatórias nos três níveis. Relaxar qualquer uma em `leve` desmonta o desenho — ortografia errada não fica menos errada em texto informal. |
| Seção "O que NÃO é erro" (`ortografia-ptbr.md`) | É o que impede a skill de virar corretor que conserta português correto. |

## Verificação

```bash
./init.sh                          # roda tudo
./init.sh caso-01                  # um caso só (match por substring)
./init.sh --cobertura              # matriz regra × (positivo, contra-teste) — não chama o Claude
PTC_MODELO=opus ./init.sh          # modelo diferente
PTC_TENTATIVAS=1 ./init.sh         # sem retry (para medir flakiness)
```

## Loops

`loops/goal-cobertura.md` é um goal loop no formato do [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) (lecture-13). Rode com `/loop` sem intervalo — o modelo se auto-pauta e para no critério do próprio arquivo.

O critério de parada é **mecânico**: `./init.sh --cobertura` sai 0 quando toda regra tem caso positivo e contra-teste. Sem julgamento, sem "acho que já deu".

Estado entre rodadas em `loops/loop-state.md`. Para um objetivo novo, escreva outro `goal-*.md` — cada um precisa de objetivo, verificação executável, condição de parada e restrições.

O runner concatena `SKILL.md` + `references/*.md` **deste repo** e manda para `claude -p`. Ele testa o arquivo que você acabou de editar, não a cópia instalada em `~/.claude/skills/`.

Ele **não compara texto** — output de LLM não é determinístico. Compara o conjunto de regras `PTC-N` citadas na tabela de saída:

- **cobertura** — toda regra de `espera:` apareceu
- **falso positivo** — nenhum termo de `nao-marca:` foi marcado como violação

Regra extra não reprova o caso.

### FLAKY não é PASS silencioso

O runner repete cada caso até `PTC_TENTATIVAS` (3) antes de reprovar, porque a suite oscila: rodando três vezes sem mudar nada, **casos diferentes falhavam a cada rodada**. Sem retry, o gate acusaria regressão inexistente e apontaria um culpado diferente toda vez.

| Estado | Significado |
|---|---|
| `PASS` | passou de primeira |
| `FLAKY` | passou numa retentativa — conta como ok, mas aparece destacado |
| `FAIL` | falhou as 3 tentativas — quebra real |

**Flaky recorrente merece investigação**, não tolerância. Aponta para uma de duas coisas:

1. **Asserção frágil** — o termo em `nao-marca` é longo demais e some por reformulação legítima. `chave de API do banco de dados` é assim: a skill pode reescrever a frase por outro motivo sem que a PTC-5 tenha dado falso positivo. Conserto: encurtar o termo para o núcleo que realmente prova a regra.
2. **Regra ambígua** — o modelo hesita porque a regra não decide o caso. Conserto: no `SKILL.md`, não no teste.

Casos com histórico de instabilidade estão registrados em `loops/loop-state.md`.

### Custo e falso alarme

Cada caso é uma chamada ao Claude; quatro casos por execução. O default é `sonnet` — Opus a cada rodada fica caro, e a asserção é sobre qual regra disparou, não sobre a qualidade da prosa.

**Se um caso falhar, rode com `PTC_MODELO=opus` antes de concluir que a skill quebrou.** Modelo menor às vezes não cita a regra na tabela mesmo tendo aplicado a correção.

## Formato de caso

```markdown
# caso: descrição curta
nivel: estrito
espera: PTC-1, PTC-4, PTC-8
nao-marca: front-end, usuário

## entrada
<texto que viola as regras esperadas>
```

- `nivel` — `estrito`, `descritivo` ou `leve`
- `espera` — regras que **devem** aparecer na tabela de violações
- `nao-marca` — termos que **não podem** ser marcados como violação (pode ficar vazio)

O parser corta a saída antes da seção "mantido de propósito" para checar `nao-marca` — ali a skill cita a regra que *pegaria* o trecho, sem tê-lo corrigido, e isso acusaria falso positivo.

## Clean-state checklist

Antes de encerrar a sessão:

- [ ] `./init.sh` roda e termina verde
- [ ] Cada regra alterada tem caso cobrindo acerto **e** falso positivo
- [ ] Nenhum exemplo `❌` do `SKILL.md`/`README.md` foi "corrigido" por engano
- [ ] `README.md` reflete a mudança, se ela for visível para quem usa
- [ ] Nada pela metade sem registro
- [ ] A próxima sessão consegue continuar sem conserto manual

## Estrutura

```
SKILL.md                  # 8 regras, 3 níveis, processo, formato de saída
references/
  lexico.md               # evite→use, conectores, variante BR, siglas
  ortografia-ptbr.md      # Acordo de 1990, armadilhas de TI, o que não é erro
  ingles.md               # regras STE-EN, pipeline bilíngue, decalques
tests/
  verify.py               # runner (Python 3 stdlib, sem dependências)
  casos/*.md              # casos de regressão
init.sh                   # checa pré-requisitos e roda o verify
```

## Origem das decisões

O desenho — por que 8 regras próprias em vez de traduzir as 53 do ASD-STE100, por que a fonte de verdade é o idioma do input, por que os níveis existem — está em `README.md`, seções "Por que não é o STE traduzido" e "Modo bilíngue". Leia antes de propor mudança estrutural; várias alternativas óbvias já foram descartadas com evidência.
