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
| `dist/` e `docs/index.html` | São **gerados**. Edite `SKILL.md`/`references/` e rode `tools/build.py`. Editar o destino é a mesma classe de erro de corrigir um `❌`: some no próximo build, sem aviso. |
| `flesch-min` / `pal-frase-max` já calibrados | O número saiu de 5 medições registradas em `loop-state.md`. Afrouxar para "fazer o teste passar" é desligar o gate sem removê-lo — e a próxima sessão acha que ele ainda gateia. |
| A versão pinada em `requirements.txt` | Cada limiar é calibrado sobre a silabação do Pyphen daquela versão do textstat. Um bump menor move `syllable_count` e invalida todo limiar medido, em silêncio. |

## Versões portáteis

`tools/build.py` acha a skill em `SKILL.md` + `references/*.md` e escreve cinco variantes em
`dist/` mais a página `docs/index.html`. Três consertos que o bundle achatado exige, e que é o
que o script existe para fazer: tirar o frontmatter YAML, tirar o aviso de edição, e reescrever
`references/X.md` para o título da seção correspondente — no arquivo único esses caminhos
apontam para nada.

O script **morre com exit 1** se uma seção que ele corta ou mantém pelo nome não existir mais.
Renomear um H2 do `SKILL.md` passa a quebrar o build em vez de emitir um bundle truncado em
silêncio.

`./init.sh` sem argumento roda `--verificar` antes dos casos. Com argumento (um caso, ou
`--cobertura`) não roda: durante o desenvolvimento, regenerar `dist/` a cada iteração só suja o
diff. O gate é a rodada completa — bundle defasado é uma skill publicada diferente da testada.

Ao acrescentar um arquivo em `references/`, ele entra no bundle sozinho (o glob é ordenado).
Ao acrescentar um destino de instalação, é a página que muda: `tools/index.template.html`.

