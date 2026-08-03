---
name: portugues-tecnico-controlado
description: "Reescreve texto técnico em português do Brasil controlado — sem ambiguidade, com ortografia do Acordo de 1990 e terminologia congelada. Gera par EN/PT quando preciso. Triggers - 'português controlado', 'PTC', 'tira a ambiguidade', 'simplifica esse procedimento', 'reescreve esse runbook', 'versão em EN e PT', 'revisa esse comunicado', 'linguagem controlada'."
version: 1.0.0
---

<!--
AVISO PARA QUEM VAI EDITAR ESTE ARQUIVO — não para quem está aplicando as regras.
Se você está reescrevendo um texto do usuário, ignore este bloco e siga as regras abaixo.
Se você está EDITANDO esta skill: os exemplos marcados ❌ contêm português errado
DE PROPÓSITO — eles ensinam a regra. Não os "corrija". Leia AGENTS.md antes.
-->

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
3. **Bilíngue?**: se sim, carregue `references/ingles.md` **antes** de mexer no texto — o pipeline tem ordem obrigatória e refazer custa caro.

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

> ❌ Envia o e-mail e atualiza o status. *(quem?)*
> ⚠️ O serviço envia o e-mail e o serviço atualiza o status. *(explicitação idiota)*
> ✅ O serviço envia o e-mail e atualiza o status. *(mesmo ator)*
> ✅ O serviço envia o e-mail. O worker atualiza o status. *(atores diferentes)*

> ❌ A configuração usa o certificado padrão. Ele expira em 90 dias. *("ele" = certificado ou a configuração?)*
> ✅ A configuração usa o certificado padrão. O certificado expira em 90 dias.

Argumento extra para banir o `-se`: ele colide com o `se` condicional na mesma frase.

> ❌ Se o arquivo existe, faz-se o backup.
> ✅ Se o arquivo existe, o agendador cria o backup.

### PTC-2 — Uma proposição por frase, uma forma verbal

- **Instrução ao leitor:** imperativo na forma "você" (`Clique`, `Faça`, `Vá`). Proibido `tu` (`Clica`), infinitivo (`Clicar em Salvar`), `deve-se`, `por favor`, `poderia`.
- **Descrição de comportamento** (tool description, docstring): presente do indicativo, 3ª pessoa. `Retorna a lista de pedidos abertos.` Nunca `Retornar` nem `Use isto para retornar`.
- **Nunca misture** imperativo e infinitivo na mesma lista. É o erro mais comum em runbook brasileiro.
- **Sem gerúndio conector.** Gerúndio só em perífrase durativa com `estar` e sujeito explícito (`O job está processando os registros`). Nunca ligando duas orações.
- **Sem relativa explicativa** (a com vírgula) em modo estrito. A vírgula muda o escopo de forma invisível. Se a informação é adicional, vira frase separada.

> ❌ Execute o script, gerando o relatório. *(simultâneo? consequência? finalidade?)*
> ✅ Execute o script para gerar o relatório. *(finalidade)*
> ✅ Execute o script. O script gera o relatório. *(consequência)*

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

> ❌ O processo deve terminar em 5 minutos. *(regra ou estimativa?)*
> ✅ O processo termina em até 5 minutos. *(estimativa)*
> ✅ Encerre o processo em até 5 minutos. *(obrigação)*

### PTC-4 — Verbo pleno, não verbo-suporte

O alvo é a construção com **verbo leve** — `fazer`/`realizar`/`efetuar`/`proceder a`/`executar`/`promover` + nominalização. Não é a nominalização em si.

> ❌ Realize a validação dos dados de entrada. → ✅ Valide os dados de entrada.

**Nominalização legítima permanece.** `A validação de entrada rejeita CPFs inválidos` está correto — ali o substantivo é o termo do domínio. Não mexa.

### PTC-5 — Sintaxe plana

