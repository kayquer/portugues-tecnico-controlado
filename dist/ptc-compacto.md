# Português Técnico Controlado (PTC) — versão curta

Reescreve texto técnico em português do Brasil para ter uma leitura só. Versão reduzida, sem exemplos: para campo de instrução com limite de caracteres.

Versão 1.1.0 · https://github.com/kayquer/portugues-tecnico-controlado

Este arquivo é o pacote completo. Onde o texto mandar consultar outra seção, ela já está aqui embaixo — não há arquivo externo para carregar.

---

# Português Técnico Controlado (PTC)

Reescreve texto técnico em português do Brasil para que ele tenha **uma leitura só**. O leitor — humano operando um procedimento, ou um modelo consumindo uma instrução — não tem como perguntar "você quis dizer X ou Y?". O texto precisa responder antes.

Inspirado no **ASD-STE100** (Simplified Technical English), o padrão de linguagem controlada da indústria aeroespacial. Mas não é uma tradução dele: metade das 53 regras do STE vira regra vazia em português, e os vícios reais do PT ficam sem cobertura. Ver "Por que não é o STE traduzido".

Esta skill é **autossuficiente**. Não invoca nem depende de nenhuma outra.

## Quando usar

- Procedimento, runbook, documentação de sistema, ou mensagem de erro em português.
- Texto que um agente/LLM vai consumir sem humano no meio.
- Comunicado interno que precisa ser claro sem virar robô (nível `leve`).
- Documento que precisa existir em português **e** inglês, com as duas versões dizendo a mesma coisa.

**Não use para** texto onde voz, nuance ou persuasão são o ponto — copy de marketing, texto criativo. Linguagem controlada é deliberadamente plana.

## Passo 0 — classificar antes de reescrever

Nunca comece a reescrever sem fixar estes três parâmetros. Se o usuário não disse, **infira e declare** o que assumiu numa linha:

1. **Nível**: `estrito` · `descritivo` · `leve` (tabela em "Níveis")
2. **Destinatário** (só importa em `estrito`): `humano` · `agente`
3. **Bilíngue?**: se sim, carregue a versão completa desta skill **antes** de mexer no texto — o pipeline tem ordem obrigatória e refazer custa caro.

## As 8 regras

PTC-1 a PTC-5 são de **desambiguação** — atacam onde o português deixa duas leituras. Exigem julgamento.
PTC-6 a PTC-8 são de **consistência** — terminologia, formato, grafia. São mecânicas e nunca relaxam.

### PTC-1 — Quem faz, aparece

A regra número um, porque em português a 3ª pessoa do singular colapsa `ele`/`ela`/`você`/`o sistema`/`o usuário` numa forma só. Tudo que o inglês desambigua ao obrigar o sujeito, o português perde.

- **Sujeito lexical em toda oração finita.** Única exceção: imperativo dirigido ao leitor.
- **Contra-regra obrigatória:** em coordenação com o mesmo sujeito, **não** repita — senão o texto vira gagueira. Se o sujeito muda, quebre em duas frases.
- **Sem `-se` apassivador ou indeterminador.** Teste mecânico, sem metalinguagem: *se dá para reescrever com "é/são + particípio" sem mudar o sentido, é o `se` proibido.* `Faz-se a validação` → `A validação é feita` ✅ logo é proibido. Já `o serviço se reinicia` (pronominal inerente) passa.
  **O teste só reprova em `estrito`.** Em `descritivo`, `-se` apassivador sem ator relevante fica — a mesma licença que a tabela de níveis dá à voz passiva. `Verifica-se a integridade dos arquivos` ✅ em descrição de sistema, ❌ em procedimento. Não invente ator (`o sistema verifica`) para fugir do `-se`: ator inventado é fato inventado.
- **Sem clítico de 3ª pessoa** (`o`, `a`, `os`, `as`, `lhe`), **sem mesóclise** (`far-se-á`), **sem `o mesmo`**, **sem demonstrativo apontando para fora da frase.** Repita o substantivo.

Argumento extra para banir o `-se`: ele colide com o `se` condicional na mesma frase.

### PTC-2 — Uma proposição por frase, uma forma verbal

