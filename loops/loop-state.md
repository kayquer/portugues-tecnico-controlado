# loop-state — goal-cobertura

Estado entre rodadas do loop de `goal-cobertura.md`. Uma linha por rodada.
Atualize **ao fim de cada rodada**, antes de começar a próxima.

## Estado atual

- **Objetivo:** `loops/goal-cobertura.md`
- **Cobertura:** positivo 8/8 ✓ · contra-teste 8/8 ✓ — **matriz fechada**
- **Rodadas:** 6 de 12
- **Suite:** 12 casos
- **Status:** objetivo atingido em 2026-08-02; harness auditado e dois achados fechados em 2026-08-03
- **Suite:** 12/12, exit 0, 2 `FLAKY` (`caso-02`, `caso-03`)
- **Abertos:** nenhum achado de regra. Ver "resíduo" ao fim.

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

## Sessão seguinte — os dois achados abertos, fechados (2026-08-03)

A sessão anterior deixou dois achados medidos e não consertados, porque consertar
era mudar a skill e o escopo dela era o harness. Esta sessão fechou os dois.

### 1. `-se` em `descritivo` — resolvido a favor da tabela de níveis

A contradição era entre a tabela (`PTC-1 sem -se passivo` = "ok em descrição sem
ator") e o teste mecânico do corpo da PTC-1, que não tinha cláusula de nível.

Decidido pela tabela, por coerência interna: a linha seguinte dela já libera voz
passiva sem ator em `descritivo`, e proibir `-se` mas permitir `é verificada` não
descreve política nenhuma. O teste mecânico ganhou a cláusula, mais a proibição
explícita de fugir do `-se` inventando ator — que era **uma das três saídas
observadas** (`o sistema verifica`) e a pior das três, porque inventa fato.

`caso-12` passou a declarar `contra-teste: PTC-1` e `Verifica-se` entrou em
`nao-marca`. Medido 5× com `PTC_TENTATIVAS=1`: **5/5**, contra 2/6 antes.

### 2. `caso-01` e a PTC-6 — era rótulo, não lacuna

A sessão anterior não determinou qual das duas hipóteses valia, e as duas
produzem a mesma saída no runner. Rodando 6× e olhando o texto final bruto:

| | Vezes |
|---|---|
| `API's` corrigido para `APIs` no texto final | **6/6** |
| linha citada como `PTC-6` | 4/6 |
| linha citada como `PTC-8 (apóstrofo não marca plural)` | 2/6 |

Hipótese "aplicou e não citou", confirmada. A correção nunca falhou; o rótulo
oscilava entre duas regras que a skill não separava.

E a atração da PTC-8 é legítima — plural de sigla **é** ortografia pela leitura
ingênua. O `SKILL.md` dizia onde a regra mora (PTC-6) e não dizia onde ela **não**
mora. Conserto: a PTC-8 ganhou uma cláusula de fronteira nomeando os três casos
que parecem ortografia e são PTC-6 (plural de sigla, gênero/artigo de sigla,
variante BR).

Medido depois, 11 rodadas com `PTC_TENTATIVAS=1`: **PTC-6 citada 11/11**.

### O que a correção da fronteira custou

Numa das 11 rodadas faltou **PTC-2**, regra que nunca tinha falhado neste caso.
Não voltou nas 6 seguintes, então entra como observação única — a mesma barra que
inocentou o `caso-02`. Mas a hipótese tem mecanismo: `Utilize as API's` era a
linha que carregava PTC-2 (formas verbais misturadas) **e** o plural da sigla, e
mover o rótulo do plural pode ter levado a linha inteira junto.

`caso-01` é o mais largo da suite — 8 regras numa entrada só — e mexer no rótulo
de uma delas mexe na competição por linha da tabela. Se PTC-2 voltar a faltar,
o conserto não é na PTC-2: é quebrar a entrada do `caso-01` em duas.

### Resíduo — dois `FLAKY` na suite completa

`caso-02` e `caso-03` saíram `FLAKY` (passaram na 2ª de 3) na rodada final.
Nenhum dos dois foi tocado nesta sessão. `caso-02` já foi medido 5/5 duas vezes
em sessões anteriores e absolvido as duas; `caso-03` tem histórico de oscilar em
`solicitamos`/`efetuem`. Não medidos aqui — registrar é honesto, chamar de verde
não seria.

### Lição

Os dois achados tinham o mesmo formato e diagnóstico oposto ao esperado. Em
nenhum dos dois a skill estava **errada**: num, ela mandava duas coisas
incompatíveis; no outro, ela acertava e nomeava o acerto de dois jeitos. Nenhum
teste consegue separar isso da saída do runner. Os dois só foram diagnosticados
olhando texto bruto — o `caso-12` medindo qual das três saídas, o `caso-01`
procurando `APIs` no texto final. **Quando um caso oscila, a saída bruta é o
primeiro lugar, não o último.**

## Sessão seguinte — posicionamento, léxico e portabilidade (2026-08-12)

Três mudanças que não vieram de um goal loop: vieram de perguntas sobre o que a
skill parecia ser de fora. Rodadas como três sessões separadas, porque duas delas
tocam regras diferentes e o `AGENTS.md` proíbe misturar.

### A ortografia não pesava no prompt, pesava na vitrine

A suspeita era que a PTC-8 estivesse dominando a skill. Medido: 23 de 274 linhas
do `SKILL.md`, 8%. O `ortografia-ptbr.md` carrega sob demanda e custa zero até a
dúvida aparecer. **O peso estava fora do prompt** — a `description` do frontmatter
abria citando o Acordo de 1990, e o `README.md` dava uma H3 inteira ao hífen. Quem
lia isso via um corretor ortográfico, não uma skill de desambiguação.

Consertado onde o problema estava: `description` reescrita liderando por sujeito
oculto, `-se` e modal; H3 do README rebaixada a parágrafo que diz que a PTC-8 é
higiene. A regra não mudou de status — continua obrigatória nos três níveis.

A tabela do hífen caiu de 9 para 4 linhas. As 5 que saíram viraram uma frase que
**nomeia cada caso com o exemplo canônico** e manda abrir o reference. Nomear é o
que importa: o modelo não carrega um reference cujo conteúdo ele não sabe que
existe. `caso-01` (`não-conformidade`) e `caso-04` (`infra-estrutura`,
`micro-serviços`) cobrem o corte — medidos 4× e 3× sem retry, todos PASS.

### `executar` já se contradizia, e ninguém tinha visto

Ampliando o léxico, a checagem de colisão contra o `SKILL.md` achou um caso
idêntico ao do `apenas`: `SKILL.md` (PTC-4) lista `executar` entre os verbos leves
proibidos, e três linhas de exemplo acima usa `Execute o script` como a resposta
✅. Os dois vão no mesmo prompt. **Não foi introduzido por esta sessão** — estava
lá desde o primeiro commit, e nenhum caso o pegava.

Resolvido pelo mesmo mecanismo do `apenas`: duas linhas no léxico separando o
sentido. `executar` + nominalização é verbo-suporte; `executar` + objeto concreto
é o verbo pleno e fica. `caso-14` tem `Execute o script` em `nao-marca`.

**Regra que sai daqui:** antes de acrescentar palavra ao léxico, procure ela no
`SKILL.md`. Foi o que achou este bug, e é barato — um grep por termo candidato.

### O léxico foi de 29 para 75 linhas, e o que ficou de fora importa

Três tabelas novas: burocratês, gíria de plantão, falsos amigos do inglês.

Uns oito candidatos foram **recusados de propósito**: `oportunamente`, `em tempo
hábil`, `o quanto antes`, `diversos`, `salvo engano`, `se possível`. Todos são
hedge ou quantificador vago — território da PTC-3. Botá-los no léxico criaria
exatamente a colisão de rótulo que custou uma sessão no `caso-01`: a correção sai
certa e a linha vem etiquetada com a outra regra, e o runner não sabe separar.
**Léxico só recebe o que é ambiguidade lexical**, não o que já tem regra.

A âncora do `caso-13` é `requisito` porque `requerimento` é o único termo novo com
alvo único — `escalar`, `checar` e `logar` têm dois alvos legítimos cada, e âncora
sobre escolha livre vira FLAKY permanente. Medida 5/5 com `PTC_TENTATIVAS=1`.

O `caso-14` também saiu 5/5. Ele é o que paga o item 3 do definition of done:
`suporta 500 conexões`, `Atualmente`, `Execute o script` e `dados sensíveis` são
os quatro sentidos legítimos das palavras que as linhas novas proíbem no outro
sentido. Ampliar léxico sem esse caso teria sido ampliar sem rede.

### Suite

14/14, **zero FLAKY**. A rodada anterior a estas mudanças deu 12/12 com `caso-02` e
`caso-03` instáveis — os dois que este arquivo já registrava como resíduo. Os dois
passaram de primeira agora. Uma rodada não absolve instabilidade conhecida, mas
registrar a melhora é mais honesto que repetir o aviso antigo sem medir.

### Versões portáteis

`tools/build.py` gera cinco bundles e a página de instalação a partir de
`SKILL.md` + `references/`. Três coisas que só apareceram construindo:

- **A reescrita de caminho não pode ser cega.** No compacto, `ortografia-ptbr.md`
  e `ingles.md` não entram. Mandar o texto para "a seção X" seria apontar para
  seção ausente — pior que o caminho quebrado. Reference que entrou vira seção;
  reference que ficou de fora aponta para a versão completa.
- **Substituir caminho por artigo gera "estão em a seção".** Numa skill de
  português controlado essa é a pior vitrine possível. O build contrai.
- **O bundle do AGENTS.md não pode se chamar `AGENTS.md`.** Codex e opencode leem
  AGENTS.md aninhado; um dentro de `dist/` mandaria o agente reescrever este repo
  em português controlado, que é o oposto do que o `AGENTS.md` da raiz manda.
  Chama-se `ptc-agents.md`; o `curl -o AGENTS.md` resolve no destino.

O compacto ficou em 21 KB, não nos ~7 KB pretendidos: o corpo das 8 regras é o
piso sem reescrever a skill à mão, e uma terceira versão escrita à mão desviaria
da fonte no primeiro commit. A página não promete que cabe em qualquer campo.

### Lição

Duas das três perguntas desta sessão eram sobre **percepção**, não sobre
comportamento — e as duas tinham a resposta fora do arquivo que parecia culpado. A
ortografia não pesava no prompt, pesava na `description`. O léxico não era pequeno
por descuido, era pequeno por escopo. **Medir antes de mexer separou o conserto
real da reação ao sintoma** nos dois casos.

## Como retomar

```bash
./init.sh --cobertura                # onde está o gap (não chama o Claude, é instantâneo)
python3 tools/build.py --verificar   # dist/ e docs/ em dia (também grátis)
./init.sh                            # a suite continua verde?
```

As duas saindo 0 = objetivo atingido. Para reabrir o loop com objetivo novo, escreva outro `goal-*.md` — o de caça a falso positivo adversarial é o próximo candidato natural.
