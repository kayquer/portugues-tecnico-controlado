# loop-state

Estado entre rodadas dos goal loops. Atualize **ao fim de cada rodada**, antes de
começar a próxima. As seções estão em ordem cronológica; a última é a atual.

## Estado atual

- **Objetivo aberto:** `loops/goal-falso-positivo.md` — contra-teste adversarial
- **Adversarial:** 5/8 após as rodadas 1-5 (PTC-4, PTC-2, PTC-3, PTC-7, PTC-8) —
  faltam PTC-1, PTC-5, PTC-6
- **Objetivo fechado:** `loops/goal-cobertura.md` — positivo 8/8 ✓ · contra-teste 8/8 ✓ em 2026-08-02
- **Suite:** 19 casos (2026-08-16)
- **Legibilidade:** 4ª asserção. Limiares calibrados: `caso-01` `flesch-min: 50`,
  `caso-11` `flesch-min: 68`, `caso-13` `pal-frase-max: 12` (este em observação —
  margem 1,3 contra espalhamento de 6,1). `caso-03` e `caso-12` foram reprovados
  na medição; o `pal-frase-max: 11` original do `caso-01` falhava ~28% e saiu.
- **Abertos:** um achado **de harness**, não de regra — `FLAKY` não imprime motivo,
  então soluço de API e falha de asserção saem idênticos. Conserto proposto na
  seção do `caso-14`. Nenhum achado de regra aberto.

## Rodadas — goal-cobertura

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

## Sessão seguinte — harness do loop adversarial (2026-08-14)

Sem rodada de loop: só o gate e o roteamento de modelo que o
`goal-falso-positivo.md` precisa para existir. Nenhum caso novo, nenhuma regra
tocada.

### O gate não podia contar contra-teste antigo

A matriz está 8/8 e 8/8, então "tem contra-teste" já não distingue nada. Pior:
PTC-6 tem 4 contra-testes e sairia "pronta" sem uma linha adversarial. O critério
mecânico passou a ser **origem do caso**, marcada no nome do arquivo
(`caso-adv-*`) — zero mudança no parser, e `PTC_ADVERSARIAL=1` filtra a coluna.

Estado inicial: **0/8 adversarial** contra 8/8 contra-teste na mesma árvore. As
duas saírem diferentes é a verificação do filtro; iguais significaria gate que
não gateia.

### `ESCALOU` — o passo manual que virava achado inventado

O `AGENTS.md` mandava rodar com opus antes de concluir quebra da skill, porque
modelo menor às vezes aplica a correção e não cita a regra. Era passo manual, e
esquecê-lo custa mais neste loop que nos anteriores: aqui um `FAIL` de rótulo
vira **achado de falso positivo registrado neste arquivo**, ou seja, ruído com
cara de evidência.

Automatizado como estado próprio, não como retentativa silenciosa — mesma razão
do `FLAKY`. Só escala depois das 3 tentativas e **só se houve resposta para
avaliar**: escalar depois de timeout gasta o modelo caro em nada.

Custo em rodada verde: zero. Só toca opus no que já falhou três vezes.

### Haiku não entrou como default

`PTC_MODELO=haiku` sempre funcionou sem código. Medido de passagem: haiku passou
o `caso-01` inteiro (8/8 regras, 1ª tentativa). Um caso não é medição, e o risco
não é prosa pior — é modelo menor **citar menos regra na tabela**, que é
exatamente o que `avaliar()` lê. Fica como possibilidade medida pela metade.

### O harness ganhou check próprio

`ESCALOU` é um branch que **nenhum caso de teste alcança**: reproduzi-lo de
verdade depende do modelo menor falhar, que é o que não se controla — a tentativa
com haiku no `caso-01` saiu PASS. A decisão saiu de dentro do `main` para
`veredito()`, e `tests/test_runner.py` a exercita com `rodar` dublado. 7 checks,
grátis, rodando no `./init.sh` junto do `build.py --verificar`.

Os dois branches novos foram verificados por mutação — escalar depois de timeout
e filtro adversarial inerte, ambos pegos. Check que não falha quando o código
quebra não verifica nada, e este repo já gastou uma sessão inteira nessa lição.

