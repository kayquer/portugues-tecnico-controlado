# loop-state — goal-cobertura

Estado entre rodadas do loop de `goal-cobertura.md`. Uma linha por rodada.
Atualize **ao fim de cada rodada**, antes de começar a próxima.

## Estado atual

- **Objetivo:** `loops/goal-cobertura.md`
- **Cobertura:** positivo 8/8 ✓ · contra-teste 8/8 ✓ — **matriz fechada**
- **Rodadas:** 6 de 12
- **Suite:** 12 casos
- **Status:** objetivo atingido em 2026-08-02; harness auditado em 2026-08-03
- **Suite:** 12/12, exit 0, 1 `FLAKY` (`caso-01`)
- **Abertos:** (1) contradição sobre `-se` apassivador em `descritivo`; (2) `caso-01` cita PTC-6 em 4/5

## Rodadas

| # | Regra | Caso criado | Resultado |
|---|---|---|---|
| — | — | — | estado inicial: contra-teste 3/8 |
| 1 | PTC-1 | `caso-05-contra-ptc1-sujeito` | verde — sujeito nulo em coordenação e `se` pronominal inerente sobrevivem |
| 2 | PTC-2 | `caso-06-contra-ptc2-gerundio` | verde — gerúndio durativo e relativa restritiva sobrevivem |
| 3 | PTC-3 | `caso-07-contra-ptc3-modal` | **vermelho → corrigido**. Ver abaixo. |
| 4 | PTC-5 | `caso-08-contra-ptc5-adjetivo` | verde após retry — instável, ver abaixo |
| 5 | PTC-7 | `caso-09-contra-ptc7-identificador` | verde — `v1.5` e `3.11` não viram decimal |
| 6 | — | — | matriz fechada; retry adicionado ao runner |

## Achados

### Rodada 3 — o caso estava errado, não a skill

O primeiro `caso-07` usava `Você deve encerrar a sessão em até 30 minutos` em nível `estrito`. A skill reescreveu, e com razão: aquilo é **instrução**, e a PTC-2 exige imperativo (`Encerre`), não `você deve`.

`deve` de obrigação só é contra-teste válido em texto **descritivo**. Caso refeito com `nivel: descritivo` e a modalidade fora de instrução direta. Passou.

É o cenário que o `goal.md` prevê no passo 4 — vermelho pode ser caso errado, não falso positivo. Aqui era caso errado.

### Rodadas 4-6 — a suite oscilava, e esse foi o achado maior

Rodando a suite três vezes seguidas sem mudar nada, **casos diferentes falhavam a cada vez**:

| Rodada | Falhou |
|---|---|
| A | `caso-03` (`solicitamos`, `efetuem`), `caso-07` |
| B | nenhum dos dois — `caso-03` passou 2× seguidas |
| C | `caso-02` (faltou PTC-3), `caso-08` (`chave de API do banco de dados`) |

Sem tratamento, a suite acusaria regressão inexistente toda rodada — e pior, apontaria um culpado diferente a cada vez. Um gate assim é ruído, não verificação.

**Correção:** o runner repete o caso até `PTC_TENTATIVAS` (3) antes de reprovar, e distingue três estados:

- `PASS` — passou de primeira
- `FLAKY` — passou numa retentativa; conta como ok, mas aparece destacado
- `FAIL` — falhou as três; aí é quebra real

### O que o flaky recorrente significa

Flaky não é só ruído de amostragem. Um caso que oscila com frequência aponta para uma de duas coisas:

1. **Asserção frágil** — o termo de `nao-marca` é longo demais e qualquer reformulação legítima o quebra. `chave de API do banco de dados` é exatamente isso: a skill pode reescrever a frase por outro motivo e o trecho literal some sem que a PTC-5 tenha dado falso positivo.
2. **Regra genuinamente ambígua** — o modelo hesita porque a regra não decide o caso. Aí o conserto é no `SKILL.md`, não no teste.

`caso-02` (bilíngue, `should` → PTC-3) e `caso-08` são os candidatos a revisão numa próxima sessão.

## Sessão seguinte — medição do flaky (2026-08-03)

O loop de cobertura fechou apontando `caso-02` e `caso-08` como instáveis. Isso veio de observação única, não de medição. Medindo com `PTC_TENTATIVAS=1`, 5 rodadas cada:

| Caso | Baseline | Depois | Veredito |
|---|---|---|---|
| `caso-02` | **5/5 PASS** | — | **não era flaky.** Acusado por uma falha isolada na rodada C. Nada foi alterado. |
| `caso-08` | 3/5 (1× `apenas um teste`, 1× timeout) | **7/7** | duas causas reais, mais uma terceira que não era da skill |