- **Adjetivo sempre depois do substantivo.** Em português, antepor muda o sentido: `um simples teste` (só um teste) ≠ `um teste simples` (de baixa complexidade). Também `certo procedimento`/`procedimento certo`, `único usuário`/`usuário único`, `nova versão`/`versão nova`. Se o sentido pretendido era o anteposto, use outra palavra: `apenas um teste`, `o procedimento correto`.
- **Cadeia de `de`/`em`/`para` ≤ 2 nós.** Termo lexicalizado conta como **um** nó (`banco de dados`, `chave de API`, `tempo de resposta`, `fila de mensagens`).
- **Nada entre verbo e objeto.** Circunstância vai no início (se for condição ou gatilho) ou no fim (se for meio ou local). Nunca no meio.
- **Modificador sobre coordenação, repetido.** `os relatórios e planilhas antigos` é ambíguo → `os relatórios antigos e as planilhas antigas`.
- **≤ 25 palavras** (procedimento) / **≤ 30** (descritivo) — **e no máximo uma subordinada por frase** em modo estrito.

> ❌ a validação do cadastro do cliente do contrato *(3 leituras)*
> ✅ Valide o cadastro. Esse cadastro pertence ao cliente do contrato.

> ❌ Envie, após validar o token e confirmar o escopo, o pacote ao servidor.
> ✅ Valide o token. Confirme o escopo. Envie o pacote ao servidor.

O limite de palavras é só o proxy verificável — 25 palavras cabem duas subordinadas encaixadas. O cap estrutural de **uma subordinada** é o que de fato desambigua.

### PTC-6 — Termos congelados, variante BR

- **Um conceito, um termo, sempre o mesmo** — inclusive dos dois lados do par bilíngue.
- **Sigla com gênero e artigo fixos** no glossário do projeto (`a API`, `a URL`, `o endpoint`). Consistência importa mais que estar "certo". Plural sem apóstrofo: `APIs`, nunca `API's`. Expanda na primeira ocorrência.
- **Fixe a variante brasileira**: `arquivo` (não `ficheiro`), `usuário` (não `utilizador`), `tela` (não `ecrã`), `mouse` (não `rato`), `equipe`/`time` (não `equipa`), `cadastro` (não `registo`), `aplicativo` (não `aplicação`).
- Aplique o léxico evite→use, os conectores ambíguos e o glossário de siglas: **`references/lexico.md`**.

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

O hífen com prefixo é onde o vocabulário de TI mais erra:

| Situação | Grafia | Exemplo |
|---|---|---|
| prefixo em vogal + **r/s** | junta e **dobra** a consoante | `microsserviço`, `autosserviço`, `antirracismo` |
| prefixo em vogal + vogal **diferente** | junta | `infraestrutura`, `extraescolar`, `multiusuário` |
| prefixo em vogal + vogal **igual** ou **h** | hífen | `anti-inflamatório`, `anti-higiênico`, `super-homem` |
| `co-`, `re-` | juntam **sempre** | `coautor`, `coprocessador`, `reescrever`, `reindexação` |
| `pré-`, `pós-`, `pró-` tônicos | hífen **sempre** | `pré-requisito`, `pós-processamento` |
| prefixo em consoante + **mesma** consoante | hífen | `inter-relação`, `hiper-resistente` |
| prefixo em consoante + outra letra | junta | `superusuário`, `interoperabilidade` |
| `sub-` + b/h/r | hífen | `sub-rotina`, `sub-região` |
| `não` + substantivo | **sem** hífen (mudou) | `não conformidade` |

Também: trema abolido (`frequência`, `sequência`, `bilíngue`); ditongo aberto em paroxítona sem acento (`ideia`, `assembleia`, `heroico`); sem circunflexo em `oo`/`ee` (`voo`, `leem`, `creem`, `veem`); diferenciais abolidos (`para`, `pelo`, `polo`, `pera`) mas **mantidos** `pôr` e `pôde`.

Casos de detalhe, armadilhas de TI e a lista do que **não** é erro: **`references/ortografia-ptbr.md`**. Em dúvida de grafia, consulte o VOLP — não deduza.

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

> ❌ `Arquivo enviado.` *(evento concluído ou propriedade do estado?)*
> ✅ `O agente enviou o arquivo.` *(evento)*
> ✅ `O arquivo está no estado ENVIADO.` *(propriedade)*

## Processo