- **Instrução ao leitor:** imperativo na forma "você" (`Clique`, `Faça`, `Vá`). Proibido `tu` (`Clica`), infinitivo (`Clicar em Salvar`), `deve-se`, `por favor`, `poderia`.
- **Descrição de comportamento** (tool description, docstring): presente do indicativo, 3ª pessoa. `Retorna a lista de pedidos abertos.` Nunca `Retornar` nem `Use isto para retornar`.
- **Nunca misture** imperativo e infinitivo na mesma lista. É o erro mais comum em runbook brasileiro.
- **Sem gerúndio conector.** Gerúndio só em perífrase durativa com `estar` e sujeito explícito (`O job está processando os registros`). Nunca ligando duas orações.
- **Sem relativa explicativa** (a com vírgula) em modo estrito. A vírgula muda o escopo de forma invisível. Se a informação é adicional, vira frase separada.

> `Os servidores que falharam foram reiniciados.` → só os que falharam
> `Os servidores, que falharam, foram reiniciados.` → todos falharam e todos foram reiniciados

`o qual`/`a qual` só para desfazer ambiguidade de antecedente. `onde` só para lugar físico.

### PTC-3 — Modalidade e quantidade explícitas

`deve` em português é obrigação **e** probabilidade na mesma forma. Isso é indecidível e precisa ser resolvido na escrita.

| Modal | Sentido único permitido | Substitui |
|---|---|---|
| `deve` | obrigação | `deverá`, `há de`, `é necessário que` |
| `pode` | permissão | — |
| `consegue` | capacidade técnica | `pode` no sentido de capacidade |
| — | probabilidade: **proibido usar modal** — dê número ou escreva `talvez` | `deveria`, `poderia`, `deve ser que` |

- **Zero hedge.** `deveria funcionar` → `funciona` ou `deve funcionar` (escolha).
- **Quantificador vago vira número.** `alguns registros` → `até 50 registros`; `pode demorar` → `leva até 30 s`.
- **Negação antes do quantificador.** `Nem todos os arquivos foram enviados`, nunca `Todos os arquivos não foram enviados`.

### PTC-4 — Verbo pleno, não verbo-suporte

O alvo é a construção com **verbo leve** — `fazer`/`realizar`/`efetuar`/`proceder a`/`executar`/`promover` + nominalização. Não é a nominalização em si.

**Nominalização legítima permanece.** `A validação de entrada rejeita CPFs inválidos` está correto — ali o substantivo é o termo do domínio. Não mexa.

### PTC-5 — Sintaxe plana

- **Adjetivo sempre depois do substantivo.** Em português, antepor muda o sentido: `um simples teste` (só um teste) ≠ `um teste simples` (de baixa complexidade). Também `certo procedimento`/`procedimento certo`, `único usuário`/`usuário único`, `nova versão`/`versão nova`. Se o sentido pretendido era o anteposto, use outra palavra: `apenas um teste`, `o procedimento correto`.
- **Cadeia de `de`/`em`/`para` ≤ 2 nós.** Termo lexicalizado conta como **um** nó (`banco de dados`, `chave de API`, `tempo de resposta`, `fila de mensagens`).
- **Nada entre verbo e objeto.** Circunstância vai no início (se for condição ou gatilho) ou no fim (se for meio ou local). Nunca no meio.
- **Modificador sobre coordenação, repetido.** `os relatórios e planilhas antigos` é ambíguo → `os relatórios antigos e as planilhas antigas`.
- **≤ 25 palavras** (procedimento) / **≤ 30** (descritivo) — **e no máximo uma subordinada por frase** em modo estrito.

O limite de palavras é só o proxy verificável — 25 palavras cabem duas subordinadas encaixadas. O cap estrutural de **uma subordinada** é o que de fato desambigua.

### PTC-6 — Termos congelados, variante BR

- **Um conceito, um termo, sempre o mesmo** — inclusive dos dois lados do par bilíngue.
- **Sigla com gênero e artigo fixos** no glossário do projeto (`a API`, `a URL`, `o endpoint`). Consistência importa mais que estar "certo". Plural sem apóstrofo: `APIs`, nunca `API's`. Expanda na primeira ocorrência.
- **Fixe a variante brasileira**: `arquivo` (não `ficheiro`), `usuário` (não `utilizador`), `tela` (não `ecrã`), `mouse` (não `rato`), `equipe`/`time` (não `equipa`), `cadastro` (não `registo`), `aplicativo` (não `aplicação`).
- Aplique o léxico evite→use, os conectores ambíguos e o glossário de siglas: **a seção "Léxico controlado PT-BR"**.