Suite completa depois dos consertos: **9/9, zero `FLAKY`**. `--cobertura` segue 8/8 e 8/8.

### O que a suspeita registrada acertou e errou

O `loop-state` anterior apostou em `chave de API do banco de dados` como asserção frágil. **Certo, e pelo motivo previsto** — mas o mecanismo só apareceu na saída bruta: a PTC-6 expande `API` na 1ª ocorrência (`chave da Interface de Programação de Aplicações (API) do banco de dados`) e o substring morre. A PTC-5 nem é citada. Encurtado para `do banco de dados`: 5/5.

Ele **errou** ao inocentar `apenas um teste`, que era a falha mais frequente.

### `apenas` — a skill se contradizia

`SKILL.md:112` (PTC-5) prescrevia `apenas um teste` como a forma correta do sentido anteposto. `lexico.md` mandava cortar `apenas` como minimizador. Os dois vão concatenados no mesmo prompt.

Dividir a entrada do léxico em hedge × quantidade levou de 3/5 para 4/5 — **dentro do ruído com n=5, não conta como resolvido.** A contradição era real e o split fica, mas não foi ele que fechou o caso.

A causa restante estava na frase do caso: `Rode apenas um teste para confirmar` é ambígua exatamente na dimensão testada. Lê como quantificador (um teste só) e como minimizador (`é só rodar um teste`), e nenhuma regra da skill pode decidir porque a informação não está na frase. Um contra-teste ambíguo no ponto que ele existe para provar não prova nada.

Entrada passou a `Rode apenas um teste, não a suíte inteira`. **7/7 PASS depois disso**, contra 3/5 antes.

### Terceira causa: o runner mentia

`FAIL` sem `faltou` e sem `corrigiu` era o caminho `saida is None` — timeout ou erro da API. Saía na tela idêntico a uma regressão da skill, e parte da instabilidade que o loop anterior atribuiu à skill era isso. O runner agora nomeia o caso. Não muda o veredito (caso não verificado não é verde), muda o diagnóstico.

### Lição

As três causas de flaky estão tabeladas no `AGENTS.md`. A que não estava lá era a de infra, e era a mais fácil de confundir com quebra real.

## Sessão seguinte — auditoria do próprio harness (2026-08-03)

A matriz estava 8/8 e 8/8 e a suite verde, mas parte desse verde não provava nada. Seis buracos, todos fechados menos um achado que ficou aberto de propósito.

### O verde que não era verde

| Buraco | O que passava |
|---|---|
| `contra-teste:` não era lido por asserção nenhuma | declarar a regra bastava para a matriz contá-la coberta |
| chave com typo era ignorada em silêncio | `espra: PTC-1` → caso `PASS` verificando zero |
| `bilingue: sim` era lido e descartado | `caso-02` só funcionava porque a entrada pedia o par EN/PT em prosa |
| `destinatario` não existia no parser | a flag `agente` do `SKILL.md` nunca foi exercitada |
| contra-teste da PTC-4 só em `leve` | onde a tabela de níveis **dispensa** a regra — testava a tabela, não a regra |
| `range(1, 9)` hardcoded em 4 lugares | uma PTC-9 sairia da matriz sem aviso |

Conserto: validação no `parse_caso` que mata o runner (5 checagens), chave `deve-conter`, `destinatario`/`bilingue` chegando ao prompt, constante `REGRAS`. Casos novos: `caso-10` (PTC-4 em `estrito`), `caso-11` (flag agente), `caso-12` (nível `descritivo`). Suite foi de 9 para 12 casos.

### `deve-conter` — a asserção que faltava

`nao-marca` prova que a skill **não** mexeu. Não havia como provar que ela **fez** algo cujo comportamento não tem número PTC próprio. Os três comportamentos da flag `destinatário: agente` são exatamente isso: pela tabela de violações, `caso-11` é indistinguível de um PTC-1 comum.

### Duas âncoras reprovadas na medição

O protocolo (5× com `PTC_TENTATIVAS=1`, aceita só 5/5) pegou as duas antes de entrarem:

| Âncora | Medição | Diagnóstico |
|---|---|---|
| `agente enviou` sobre `Pacote enviado às 14h30` | 3/5 | com marca de tempo, `envia` e `enviou` são as duas certas — a entrada não diz se é log passado ou comportamento recorrente. Consertado na **entrada** (`ao servidor` força ação em presente): 5/5 |
| `espera: PTC-1` no `caso-11` | 4/5 | a skill conserta sempre, mas etiqueta a linha ora `PTC-1`, ora "Destinatário agente" — os comportamentos da flag não têm número. Asserção sobre etiqueta é moeda ao ar; removida |