1. **Leia o texto inteiro** antes de reescrever qualquer coisa. Você precisa saber o que ele ainda tem que dizer depois.
2. **Fixe os parâmetros** do Passo 0. Declare o que assumiu.
3. **Se for bilíngue**, carregue `references/ingles.md` agora e siga o pipeline de lá — a ordem é obrigatória.
4. **Varra frase a frase**, marcando qual regra PTC cada trecho viola.
5. **Reescreva cada trecho marcado**, preservando o sentido exato. Se a reescrita fosse custar precisão — uma condição de segurança, um qualificador de escopo, um número — **mantenha o texto longo e sinalize** em vez de simplificar em silêncio.
6. **Consulte as referências** quando a dúvida for de grafia (`ortografia-ptbr.md`) ou de palavra (`lexico.md`). Não chute grafia.
7. **Se o texto já estiver conforme, diga isso.** Não force mudança em texto que já está bom.

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

No modo bilíngue, acrescente a tabela de proposições e — se o linter reverso disparou — a lista de ambiguidades que a fonte teve que resolver. Ver `references/ingles.md`.

## Por que não é o STE traduzido

Traduzir as 53 regras do ASD-STE100 uma a uma não funciona, por duas razões simétricas:

**Regras que viram vazias em português.** "Uma classe gramatical por palavra" existe porque em inglês `oil` é substantivo e verbo sem mudar de forma. Em português a morfologia já separa `óleo`/`lubrificar` — a regra não paga nada. "Cluster nominal ≤3" também quase não se aplica: o português transforma pilha de substantivos em sintagma preposicionado, e o problema migra para a cadeia de `de` (PTC-5).

**Vícios do português que o STE não cobre.** O inglês obriga o sujeito, então o STE nunca precisou de uma regra para isso — enquanto em português o sujeito nulo é a maior fonte de ambiguidade que existe (PTC-1). O mesmo vale para o `-se` apassivador, a posição do adjetivo, o gênero gramatical criando correferência falsa, e a relativa explicativa distinguida só por vírgula.

Também não existe norma equivalente: **não há "Simplified Technical Portuguese"** — nem da ASD, nem da ABNT, nem da ABRAT. Só pesquisa acadêmica isolada (Gomes 2011, Univ. de Lisboa; UFSC 2014), sem adoção industrial. Esta skill não implementa uma norma; ela aplica o *princípio* da linguagem controlada às características reais do português.

Sobre a prática da indústria: a **Embraer escreve** a documentação dos E-Jets em Simplified English e o mercado brasileiro consome em inglês — não há evidência pública de um fluxo "escreve em STE, traduz para PT". O inglês ali é imposição regulatória (ICAO/ATA), não escolha de qualidade. E a alegação de que linguagem controlada melhora tradução é empiricamente modesta: O'Brien (Dublin City University, eye-tracking) mediu efeito real mas marginal, concentrado em textos já complexos — em alguns pares a tradução automática teve *mais* erros com as regras aplicadas.

## Limites

**Faz:**
- Reescreve texto em português para leitura única, marcando qual regra cada trecho violava.
- Preserva todo fato, condição e qualificador de escopo do original.
- Gera o par EN/PT com verificação de equivalência proposicional.
- Ajusta o rigor ao leitor, em vez de aplicar tudo sempre.

**Não faz:**
- Não reproduz o dicionário de ~900 palavras aprovadas da ASD — esse é o download oficial deles, em <https://www.asd-ste100.org/>. Esta skill aplica o princípio (a palavra mais simples disponível, sempre usada do mesmo jeito), não uma checagem contra lista fixa.
- Não entrega documentação aeroespacial certificada em STE. Para isso, o padrão oficial é a fonte de verdade, não esta skill.
- Não marca variante de português europeu como erro (ver PTC-6).
- Não trata convenção de estilo como norma — `front-end`/`frontend`, `data center`/`datacenter` e afins são escolha documentada, não erro ortográfico.
- Não simplifica texto criativo ou persuasivo.
- Não corta condição de segurança, exceção ou qualificador para encurtar frase — sinaliza o custo em vez disso.

## Referências

- **`references/lexico.md`** — evite→use, conectores ambíguos, variante BR, siglas
- **`references/ortografia-ptbr.md`** — Acordo de 1990 em detalhe, armadilhas de TI, o que não é erro
- **`references/ingles.md`** — regras do lado inglês, pipeline bilíngue, tabela de proposições, decalques EN→PT