> **O Acordo de 1990 unificou a ortografia, não o léxico.** `utilizador` e `ecrã` **não são erros** — são português europeu. Esta skill *fixa* a variante BR por consistência de projeto. Nunca marque uma variante regional legítima como incorreta.

### PTC-7 — Formato de número, data e unidade

Aqui o erro não é de estilo, é **dado errado**.

- **Decimal:** vírgula em PT, ponto em EN. `1,5 GB` (PT) = `1.5 GB` (EN). Deixar `1.5` num texto PT lê-se como mil e quinhentos.
- **Milhar:** `1.000` (PT) vs `1,000` (EN) — inverso perfeito. Fonte de erro de ordem de grandeza 1000×.
- **Data: ISO 8601 (`2026-08-02`) nos dois idiomas.** `02/08/2026` é 2 de agosto em PT e 8 de fevereiro em EN. Se o contexto exigir extenso, escreva o mês por nome.
- **Hora:** 24 h, `14h30`. Nunca `2:30 PM` em PT.
- **Unidade:** espaço entre número e símbolo (`10 MB`, `200 ms`); símbolo nunca traduzido nem pluralizado (`5 kg`, não `5 kgs`).
- **Intervalo:** `de 10 a 20`, nunca `10-20` (colide com sinal de menos).

### PTC-8 — Ortografia PT-BR vigente

Acordo Ortográfico de 1990, **obrigatório no Brasil desde 2016-01-01** (Decreto 6.583/2008, transição prorrogada até 2015-12-31). Fonte autoritativa: **VOLP da Academia Brasileira de Letras**.

Quatro situações respondem por quase todo o erro de hífen em texto de TI:

| Situação | Grafia | Exemplo |
|---|---|---|
| prefixo em vogal + **r/s** | junta e **dobra** a consoante | `microsserviço`, `autosserviço`, `antirracismo` |
| prefixo em vogal + vogal **diferente** | junta | `infraestrutura`, `extraescolar`, `multiusuário` |
| `co-`, `re-` | juntam **sempre** | `coautor`, `coprocessador`, `reescrever`, `reindexação` |
| `pré-`, `pós-`, `pró-` tônicos | hífen **sempre** | `pré-requisito`, `pós-processamento` |

Fora dessas quatro, **não deduza** — as demais situações estão na versão completa desta skill, "Hífen com prefixo": vogal igual ou `h` depois do prefixo (`anti-inflamatório`, `super-homem`), prefixo terminado em consoante (`inter-relação`, mas `superusuário`), `sub-` + b/h/r (`sub-rotina`), e `não` + substantivo, que perdeu o hífen com o Acordo (`não conformidade`).

Também: trema abolido (`frequência`, `sequência`, `bilíngue`); ditongo aberto em paroxítona sem acento (`ideia`, `assembleia`, `heroico`); sem circunflexo em `oo`/`ee` (`voo`, `leem`, `creem`, `veem`); diferenciais abolidos (`para`, `pelo`, `polo`, `pera`) mas **mantidos** `pôr` e `pôde`.

Casos de detalhe, armadilhas de TI e a lista do que **não** é erro: **a versão completa desta skill**. Em dúvida de grafia, consulte o VOLP — não deduza.

**Fronteira com a PTC-6.** Plural de sigla (`API's` → `APIs`), gênero e artigo de sigla e variante BR (`ficheiro` → `arquivo`) **parecem** ortografia e não são: rotule como **PTC-6**. Aqui só entra o que o Acordo de 1990 decide — hífen, acento, trema, grafia da palavra comum.

## Níveis