## Sessão seguinte — a 4ª asserção: legibilidade medida (2026-08-16)

O harness verificava **qual regra disparou** e **quais termos sobreviveram**, nunca
o texto. O `AGENTS.md` admitia isso numa frase ("a asserção é sobre qual regra
disparou, não sobre a qualidade da prosa"). Demonstrado em vez de suposto: uma
saída forjada com a tabela citando as 8 regras e o texto final
`banana front-end banana usuário banana` **passa** no `caso-01` de hoje. Com
`flesch-min: 55`, reprova.

### A fórmula é nossa porque o textstat não tem português

`LANG_CONFIGS` do textstat 0.7.12 tem `en, de, es, fr, it, nl, pl, ru, hu`.
`set_lang("pt_BR")` **não levanta erro** — cai nas constantes do inglês, e
`flesch_reading_ease` devolve número calibrado para inglês sobre texto português.
Do textstat só se usa o que vale em PT: `syllable_count` (via Pyphen, que tem
`hyph_pt_BR.dic`), `lexicon_count`, `sentence_count`. A fórmula é o Flesch
adaptado ao PT-BR de Martins et al. 1996 (USP São Carlos), em
`tests/legibilidade.py`.

Primeira dependência do repo. A skill continua Markdown puro.

### Duas armadilhas de contagem, uma específica deste repo

`count_sentences` racha em **qualquer** `.`: `1.5 GB` vira duas frases. Aqui isso
é grave porque a PTC-7 troca `1.5` por `1,5` — entrada e texto final sairiam com
contagens diferentes por um motivo que não é legibilidade. `normaliza()` neutraliza
`(?<=\d)\.(?=\d)` **dos dois lados**; `teste_decimal_nao_racha_frase` trava isso.

A segunda: fragmento de ≤2 palavras é descartado e o retorno é `max(1, ...)`, então
a guarda de divisão por zero é sobre palavras, não frases.

### A faixa do `flesch-min` era `[0, 100]` e estava errada

Pego por `teste_gate_metrica_reprova_e_aprova`, que testa um **par** — o gate
reprova texto ruim *e* aprova texto bom. Só a primeira metade teria ficado verde
com a faixa quebrada. Medido: burocratês 35, `caso-01` cru 52, reescrita PTC boa
acima de 100, período único de palavras longas −79. A escala de Martins é nominal
e transborda nas duas pontas; o teto real da fórmula é 163,22. Faixa corrigida
para `[-100, 160]`, com os números no comentário para ninguém "consertar" de volta.

### Calibração — 25 medições, e 2 dos 3 palpites caíram

`--metricas` 5× nos 5 candidatos. O palpite escrito no plano era 01, 03, 13.

| Caso | flesch do texto final, 5 rodadas | pior | entrada | resultado |
|---|---|---|---|---|
| 01 | 55,9 · 63,3 · 66,3 · 60,8 · 67,0 | 55,9 | 51,6 | `pal-frase-max: 11` |
| 03 | 32,9 · 37,6 · 37,6 · 32,9 · 32,9 | 32,9 | 35,3 | **sem limiar** |
| 11 | 73,2 nas cinco | 73,2 | 52,0 | `flesch-min: 68` |
| 12 | — · 72,3 · 72,3 · 72,3 · 72,3 | 72,3 | 72,3 | **sem limiar** |
| 13 | 80,3 · 76,4 · 71,5 · 79,0 · 74,1 | 71,5 | 73,5 | `pal-frase-max: 12` |

**`caso-03` reprovado:** nível `leve`, o flesch *cai* em 3 de 5 rodadas e
palavras/frase fica 9,0 nas cinco — idêntico à entrada. A métrica não se move;
um limiar aqui asseraria a entrada.

**`caso-12` reprovado:** a saída é numericamente igual à entrada em 4 rodadas, e a
rodada 1 **não produziu seção "Texto final"**. Um limiar teria dado FAIL 1/5 por
formato, não por legibilidade — é para isso que a regra dos 5/5 existe.

**`caso-11` foi o inverso do previsto:** texto curto, previsão de ruído, e deu
variância **zero** — 73,2 nas cinco, 21 pontos acima da entrada.

Onde o limiar entrou em `pal-frase-max`, foi porque lá ele assere *melhora*: no
`caso-01` a entrada tem 13,1 palavras/frase e o teto é 11, então uma saída que não
mexesse no texto reprovaria. `flesch-min` calibrado costuma cair **abaixo** da
entrada e vale como piso contra reescrita inchada, não como prova de melhora.

### O que a métrica não vê

Repetição — "O operador deve" 6× no `caso-01` é prosa robótica e o Flesch
**premia** isso. Fidelidade — o modelo completou um objeto elíptico com
"o andamento da restauração" e declarou em "Mantido de propósito"; nenhum número
confere se a inferência estava certa. Ela é piso contra inchaço, não juiz de
qualidade. Estilo e fidelidade continuam por conta de `nao-marca` com termo
concreto.

### Falha de métrica não escala

`ESCALOU` significa colisão de rótulo. Texto difícil de ler não é isso, e o opus
reescrever melhor não desmente regressão nenhuma. O guard é
`escalavel = [f for f in falhas if f[0] != "métrica"]` em `veredito()`, com o par
`teste_metrica_nao_escala` / `teste_metrica_escala_com_rotulo` provando que ele
filtra por rótulo, não por "o caso tem métrica".

## Rodadas — goal-falso-positivo

### Rodada 1 — PTC-4, `executar` com objeto concreto (2026-08-16)

Adversarial 0/8 → **1/8**. `caso-adv-4-executar-objeto-concreto.md`, verde de
primeira, sem medição extra.

A escolha não foi pela ordem da matriz e sim por lacuna: `lexico.md:40-41` decide
que `executar a validação` é verbo-suporte e `execute o script` é verbo pleno —
distinção que saiu do conserto da contradição do `executar` (de05802) e ficou
**sem asserção nenhuma atrás**, duas linhas de tabela em prosa. O `caso-10` cobre
nominalização como *sujeito*; ninguém cobria o gatilho superficial literal da
regra, que é verbo leve + substantivo.

Entrada: três `executar` com objeto concreto (`script`, `testes`, `script`).
Descartei `plano de reversão` de propósito — ali `reversão` **é** nominalização e
a linha ficaria discutível em vez de decisiva.

Sem achado na skill. A PTC-4 respeitou a fronteira nas duas leituras.

**Mas a rodada achou um bug no harness**, e o modo de falha é o interessante:
`teste_filtro_adversarial` afirmava `codigo_on == (0 if adv else 1)` — ou seja,
"existe ao menos um `caso-adv` ⇒ a matriz adversarial está fechada". Isso só vale
com as 8 regras cobertas. Enquanto `caso-adv-*` não existia, o ramo `0 if adv`
era **código morto**: a asserção nunca tinha rodado nesse lado. O primeiro caso
adversarial da história do repo derrubou a suite inteira sem nenhuma regressão
real.

Consertado para a invariante certa — a matriz fecha quando **todas** as 8 regras
têm `caso-adv-*` declarando-as em `contra-teste`:

```python
regras_adv = {r for c in casos if c.stem.startswith(verify.PREFIXO_ADV)
              for r in verify.parse_caso(c)["contra_teste"]}
fechada = len(regras_adv) == len(verify.REGRAS)
assert codigo_on == (0 if fechada else 1), (codigo_on, sorted(regras_adv))
```

Verificado por mutação: forçando `cobertura()` a devolver 0 com só a PTC-4
coberta, a asserção recusa. A versão nova é **mais estrita** que a antiga, não
mais frouxa — ela falha num estado que a antiga nem alcançava.

Lição, que é a mesma do `goal-cobertura`: check escrito para um estado futuro
não é check, é intenção. Ele só vira verificação na primeira vez que o estado
chega — e é aí que ele cobra a fatura, no meio de outra tarefa.

### Rodada 2 — PTC-2, relativa restritiva longa (2026-08-16)

Adversarial 1/8 → **2/8**. `caso-adv-2-relativa-restritiva-longa.md`, verde de
primeira. Sem achado.

O `caso-06` já era contra-teste da PTC-2, mas com relativa de duas palavras
(`que falharam`) — curta demais para tentar alguém a cortar. O adversarial usa
uma restritiva de dez palavras: quanto mais longa, mais ela *parece* aposto e
mais convida à vírgula. E a vírgula ali não é estilo — `arquivos que o operador
enviou` são alguns arquivos, `arquivos, que o operador enviou,` são todos.

**A âncora foi escolhida para morrer no erro certo.** `nao-marca` é
`arquivos que o operador`, não `que o operador enviou`: a segunda sobreviveria
intacta à inserção da vírgula, que é exatamente o falso positivo procurado.
Âncora que sobrevive ao erro que ela deveria pegar é âncora inerte — mesma
família do check morto da rodada 1.

Descartei entrada com `enquanto`: duas proposições numa frase fazem a PTC-2
dividir com razão, e a asserção viraria moeda ao ar em vez de decidir.

### Rodada 3 — PTC-3, `talvez` prescrito × "zero hedge" (2026-08-16)

Adversarial 2/8 → **3/8**. `caso-adv-3-talvez-e-pode-permissao.md`, **5/5** com
`PTC_TENTATIVAS=1`. Sem achado — mas o alvo era outro tipo de coisa.

Este caso não foi atrás de um terreno da regra e sim de uma **contradição interna
suspeita**, com a mesma assinatura do achado do `apenas`:

```
SKILL.md:95   "Zero hedge."
SKILL.md:93   probabilidade: proibido usar modal — dê número ou escreva `talvez`
```

`talvez` prescrito numa linha, condenado na outra, e as duas concatenadas no mesmo
prompt. O `apenas` ficou invisível meses exatamente assim, e só apareceu porque o
modelo decidia diferente a cada rodada — foi por isso que aqui um PASS de primeira
não bastou.

**Resultado: a contradição é textual mas não está mordendo.** 5/5 preservou
`talvez`. Isso não é motivo para reescrever nada no `SKILL.md` — a divisão que o
`apenas` recebeu (`lexico.md:38-39`) foi paga por evidência de oscilação, e aqui
não há. O valor da rodada é que agora **existe asserção atrás da linha**: se uma
edição futura pender a balança, o caso pega. Antes, nada pegava.

Se a skill cortasse `talvez`, as duas saídas seriam achado: trocar por modal viola
a própria célula que proíbe modal para probabilidade, e inventar número inventa
fato. Por isso a âncora é `talvez` sozinho — as duas matam o substring.

### Observação aberta — `caso-01` e `caso-14` instáveis na suite da rodada 2

A suite saiu 16/16 e **2 instáveis**: `caso-01` passou na 3ª de 3, `caso-14` na 2ª
de 3. Nas quatro suites anteriores do mesmo dia, zero flaky.

`caso-01` é o que ganhou `pal-frase-max: 11` nesta sessão, então a primeira
hipótese é limiar apertado demais — apesar de ele ter fechado 5/5 na confirmação
da calibração. Em medição, 5 amostras não distinguem 0% de ~15% de falha.

A linha `FLAKY` **não diz qual asserção falhou** — o runner só imprime detalhe em
`FAIL`. Isso é lacuna do harness, não desta rodada: quem investiga flaky tem de
remedir com `PTC_TENTATIVAS=1` só para descobrir qual das quatro asserções caiu.

### Resolvido — o limiar do `caso-01` era meu, e estava errado

Não precisou de rodada nova: a resposta já estava nos dados do mesmo dia.

| Origem da medição | pal/frase da saída |
|---|---|
| calibração (5×) | 9,1 · 8,0 · 9,0 · 7,6 · 8,6 |
| fumaça do `--metricas` | **11,4** |
| execução avulsa (`mostrar.py`) | **12,1** |

**2 de 7 estouram `pal-frase-max: 11`** — ~28% de falha, que explica um `FLAKY`
passando na 3ª de 3. O erro tem duas camadas e a segunda é a que importa: as 5
amostras da calibração caíram agrupadas entre 7,6 e 9,1 por sorte, e as duas
discordantes **já estavam medidas** — foram ignoradas por não terem saído do laço
de calibração. Isso é escolher os dados que confirmam o limiar.

Conserto: `pal-frase-max: 11` → **`flesch-min: 50`**. 0 de 7 fora, margem 5,9, e
ainda reprova o texto-lixo (12,1) que motivou a métrica. O que ele perde: **não
assere melhora** — a entrada é 51,6, então reescrita nula passaria. É o teto real
deste caso: a saída varia de 7,6 a 12,1 pal/frase contra entrada de 13,1, então as
distribuições encostam e não cabe margem e asserção de melhora ao mesmo tempo.

O `AGENTS.md` ganhou três passos que faltavam no procedimento: olhar o
**espalhamento** e não só o pior valor; cruzar com **toda** medição avulsa do
caso; e reconhecer quando não existe limiar bom.

### Remedição de `caso-11` e `caso-13` (7 amostras cada)

- **`caso-11`** — flesch **73,2 nas sete**, variância zero. `flesch-min: 68` com
  margem 5,2. Sólido, mantém.
- **`caso-13`** — p/f 4,6 · 6,0 · 8,2 · 8,2 · 8,2 · 10,7 · 10,7. `pal-frase-max: 12`
  com margem 1,3 contra espalhamento de 6,1 — mesmo perfil de risco do `caso-01`.
  **Mantido em observação:** 0 de 7 violações, e no `caso-01` havia 2 na mão. Se
  ele aparecer `FLAKY` numa suite, tire a chave em vez de remedir.

Nota de método: as 3 últimas de 5 remedições voltaram vazias — erro de API por
limite de taxa depois de muitas chamadas seguidas. Vale orçar isso: uma sessão que
mede muito bate no teto e as medições perdidas parecem dado, não falha.

### Rodada 4 — PTC-7, identificadores de rede (2026-08-16)

Adversarial 3/8 → **4/8**. `caso-adv-7-identificadores-de-rede.md`, verde de
primeira. Sem achado.

O `caso-09` cobria o ponto que separa versão de decimal (`v1.5`, `3.11`,
`1,5 GB`). Sobrou o resto do terreno que o goal file lista e ninguém testou:
porta `:8080`, CIDR `10.0.0.0/24`, semver de três campos e hash curto.

`1.10.2` é o item perigoso, e está na entrada ao lado de `1.2` de propósito:
trocar o ponto por vírgula não só quebra o identificador como **inverte a
ordenação** — `1.10.2` é maior que `1.2` em semver e menor em decimal. Se a
PTC-7 disparar ali, o erro tem consequência visível na própria frase, não só na
grafia.

Nota que vale para quem for pôr limiar depois: este é o pior caso possível para a
métrica. `normaliza()` troca ponto entre dígitos por vírgula para não rachar
frase, então ela mede `1,10,2`. Não afeta asserção nenhuma aqui — as âncoras são
substring do texto cru —, mas **não ponha `flesch-min` nem `pal-frase-max` neste
caso**.

### Achado aberto — `FLAKY` não é diagnosticável, e isso custou uma investigação

O `caso-14` saiu `FLAKY` em duas suites (rodadas 2 e 4). Medido 5× com
`PTC_TENTATIVAS=1`: **5/5 PASS.**

A hipótese registrada antes da medição estava **errada**, e vale guardar o erro: o
`caso-14` empilha quatro decisões de desambiguação de sentido (`suportar` de
carga, `sensível` de dado, `atualmente` de tempo, `executar` de objeto concreto),
cada uma numa entrada do léxico com divisão "corte este sentido / mantenha
aquele". Parecia fragilidade estrutural — quatro julgamentos independentes numa
asserção só, ~81% de acerto composto se cada um acerta 95%. Os quatro
sobreviveram nas cinco rodadas.

O que resta: 2 flakies em suites de **18 chamadas seguidas**, 0 em rodadas
isoladas. Nesta mesma sessão houve erro de API por limite de taxa, com medições
voltando vazias. `rodar()` devolvendo `None` conta como tentativa falha, a
retentativa passa, e sai `FLAKY`. **Provável infra, não skill.**

**O achado real é do harness:** `FLAKY` não imprime detalhe — só `FAIL` imprime.
Então falha de asserção e soluço de API saem idênticas na tela, e a única forma de
separar é remedir o caso isolado, o que custa 5 chamadas e só responde depois. Num
gate de 18 chamadas sequenciais, falha transitória é esperada, e hoje ela se
disfarça de instabilidade da skill.

Conserto proposto (**outra sessão** — `verify.py` está fora do escopo deste loop):
`veredito()` já sabe por que cada tentativa falhou; basta guardar o motivo da
primeira falha e imprimi-lo na linha `FLAKY`, como já se faz em `FAIL`. Distinguir
`sem resposta do modelo` de `corrigiu indevidamente: X` transforma cada flaky de
investigação em leitura.

Enquanto isso não existe: **flaky que não reproduz isolado 5/5 é infra**, e não
deve gerar conserto na skill nem no caso.

### Rodada 5 — PTC-8, o hífen que fica (2026-08-16)

Adversarial 4/8 → **5/8**. `caso-adv-8-hifen-que-fica.md`, verde de primeira. Sem
achado.

O `caso-04` já era contra-teste da PTC-8, mas com **convenção de estilo** —
`front-end`, `data center`, `e-mail`. São palavras que a regra deixa em paz por
decisão declarada ("O que NÃO é erro"), não por mecânica de hífen. A mecânica em
si nunca tinha sido atacada.

Três formas corretas caem no mesmo gatilho superficial (prefixo + palavra em
`r`/`s`) por motivos **opostos**:

| Forma | Por que está certa |
|---|---|
| `sub-rede` | prefixo termina em consoante → hífen fica |
| `microsserviços` | prefixo termina em vogal → dobra o `s`, sem hífen |
| `pós-processamento` | prefixo tônico e acentuado → hífen sempre |

`sub-rede` é o item perigoso e é termo de rede de runbook real: aplicar a dobra
ali produz `subrrede`, que não existe. As três juntas obrigam a regra a decidir
três vezes em direções diferentes na mesma entrada.

`infraestrutura` entra como quarto termo e fecha um par com o lado positivo: o
`caso-01` planta `infra-estrutura` **errada** de propósito; aqui ela está certa e
não pode ser tocada.

Descartei `pré-requisito`: `prerrequisito` também é forma atestada, então a
asserção seria moeda ao ar. Adversarial precisa de item onde só uma grafia está
certa — mesma disciplina que tirou `a qualquer momento` da rodada 3 e
`plano de reversão` da rodada 1.

## Como retomar

Instale o harness uma vez — ele deixou de ser stdlib puro:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Depois, o que é grátis primeiro:

```bash
PTC_ADVERSARIAL=1 ./init.sh --cobertura   # o gap aberto: 5/8 (grátis)
./init.sh --cobertura                      # matriz fechada: 8/8 e 8/8 (grátis)
.venv/bin/python3 tests/test_runner.py     # 15 checks do runner (grátis)
./init.sh                                  # 19 casos — última rodada: 19/19, exit 0
```

O loop aberto é `loops/goal-falso-positivo.md` — rode com `/loop` sem intervalo.
O `goal-cobertura.md` está fechado; não reabra.

**Faltam três regras no adversarial: PTC-1, PTC-5, PTC-6.** Terrenos que o goal
file sugere e que ninguém testou ainda:

| Regra | Português correto que pode ser confundido com a violação |
|---|---|
| PTC-1 | `-se` pronominal inerente em cadeia (`o processo se encerra e se registra`) |
| PTC-5 | cadeia de `de` com termo lexicalizado — cada um conta como **um** nó (`chave de API do banco de dados` são 2, não 4) |
| PTC-6 | sigla consagrada que não pede expansão (`CPU`, `URL`, `HTTP`) |

Duas disciplinas que as cinco rodadas confirmaram e que economizam rodada perdida:

1. **Escolha item onde só uma forma está certa.** Foram descartados
   `plano de reversão` (rodada 1), `a qualquer momento` (rodada 3) e
   `pré-requisito` (rodada 5) — todos discutíveis, e asserção discutível não
   decide nada.
2. **A âncora tem de morrer no erro que ela deveria pegar.** Na rodada 2, a
   âncora virou `arquivos que o operador` porque `que o operador enviou`
   sobreviveria à vírgula, que era o falso positivo procurado.

E uma dívida de harness registrada acima: `FLAKY` não imprime motivo, então
soluço de API se disfarça de instabilidade da skill. Enquanto isso não muda,
**flaky que não reproduz isolado 5/5 é infra** — não gere conserto por causa dele.
