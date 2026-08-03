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

O item 2 tem piso mecânico: o parser recusa caso que não assere nada (ver "O parser recusa caso inválido"). Antes disso, um typo no nome da chave produzia caso verde que verificava zero.

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
PTC_TIMEOUT=600 ./init.sh          # timeout por chamada (default: 300s)
```

## Loops

`loops/goal-cobertura.md` é um goal loop no formato do [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) (lecture-13). Rode com `/loop` sem intervalo — o modelo se auto-pauta e para no critério do próprio arquivo.

O critério de parada é **mecânico**: `./init.sh --cobertura` sai 0 quando toda regra tem caso positivo e contra-teste. Sem julgamento, sem "acho que já deu".

Estado entre rodadas em `loops/loop-state.md`. Para um objetivo novo, escreva outro `goal-*.md` — cada um precisa de objetivo, verificação executável, condição de parada e restrições.

O runner concatena `SKILL.md` + `references/*.md` **deste repo** e manda para `claude -p`. Ele testa o arquivo que você acabou de editar, não a cópia instalada em `~/.claude/skills/`.

Ele **não compara texto** — output de LLM não é determinístico. Verifica três coisas:

- **cobertura** — toda regra de `espera:` apareceu na tabela de violações
- **falso positivo** — todo termo de `nao-marca:` sobreviveu intacto no texto final
- **âncora** — todo termo de `deve-conter:` apareceu na saída

Regra extra não reprova o caso.

### FLAKY não é PASS silencioso

O runner repete cada caso até `PTC_TENTATIVAS` (3) antes de reprovar, porque a suite oscila: rodando três vezes sem mudar nada, **casos diferentes falhavam a cada rodada**. Sem retry, o gate acusaria regressão inexistente e apontaria um culpado diferente toda vez.

| Estado | Significado |
|---|---|
| `PASS` | passou de primeira |
| `FLAKY` | passou numa retentativa — conta como ok, mas aparece destacado |
| `FAIL` | falhou as 3 tentativas — quebra real |

**Flaky recorrente merece investigação**, não tolerância. Aponta para uma de três coisas — e a linha de detalhe abaixo do `FAIL` diz qual:

| Detalhe impresso | Causa | Conserto |
|---|---|---|
| `corrigiu indevidamente: <termo>` | **asserção frágil** — o termo de `nao-marca` some por reescrita legítima | encurtar o termo para o núcleo que prova a regra |
| `faltou: PTC-N` | **regra ambígua** — o modelo hesita porque a regra não decide o caso | no `SKILL.md`/`references`, **não** no teste |
| `não apareceu: <termo>` | **âncora frágil** — o `deve-conter` fixa uma escolha que a skill não é obrigada a fazer | desambiguar a **entrada**, não encurtar a âncora |
| `sem resposta do modelo` | **infra** — timeout ou erro da API | nenhum; rode de novo |

**Âncora frágil, caso real:** `caso-11` entrava com `Pacote enviado às 14h30` e ancorava `agente enviou` — 3/5. Com marca de tempo, `O agente envia` e `O agente enviou` são as duas corretas, porque a entrada não diz se aquilo é log de evento passado ou comportamento recorrente. Trocado por `ao servidor`, que força a leitura de ação em presente: 5/5. O conserto foi na entrada; encurtar a âncora teria escondido a ambiguidade em vez de removê-la.

**Asserção frágil, caso real:** `caso-08` pedia `chave de API do banco de dados` intacto. A PTC-6 expande `API` na primeira ocorrência — `chave da Interface de Programação de Aplicações (API) do banco de dados` — e o substring literal morre sem que a PTC-5 tenha dado falso positivo algum. Encurtado para `do banco de dados`, que prova a mesma coisa (a cadeia de `de` não foi quebrada) e sobrevive à expansão.

**Regra ambígua, caso real:** `apenas` estava nos dois lados da skill — `SKILL.md` (PTC-5) prescrevia `apenas um teste` como a forma correta do sentido anteposto, e `lexico.md` mandava cortar `apenas` como minimizador. Os dois arquivos vão concatenados no mesmo prompt, então o modelo decidia diferente a cada rodada. A entrada do léxico foi dividida em hedge (`é apenas um bug`, corte) e quantidade (`apenas um teste`, mantenha).

**Infra:** `FAIL` sem `faltou` e sem `corrigiu` significa que nunca houve resposta para avaliar. Continua contando como falha — caso não verificado não é caso verde — mas não é regressão. Suba `PTC_TIMEOUT` se for recorrente.

Casos com histórico de instabilidade estão registrados em `loops/loop-state.md`.

### Custo e falso alarme

Cada caso é **até `PTC_TENTATIVAS` (3) chamadas** ao Claude, e a suite tem 12 casos — 12 chamadas quando tudo passa de primeira, mais uma por retentativa. O default é `sonnet`: Opus a cada rodada fica caro, e a asserção é sobre qual regra disparou, não sobre a qualidade da prosa.

Durante o desenvolvimento, prefira `./init.sh <caso>` e deixe a suite inteira para o fim. `--cobertura` é grátis (não chama a API).

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

| Chave | O que faz |
|---|---|
| `nivel` | `estrito`, `descritivo` ou `leve` |
| `espera` | regras que **devem** aparecer na tabela de violações |
| `nao-marca` | termos que **não podem** ser marcados como violação — checados só no texto final |
| `deve-conter` | termos que **devem** aparecer — checados na saída inteira |
| `contra-teste` | regras que este caso prova não dispararem. Só alimenta `--cobertura` |
| `destinatario` | `agente` ativa a flag do `SKILL.md` sobre `estrito` |
| `bilingue` | `sim` pede o par EN/PT |

O parser corta a saída antes da seção "mantido de propósito" para checar `nao-marca` — ali a skill cita a regra que *pegaria* o trecho, sem tê-lo corrigido, e isso acusaria falso positivo.

`deve-conter` **não** é cortado: o que ele existe para provar — tabela de proposições do modo bilíngue, registro do linter reverso — fica fora do texto reescrito por desenho.

### Quando usar `deve-conter`

Quando o comportamento testado **não tem número PTC próprio** e a asserção por regra citada não o distingue de outro caso. Os três comportamentos da flag `destinatário: agente` são isso: `caso-11` é indistinguível de um PTC-1 comum pela tabela de violações, e só `deve-conter` prova que a flag mudou alguma coisa.

**Âncora se mede, não se chuta.** Rode o caso 5× com `PTC_TENTATIVAS=1` e só aceite âncora 5/5. Uma que passa 3/5 vira `FLAKY` permanente e some no ruído. Ver `loop-state.md` para as duas âncoras que foram reprovadas e por quê.

### O parser recusa caso inválido

`parse_caso` mata o runner em vez de aceitar em silêncio. Um caso que não assere nada é pior que caso nenhum: ele conta como cobertura.

| Erro | Por que é fatal |
|---|---|
| chave desconhecida | `espra: PTC-1` dava `PASS` sem verificar nada |
| `espera`, `nao-marca` e `deve-conter` todos vazios | caso sem asserção |
| `contra-teste` preenchido com `nao-marca` vazio | a matriz contava a regra coberta sem asserção por trás |
| regra fora de `PTC-1..8` | `PTC-9` caía num `.get(..., [])` e sumia |
| `nivel` que não existe | ia para o prompt como nível inventado |

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
loops/
  goal-cobertura.md       # goal loop: matriz regra × (positivo, contra-teste)
  loop-state.md           # estado entre rodadas + achados abertos
init.sh                   # checa pré-requisitos e roda o verify
AGENTS.md                 # este arquivo
```

Só `SKILL.md` e `references/*.md` vão para o prompt. O resto é harness.

## Origem das decisões

O desenho — por que 8 regras próprias em vez de traduzir as 53 do ASD-STE100, por que a fonte de verdade é o idioma do input, por que os níveis existem — está em `README.md`, seções "Por que não é o STE traduzido" e "Modo bilíngue". Leia antes de propor mudança estrutural; várias alternativas óbvias já foram descartadas com evidência.