| | `estrito` | `descritivo` | `leve` |
|---|---|---|---|
| **Uso** | procedimento, runbook, output de agente | documentação de sistema | comunicado interno |
| PTC-1 sujeito, correferência | obrigatório | obrigatório | obrigatório |
| PTC-1 sem `-se` passivo | obrigatório | ok em descrição sem ator | livre |
| PTC-2 uma proposição/frase | obrigatório | 2 se coordenadas | livre |
| PTC-2 forma verbal fixa | obrigatório | presente 3ª pessoa | livre |
| PTC-2 sem gerúndio conector | obrigatório | obrigatório | recomendado |
| PTC-2 sem relativa explicativa | obrigatório | 1 por frase | livre |
| PTC-3 modal unívoco, sem hedge | obrigatório | obrigatório | recomendado (hedge social ok) |
| PTC-4 sem verbo-suporte | obrigatório | recomendado | dispensado |
| PTC-5 adjetivo pós-nominal | obrigatório | obrigatório | recomendado |
| PTC-5 cadeia de `de` | ≤2 | ≤3 | dispensado |
| PTC-5 limite | ≤25 + 1 subordinada | ≤30 | ≤35, sem cap estrutural |
| PTC-6 termo congelado | obrigatório | obrigatório | só nomes de produto/processo |
| PTC-6 léxico evite→use | obrigatório | obrigatório | **dispensado** |
| PTC-7 número/data/unidade | obrigatório | obrigatório | obrigatório |
| PTC-8 ortografia | obrigatório | obrigatório | obrigatório |
| Voz passiva | proibida | ok sem ator relevante | livre |
| Lista vertical p/ sequência ≥3 | obrigatório | recomendado | dispensado |
| ≤6 frases/parágrafo | obrigatório | obrigatório | recomendado |
| Condição/segurança abre a frase | obrigatório | obrigatório | obrigatório |
| 1ª pessoa (`nós`, `nosso time`) | proibida | evitar | **permitida e desejável** |

**PTC-1, PTC-7 e PTC-8 nunca relaxam.** Em comunicado, `o mesmo foi cancelado`, `1,000 clientes` e `infra-estrutura` continuam causando dano — ortografia errada não fica menos errada porque o texto é informal.

O resto sai justamente para o comunicado **não ficar robótico**. Aplicar rigor de procedimento a texto para humano não-técnico é o erro clássico de quem adota linguagem controlada.

### Flag `destinatário: agente`

Só se aplica sobre `estrito`. Não é um quarto nível — muda três coisas:

1. Instrução ao agente é imperativo; **descrição de ferramenta é presente 3ª pessoa**.
2. **Nenhuma anáfora atravessa frase.** Cada frase se sustenta sozinha, porque o consumidor pode truncar.
3. **Status é sujeito + verbo finito**, nunca particípio isolado.

## Processo

1. **Leia o texto inteiro** antes de reescrever qualquer coisa. Você precisa saber o que ele ainda tem que dizer depois.
2. **Fixe os parâmetros** do Passo 0. Declare o que assumiu.
3. **Se for bilíngue**, carregue a versão completa desta skill agora e siga o pipeline de lá — a ordem é obrigatória.
4. **Varra frase a frase**, marcando qual regra PTC cada trecho viola.
5. **Reescreva cada trecho marcado**, preservando o sentido exato. Se a reescrita fosse custar precisão — uma condição de segurança, um qualificador de escopo, um número — **mantenha o texto longo e sinalize** em vez de simplificar em silêncio.
6. **Consulte as referências** quando a dúvida for de grafia (a versão completa desta skill) ou de palavra (a seção "Léxico controlado PT-BR"). Não chute grafia.
7. **Se o texto já estiver conforme, diga isso** em "Mantido de propósito" — e emita o "Texto final" mesmo assim, idêntico ao original. Não force mudança em texto que já está bom.

## Formato de saída

```markdown
**Nível:** estrito · **Destinatário:** humano *(inferido — não foi especificado)*

| Regra | Original | Reescrito |
|---|---|---|
| PTC-1 (`-se` apassivador) | "Faz-se a validação do token." | "O gateway valida o token." |
| PTC-4 (verbo-suporte) | "Realize a conferência dos logs." | "Confira os logs." |
| PTC-8 (hífen r/s) | "micro-serviços" | "microsserviços" |

**Texto final:**
> [texto reescrito corrido]

**Mantido de propósito:** [o que não foi simplificado e por quê]
```

**A seção "Texto final" sai sempre**, inclusive quando nada mudou — nesse caso, repita o original. Quem consome a saída (uma pessoa aplicando o procedimento, um script, outro agente) procura o texto reescrito num lugar só, e não pode depender de você ter achado alguma coisa. Tabela vazia é resposta legítima; saída sem texto final não é.