## Verificação

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # textstat, uma vez
./init.sh                          # roda tudo (checa dist/ e o runner antes; ver abaixo)
./init.sh caso-01                  # um caso só (match por substring)
./init.sh --cobertura              # matriz regra × (positivo, contra-teste) — não chama o Claude
./init.sh --metricas               # legibilidade antes/depois, sem gatear — 1 chamada por caso
python3 tools/build.py             # regenera dist/ e docs/index.html
python3 tools/build.py --verificar # só confere se estão em dia — não chama o Claude
python3 tests/test_runner.py       # checks do próprio runner — não chama o Claude
PTC_MODELO=opus ./init.sh          # modelo diferente (default: sonnet)
PTC_MODELO_ESCALA= ./init.sh       # desliga a repetição em opus (ver "ESCALOU")
PTC_TENTATIVAS=1 ./init.sh         # sem retry (para medir flakiness)
PTC_TIMEOUT=600 ./init.sh          # timeout por chamada (default: 300s)
PTC_ADVERSARIAL=1 ./init.sh --cobertura   # matriz só com contra-teste caso-adv-*
```

`tests/test_runner.py` cobre as duas decisões que os casos **não** alcançam: os
quatro estados de `veredito()` e o filtro do `PTC_ADVERSARIAL`. Reproduzir um
`ESCALOU` de verdade depende do modelo menor falhar, que é justamente o que não
se controla — ali `rodar` vai dublado. Roda em `./init.sh` sem argumento, junto
do `build.py --verificar`, pela mesma razão: é grátis.

## Loops

Goal loops no formato do [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) (lecture-13). Rode com `/loop` sem intervalo — o modelo se auto-pauta e para no critério do próprio arquivo.

| Loop | Critério mecânico | Estado |
|---|---|---|
| `loops/goal-cobertura.md` | `./init.sh --cobertura` sai 0 | fechado (8/8, 8/8) |
| `loops/goal-falso-positivo.md` | `PTC_ADVERSARIAL=1 ./init.sh --cobertura` sai 0 | fechado (8/8, em 8 rodadas) |

Sem julgamento, sem "acho que já deu". O segundo existe porque o primeiro fechou com contra-testes escritos **junto com a regra** — todos testam a leitura legítima óbvia, e nenhum testa português correto que *se parece* com a violação. Por isso `PTC_ADVERSARIAL` não conta os antigos: PTC-6 tem 4 contra-testes e sairia "pronta" sem uma linha nova.

As 8 rodadas fecharam com **zero achado de falso positivo**, e o subproduto vale mais que o resultado: duas contradições internas do prompt foram medidas (`talvez` na rodada 3, expansão de sigla na rodada 6) e **nenhuma das duas foi consertada**, porque nenhuma oscila. `apenas` e `executar` foram, porque oscilavam. **Contradição textual não é achado — oscilação é.**

Estado entre rodadas em `loops/loop-state.md`. Para um objetivo novo, escreva outro `goal-*.md` — cada um precisa de objetivo, verificação executável, condição de parada e restrições.

O runner concatena `SKILL.md` + `references/*.md` **deste repo** e manda para `claude -p`. Ele testa o arquivo que você acabou de editar, não a cópia instalada em `~/.claude/skills/`.

Ele **não compara texto** — output de LLM não é determinístico. Verifica quatro coisas:

- **cobertura** — toda regra de `espera:` apareceu na tabela de violações
- **falso positivo** — todo termo de `nao-marca:` sobreviveu intacto no texto final
- **âncora** — todo termo de `deve-conter:` apareceu na saída
- **legibilidade** — o texto final passa dos limiares `flesch-min:`/`pal-frase-max:` do caso

Regra extra não reprova o caso.

A quarta existe porque as outras três medem **qual regra disparou**, nunca se a prosa
melhorou: a skill podia produzir reescrita correta-e-ilegível com os 14 casos verdes. Ela é
`tests/legibilidade.py` — Flesch adaptado ao PT-BR (Martins et al. 1996, USP São Carlos) sobre
os contadores do textstat. **A fórmula é nossa de propósito:** o textstat não tem português, e
`set_lang("pt_BR")` não dá erro — cai nas constantes do inglês em silêncio. Do textstat só se
usa o que vale em PT: `syllable_count` (via Pyphen, que tem `hyph_pt_BR.dic`), `lexicon_count`
e `sentence_count`. Não reabra isso sem ler a docstring do módulo.

### FLAKY não é PASS silencioso

O runner repete cada caso até `PTC_TENTATIVAS` (3) antes de reprovar, porque a suite oscila: rodando três vezes sem mudar nada, **casos diferentes falhavam a cada rodada**. Sem retry, o gate acusaria regressão inexistente e apontaria um culpado diferente toda vez.

| Estado | Significado |
|---|---|
| `PASS` | passou de primeira |
| `FLAKY` | passou numa retentativa — conta como ok, mas aparece destacado **com o motivo da falha que ele escondeu** |
| `ESCALOU` | falhou as 3 em `PTC_MODELO`, passou em `PTC_MODELO_ESCALA` (opus) |
| `FAIL` | falhou as 3 tentativas **e** a escalada — quebra real |

`ESCALOU` automatiza o que antes era passo manual desta seção: modelo menor às
vezes aplica a correção e não cita a regra na tabela, e a asserção lê a tabela.
Esquecer de conferir isso à mão faz um problema de rótulo passar por quebra da
skill — e num loop de caça a falso positivo, vira achado inventado no
`loop-state`. **`ESCALOU` não é falso positivo da regra**; o diagnóstico é a
linha "colisão de rótulo" da tabela abaixo. Depois de timeout não escala:
sem resposta para avaliar, a chamada cara não decide nada.

**Falha só de métrica também não escala.** `ESCALOU` quer dizer uma coisa só —
o modelo menor aplicou a correção e não citou a regra. Texto difícil de ler não
é colisão de rótulo, e o opus reescrever melhor não desmente regressão nenhuma:
escalar ali gastaria o modelo caro e ainda etiquetaria um FAIL legítimo de
legibilidade como problema de citação. Falha **mista** (rótulo + métrica) escala
normalmente, e a métrica é reavaliada na saída do opus junto com o resto.

**Flaky recorrente merece investigação**, não tolerância. Aponta para uma das causas abaixo — e a linha de detalhe impressa abaixo do `FAIL` **e do `FLAKY`** diz qual.

O `FLAKY` só passou a dizer isso em 2026-08-16. Antes, ele imprimia a contagem de tentativas e nada mais: falha de asserção e erro de API saíam idênticos na tela, e a única forma de separar era remedir o caso isolado com `PTC_TENTATIVAS=1` — 5 chamadas que respondiam depois, no meio de outra tarefa. Numa suite de 22 chamadas sequenciais, falha transitória é esperada, e ela se disfarçava de instabilidade da skill. O que o runner guarda é o motivo da **primeira falha diagnosticável**; timeout deixa a lista vazia de propósito, para continuar imprimindo "sem resposta do modelo" em vez de inventar uma asserção que não quebrou.

| Detalhe impresso | Causa | Conserto |
|---|---|---|
| `corrigiu indevidamente: <termo>` | **asserção frágil** — o termo de `nao-marca` some por reescrita legítima | encurtar o termo para o núcleo que prova a regra |
| `faltou: PTC-N` | **regra ambígua** — o modelo hesita porque a regra não decide o caso | no `SKILL.md`/`references`, **não** no teste |
| `faltou: PTC-N` | **colisão de rótulo** — a correção sai certa e a linha é etiquetada com outra regra | dizer no `SKILL.md` onde a regra **não** mora, não só onde mora |
| `não apareceu: <termo>` | **âncora frágil** — o `deve-conter` fixa uma escolha que a skill não é obrigada a fazer | desambiguar a **entrada**, não encurtar a âncora |
| `métrica: flesch X < Y` | **limiar chutado**, ou regressão real de legibilidade | rode `--metricas` 5×; se nunca fecha 5/5, o limiar estava chutado — baixe ou tire a chave |
| `métrica: não achei o 'Texto final:'` | **formato** — a skill mudou o rótulo da seção final | conserte `INICIO_TEXTO_FINAL` ou o formato de saída da skill, **nunca** o limiar |
| `métrica: texto curto demais` | **caso curto** — não há palavra que sustente a medida | tire o limiar deste caso |
| `sem resposta do modelo` | **infra** — timeout, erro da API ou limite de taxa | nenhum; espere e rode de novo |

**Âncora frágil, caso real:** `caso-11` entrava com `Pacote enviado às 14h30` e ancorava `agente enviou` — 3/5. Com marca de tempo, `O agente envia` e `O agente enviou` são as duas corretas, porque a entrada não diz se aquilo é log de evento passado ou comportamento recorrente. Trocado por `ao servidor`, que força a leitura de ação em presente: 5/5. O conserto foi na entrada; encurtar a âncora teria escondido a ambiguidade em vez de removê-la.

**Asserção frágil, caso real:** `caso-08` pedia `chave de API do banco de dados` intacto. A PTC-6 expande `API` na primeira ocorrência — `chave da Interface de Programação de Aplicações (API) do banco de dados` — e o substring literal morre sem que a PTC-5 tenha dado falso positivo algum. Encurtado para `do banco de dados`, que prova a mesma coisa (a cadeia de `de` não foi quebrada) e sobrevive à expansão.

**Colisão de rótulo, caso real:** `caso-01` citava PTC-6 em 4/5. As duas hipóteses — não aplicou, ou aplicou e não citou — dão a mesma saída no runner, e só o texto final bruto separa. Rodando 6× e procurando `APIs`: a correção saiu **6/6**, e em 2 delas a linha veio como `PTC-8 (apóstrofo não marca plural)`. Plural de sigla parece ortografia; o `SKILL.md` dizia que a regra mora na PTC-6 e não dizia que ela não mora na PTC-8. Com a cláusula de fronteira na PTC-8: 11/11. **Diagnostique olhando a saída bruta antes de mexer na regra** — as duas hipóteses mandavam para lugares opostos.

**Regra ambígua, caso real:** `apenas` estava nos dois lados da skill — `SKILL.md` (PTC-5) prescrevia `apenas um teste` como a forma correta do sentido anteposto, e `lexico.md` mandava cortar `apenas` como minimizador. Os dois arquivos vão concatenados no mesmo prompt, então o modelo decidia diferente a cada rodada. A entrada do léxico foi dividida em hedge (`é apenas um bug`, corte) e quantidade (`apenas um teste`, mantenha).

**Infra:** `FAIL` sem `faltou` e sem `corrigiu` significa que nunca houve resposta para avaliar. Continua contando como falha — caso não verificado não é caso verde — mas não é regressão. Suba `PTC_TIMEOUT` se for recorrente.

**Limite de taxa é o modo de falha da suite inteira, não de um caso.** Uma rodada completa são 22+ chamadas sequenciais; somada a medições no mesmo dia, ela bate no teto e daí para frente **todos** os casos saem em `sem resposta do modelo`. Aconteceu em 2026-08-16: 4/22, com os 18 restantes idênticos. O sinal é a uniformidade — regressão de skill não derruba 18 casos diferentes na mesma linha. Espere e rode de novo; não conserte nada. Orce isso antes de uma sessão que mede muito.

Casos com histórico de instabilidade estão registrados em `loops/loop-state.md`.

### Custo e falso alarme

Cada caso é **até `PTC_TENTATIVAS` (3) chamadas** ao Claude, e a suite tem 22 casos — 22 chamadas quando tudo passa de primeira, mais uma por retentativa. O default é `sonnet`: Opus a cada rodada fica caro, e a asserção é sobre qual regra disparou, não sobre a qualidade da prosa.

Durante o desenvolvimento, prefira `./init.sh <caso>` e deixe a suite inteira para o fim. `--cobertura` é grátis (não chama a API).

`--metricas` **não** é grátis, ao contrário de `--cobertura`: 1 chamada por caso, sem retry. E o
procedimento de calibração pede 5 rodadas — orce isso antes de sair medindo a suite inteira.

**Isto agora é automático:** o runner repete em opus antes de dar `FAIL`, e o caso sai como `ESCALOU`. Só chama o modelo caro no que já falhou três vezes, então em rodada verde o custo é zero. Para medir sem essa rede — comparando modelos, por exemplo — use `PTC_MODELO_ESCALA=`.

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
| `flesch-min` | piso do Flesch-PT no **texto final** — medido, nunca chutado |
| `pal-frase-max` | teto de palavras por frase no **texto final** |

O parser corta a saída antes da seção "mantido de propósito" para checar `nao-marca` — ali a skill cita a regra que *pegaria* o trecho, sem tê-lo corrigido, e isso acusaria falso positivo.

`deve-conter` **não** é cortado: o que ele existe para provar — tabela de proposições do modo bilíngue, registro do linter reverso — fica fora do texto reescrito por desenho.

### Quando usar `deve-conter`

Quando o comportamento testado **não tem número PTC próprio** e a asserção por regra citada não o distingue de outro caso. Os três comportamentos da flag `destinatário: agente` são isso: `caso-11` é indistinguível de um PTC-1 comum pela tabela de violações, e só `deve-conter` prova que a flag mudou alguma coisa.

**Âncora se mede, não se chuta.** Rode o caso 5× com `PTC_TENTATIVAS=1` e só aceite âncora 5/5. Uma que passa 3/5 vira `FLAKY` permanente e some no ruído. Ver `loop-state.md` para as duas âncoras que foram reprovadas e por quê.

### O limiar se mede, não se chuta

Mesma doutrina da âncora, e a tentação aqui é maior porque limiar é um número e número parece
objetivo. Não é: ele é uma aposta sobre a oscilação do modelo até ser medido.

1. `PTC_TENTATIVAS=1 ./init.sh --metricas <caso>`, **5 vezes**.
2. Pegue o **pior** "texto final" das 5 — menor flesch, maior palavras/frase.
3. **Olhe o espalhamento, não só o pior.** Se `max − min` for maior que a margem que você ia usar, 5 amostras não viram a cauda: meça mais 5 ou não ponha limiar. Foi aqui que o `caso-01` custou uma sessão — ver abaixo.
4. Limiar = pior menos a margem: flesch **−5**, palavras/frase **+2**. Arredonde para número humano.
5. **Cruze com toda medição que você já tem do caso**, inclusive as avulsas — uma rodada de fumaça, um `--metricas` solto. Elas contam como amostra. Ignorá-las porque não saíram do "laço de calibração" é escolher os dados que confirmam o limiar.
6. Escreva a chave e rode `PTC_TENTATIVAS=1 ./init.sh <caso>` 5×. **Só aceite 5/5.** Menos que isso o limiar é moeda ao ar: baixe ou tire a chave.
7. Registre o número medido, o espalhamento e a data em `loops/loop-state.md`, como as âncoras já são.

**Se a saída encosta na entrada, não há limiar bom.** O `caso-01` tem entrada de
13,1 palavras/frase e saída medida entre 7,6 e 12,1: não cabe margem e asserção
de melhora ao mesmo tempo. Ali o limiar só pode ser **piso contra lixo** — um
`flesch-min` abaixo da legibilidade da entrada, que pega reescrita destruída e
não pega reescrita preguiçosa. Aceite o limite ou não ponha a chave; um limiar
apertado que oscila é pior que nenhum, porque vira `FLAKY` permanente e some no
ruído junto com os flaky que importam.

Ordem de grandeza medida neste repo: comunicado burocrático 35, o `caso-01` cru 52, reescrita
PTC boa acima de 100. A escala de Martins não é limitada a `[0, 100]` — período único de
palavras longas dá negativo, e isso é sinal, não defeito.

**Contra-teste de `espera:` vazia não leva limiar.** O comportamento correto ali é o texto sair
praticamente inalterado, então o número assere uma propriedade da **entrada** — que é fixa e
escrita por nós. Passa no dia 1 e continua passando faça a skill o que fizer, inclusive se ela
quebrar. É o caso verde que não verifica nada. Se algo se assere num contra-teste é *teto* de
mudança, e teto já é o que `nao-marca` faz, com termo concreto em vez de número agregado.

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
  verify.py               # runner
  legibilidade.py         # Flesch-PT (Martins 1996) sobre os contadores do textstat
  test_runner.py          # checks do runner — grátis, roda no init.sh
  casos/*.md              # casos de regressão
  casos/caso-adv-*.md     # contra-teste adversarial (ver goal-falso-positivo)
loops/
  goal-cobertura.md       # goal loop: matriz regra × (positivo, contra-teste)
  goal-falso-positivo.md  # goal loop: contra-teste adversarial por regra
  loop-state.md           # estado entre rodadas + achados abertos
tools/
  build.py                # gera dist/ e docs/ — ver "Versões portáteis"
  index.template.html     # molde da página de instalação (aqui é onde se edita)
dist/                     # GERADO: bundles para agentes fora do Claude Code
docs/index.html           # GERADO: página de instalação (GitHub Pages)
init.sh                   # checa pré-requisitos e roda o verify
requirements.txt          # textstat — só o harness; instalar a skill não precisa de nada
AGENTS.md                 # este arquivo
```

Só `SKILL.md` e `references/*.md` vão para o prompt. O resto é harness ou saída gerada.

O harness deixou de ser stdlib puro quando a métrica entrou: `python3 -m venv .venv &&
.venv/bin/pip install -r requirements.txt`, uma vez. O `init.sh` prefere `.venv/bin/python3`
quando ele existe e recusa rodar sem o textstat — falhar em 200 ms vale mais que descobrir a
dependência ausente depois de 14 chamadas de API. **A skill em si continua sem dependência
nenhuma:** ela é Markdown.

## Origem das decisões

O desenho — por que 8 regras próprias em vez de traduzir as 53 do ASD-STE100, por que a fonte de verdade é o idioma do input, por que os níveis existem — está em `README.md`, seções "Por que não é o STE traduzido" e "Modo bilíngue". Leia antes de propor mudança estrutural; várias alternativas óbvias já foram descartadas com evidência.