`caso-02` ganhou `deve-conter: proposiç` — a tabela de proposições só é emitida no modo bilíngue, então a presença dela prova que o pipeline rodou. 5/5. De quebra confirmou de novo que `caso-02` nunca foi flaky.

### Achado aberto — a skill se contradiz sobre `-se` em `descritivo`

O `caso-12` entrava com `Verifica-se a integridade dos arquivos` em nível `descritivo`. Medido 6×, o trecho sobrevive **2/6**. As três saídas:

| Saída | Vezes |
|---|---|
| `Verifica-se a integridade dos arquivos` *(mantido)* | 2 |
| `A integridade dos arquivos é verificada` *(passiva explícita)* | 2 |
| `o sistema verifica a integridade` *(ator inventado)* | 2 |

Não é asserção frágil. É contradição interna, mesma família do `apenas`:

- **tabela de níveis:** `PTC-1 sem -se passivo` = "ok em descrição sem ator"
- **corpo da PTC-1:** teste mecânico *"se dá para reescrever com é/são + particípio sem mudar o sentido, é o `se` proibido"* — que classifica justamente este `-se` como proibido

Os dois vão concatenados no mesmo prompt. O modelo decide diferente a cada rodada.

**Não foi consertado**, por restrição de escopo: o objetivo da sessão era cobrir o harness, não mudar a skill. `caso-12` ficou com as duas âncoras que se sustentam (`é gerado`, cadeia de `de` de 3 nós) e **não** declara `contra-teste: PTC-1` — não dá para provar PTC-1 enquanto a contradição existir.

**Próxima sessão:** decidir de que lado a contradição se resolve. O teste mecânico do corpo da PTC-1 não tem cláusula de nível; ou ele ganha uma, ou a linha da tabela de níveis sai. A entrada do `caso-12` já está pronta para virar contra-teste de PTC-1 assim que a regra decidir.

### Segundo achado aberto — `caso-01` cita PTC-6 em 4 de 5 rodadas

A suite completa fechou **12/12, exit 0**, com um `FLAKY` no `caso-01` (passou na 2ª de 3). Medido depois com `PTC_TENTATIVAS=1`, 5 rodadas: **4/5**, e a falha é sempre a mesma linha — `faltou: PTC-6`.

O `caso-01` é o mais largo da suite: 8 regras numa entrada só. É também o único caso pré-existente que oscila, e não foi tocado nesta sessão (sem `destinatario` nem `bilingue`, o prompt dele é idêntico ao de antes).

**Não determinado:** se nas rodadas que falham a PTC-6 deixou de ser *aplicada* (`API's` → `APIs`, variante BR) ou apenas de ser *citada* na tabela. As duas hipóteses produzem exatamente esta saída, e a tabela do `AGENTS.md` manda para lugares diferentes:

- se foi aplicada e não citada → colisão de rótulo com a PTC-8, que também parece ortografia. Custo cosmético; o `AGENTS.md:120` já registra que modelo menor às vezes aplica sem citar
- se não foi aplicada → lacuna real, e o conserto é no `SKILL.md`

Resolver pede rodar o caso até falhar e olhar o texto final bruto atrás de `APIs`. Com 4/5, são ~5 chamadas por tentativa de captura.

**Impacto no gate:** nenhum hoje. Com `PTC_TENTATIVAS=3`, 4/5 por tentativa dá ~0,8% de chance de `FAIL`. O caso aparece como `FLAKY`, que é o estado que existe justamente para isso.

### Lição

Um harness também precisa de contra-teste. Cinco dos seis buracos eram do mesmo formato: a asserção existia no arquivo e não existia no código, e nada verificava a distância entre as duas.

O sexto é de outra natureza e apareceu duas vezes nesta sessão (`caso-11`, `caso-01`): **comportamento correto com rótulo instável**. A skill conserta e nomeia a linha de um jeito diferente a cada rodada, e uma asserção sobre `PTC-N` citada mede o rótulo, não a correção. `deve-conter` existe para isso — quando o que importa é a correção, ancore na correção.

## Como retomar

```bash
./init.sh --cobertura   # onde está o gap (não chama o Claude, é instantâneo)
./init.sh               # a suite continua verde?
```

As duas saindo 0 = objetivo atingido. Para reabrir o loop com objetivo novo, escreva outro `goal-*.md` — o de caça a falso positivo adversarial é o próximo candidato natural.