No modo bilíngue, acrescente a tabela de proposições e — se o linter reverso disparou — a lista de ambiguidades que a fonte teve que resolver. Ver a versão completa desta skill.

---

# Léxico controlado PT-BR

## Evite → use

| Evite | Use | Por quê |
|---|---|---|
| realizar / efetuar / proceder a | o verbo pleno (`validar`, `enviar`, `conferir`) | verbo-suporte; esconde a ação (PTC-4) |
| utilizar | usar | sílaba a mais, zero ganho |
| possuir | ter | `possuir` implica posse jurídica |
| disponibilizar | dar acesso a / publicar / entregar | três ações diferentes num verbo só |
| necessitar de / demandar | precisar de / exigir | — |
| solicitar | pedir | — |
| o mesmo / a mesma | repita o substantivo | correferência falsa (PTC-1) |
| no sentido de / a fim de que | para | — |
| através de *(meio)* | por / por meio de | `através` é atravessar |
| em função de / face a | por causa de / para | `em função de` também é matemático |
| no âmbito de | em | — |
| sendo que | ponto final | conector vazio |
| onde *(não-lugar)* | em que / reescreva | — |
| eventualmente | às vezes **ou** no futuro | escolha um; falso amigo de `eventually` |
| inclusive | e também **ou** até | dois sentidos em PT-BR |
| vir a ser / estar sendo | ser / está | perífrase oca |
| impactar | afetar / aumentar / reduzir | diga a direção |
| performance | desempenho | — |
| garantir *(que X funciona)* | verificar / confirmar | um agente não garante, verifica |
| validar | verificar **ou** aprovar | dois sentidos; congele um por projeto |
| atualizar | atualizar *(update)* / recarregar *(refresh)* | dois sentidos |
| acessar | abrir / ler / consultar | genérico demais |
| gerar | criar / calcular / exportar | genérico demais |
| apresentar erro | exibe erro / retorna erro / falha com | três coisas diferentes |
| tratar | capturar *(exceção)* / resolver *(problema)* | — |
| subir / derrubar / startar | iniciar / parar / implantar | gíria de plantão |
| vale ressaltar / é importante notar | corte | metatexto |
| basicamente / simplesmente / apenas *(hedge: `é apenas um bug menor`)* | corte | minimizador; muda o fato |
| apenas / somente *(quantidade: `apenas um teste`)* | mantenha | não é hedge: restringe a quantidade. Cortar muda o fato, e a PTC-5 prescreve `apenas` para o sentido anteposto |
| executar *(+ nominalização: `executar a validação`)* | o verbo pleno (`valide`) | verbo-suporte (PTC-4) |
| executar *(+ objeto concreto: `execute o script`)* | mantenha | ali `executar` **é** o verbo pleno. A PTC-4 só proíbe a construção com nominalização |

### Burocratês

Fórmula de ofício que sobreviveu no e-mail corporativo. Some sem levar informação junto.

| Evite | Use | Por quê |
|---|---|---|
| vimos por meio desta / venho por meio deste | corte | abertura vazia; a primeira frase já devia ser o assunto |
| segue anexo / segue em anexo | o relatório está anexado | `segue` esconde quem envia (PTC-1) e a concordância de `anexo` gera dúvida |
| conforme alinhado / conforme conversado | conforme a decisão de 2026-03-14 | referência sem rastro: ninguém consegue conferir |
| para conhecimento / para ciência | corte, ou diga a ação esperada | não diz se o leitor precisa fazer algo |
| no que tange a / no tocante a | sobre | — |
| a partir do momento em que | quando | — |
| tendo em vista que | porque | — |
| de forma a / de modo a | para | — |
| sem prejuízo de | e também **ou** sem cancelar | adição e ressalva na mesma expressão |
| dar início a | iniciar | verbo-suporte (PTC-4) |
| fazer uso de | usar | verbo-suporte (PTC-4) |
| ter conhecimento de | saber | verbo-suporte (PTC-4) |
| levar em consideração | considerar | verbo-suporte (PTC-4) |
| ter como objetivo | servir para | verbo-suporte (PTC-4) |
| entrar em contato com | contate / ligue para / escreva para | verbo-suporte, e o canal fica implícito |
| a princípio / em princípio | inicialmente **ou** em tese | dois sentidos opostos: provisório e teórico |
| aderente a | conforme a / compatível com | anglicismo de `compliant`; em PT `aderente` é o que gruda |

