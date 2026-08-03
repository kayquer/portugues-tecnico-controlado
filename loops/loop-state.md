# loop-state — goal-cobertura

Estado entre rodadas do loop de `goal-cobertura.md`. Uma linha por rodada.
Atualize **ao fim de cada rodada**, antes de começar a próxima.

## Estado atual

- **Objetivo:** `loops/goal-cobertura.md`
- **Cobertura:** positivo 8/8 ✓ · contra-teste 8/8 ✓ — **matriz fechada**
- **Rodadas:** 6 de 12
- **Suite:** 9 casos
- **Status:** objetivo atingido em 2026-08-02

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

## Como retomar

```bash
./init.sh --cobertura   # onde está o gap (não chama o Claude, é instantâneo)
./init.sh               # a suite continua verde?
```

As duas saindo 0 = objetivo atingido. Para reabrir o loop com objetivo novo, escreva outro `goal-*.md` — o de caça a falso positivo adversarial é o próximo candidato natural.