### Gíria de plantão

Vocabulário de conversa de time que não sobrevive a um runbook lido às 3h da manhã.

| Evite | Use | Por quê |
|---|---|---|
| rodar | executar *(script)* / funcionar *(serviço)* | dois sentidos |
| puxar | buscar / baixar / consultar | três operações diferentes |
| bater *(com)* | conferir com / coincidir com | — |
| quebrar | falhar / interromper / ficar inválido | três resultados diferentes |
| estourar | exceder o limite / lançar exceção | dois sentidos |
| cair | ficar indisponível / falhar / ser encerrado | três sentidos |
| logar | registrar em log **ou** entrar na conta | dois sentidos opostos na mesma palavra |
| setar | definir | anglicismo sem ganho |
| resetar | reiniciar / limpar / restaurar o padrão | três operações diferentes |
| deployar | implantar / publicar | anglicismo sem ganho |
| acionar | chamar / notificar / iniciar | três ações diferentes |
| escalar | aumentar a capacidade **ou** encaminhar ao nível superior | dois sentidos técnicos opostos |
| otimizar | reduzir / acelerar / diminuir o custo | diga a direção, como em `impactar` |
| checar | verificar / conferir | anglicismo; e não distingue os dois |

### Falsos amigos do inglês

Aparecem em texto traduzido e em documentação escrita por quem lê em inglês o dia inteiro.

| Evite | Use | Por quê |
|---|---|---|
| assumir *(supor)* | supor / presumir | em PT `assumir` é assumir responsabilidade |
| endereçar *(tratar)* | tratar / resolver | em PT `endereçar` é pôr endereço |
| suportar *(aceitar)* | aceitar / ser compatível com | em PT `suportar` é aguentar carga — e esse sentido é legítimo |
| sensível *(significativo)* | significativo / relevante | `dado sensível` é outro sentido e fica |
| requerimento | requisito | em PT `requerimento` é petição |
| compreensivo | completo / abrangente | em PT `compreensivo` é quem compreende os outros |
| efetivo | eficaz | em PT `efetivo` é permanente ou de fato |
| prover | fornecer / dar | decalque de `provide`; raro em PT-BR fora de tradução |
| reportar | relatar / informar / registrar | `reportar-se a` é subordinar-se: outro sentido |
| submeter | enviar | em PT `submeter` é sujeitar alguém a algo |
| abortar | interromper / cancelar | — |
| deletar | excluir / apagar | anglicismo sem ganho |
| atualmente *(tradução de `actually`)* | na verdade | `atualmente` em PT é "no momento": inverte o sentido |

## Conectores ambíguos

O ASD-STE100 resolve ambiguidade lexical com um dicionário de ~900 palavras. Em português o veneno está concentrado nos conectores — esta tabela é o análogo funcional.

| Conector | Ambiguidade | Use |
|---|---|---|
| `uma vez que` | causal ou temporal | `porque` / `quando` |
| `como` *(início de frase)* | causal, comparativo, conforme | `porque` / `conforme` |
| `desde que` | temporal ou condicional | `se` / `a partir de` |
| `à medida que` | proporcional ou temporal | `quando` / `conforme` |
| `na medida em que` | causal, e trocado com `à medida que` o tempo todo | `porque` |
| `enquanto` | temporal ou adversativo | `enquanto` *(só temporal)* / `mas` |
| `inclusive` | "até mesmo" ou "aliás" | `até` / `e também` |
| `sendo que` | nenhuma — é cola | ponto final |
| `e/ou` | proibido | escolha `e` ou `ou`; se inclusivo mesmo: `A, B, ou os dois` |

## Siglas

- **Gênero e artigo fixos no glossário do projeto.** `a API`, `a URL`, `a VPN`, `o endpoint`, `o commit`. Consistência importa mais que estar "certo" — decida uma vez e congele.
- **Plural sem apóstrofo.** `APIs`, `CDs`, `PRs`. Nunca `API's` — em português o apóstrofo marca elisão (`pau-d'água`), não plural.
- **Expanda na primeira ocorrência** e só então use a sigla: "Interface de Programação de Aplicações (API)".
- Sigla que já entrou na língua como palavra comum não precisa de expansão (`CPF`, `PDF`, `URL`).
