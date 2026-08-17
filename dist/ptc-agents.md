# Português Técnico Controlado (PTC)

Reescreve texto técnico em português do Brasil para ter uma leitura só — tira sujeito oculto, -se apassivador, modal que é obrigação e probabilidade ao mesmo tempo, e escopo decidido por vírgula. Congela terminologia, formato de número e data, e ortografia. Gera par EN/PT quando preciso.

Salve este arquivo como `AGENTS.md` na raiz do seu projeto. Codex, opencode, Jules e Aider o leem automaticamente; o Gemini CLI espera o mesmo conteúdo em `GEMINI.md`.

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
3. **Bilíngue?**: se sim, carregue a seção "Lado inglês e pipeline bilíngue" **antes** de mexer no texto — o pipeline tem ordem obrigatória e refazer custa caro.

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

Fora dessas quatro, **não deduza** — as demais situações estão na seção "Ortografia PT-BR — Acordo de 1990", "Hífen com prefixo": vogal igual ou `h` depois do prefixo (`anti-inflamatório`, `super-homem`), prefixo terminado em consoante (`inter-relação`, mas `superusuário`), `sub-` + b/h/r (`sub-rotina`), e `não` + substantivo, que perdeu o hífen com o Acordo (`não conformidade`).

Também: trema abolido (`frequência`, `sequência`, `bilíngue`); ditongo aberto em paroxítona sem acento (`ideia`, `assembleia`, `heroico`); sem circunflexo em `oo`/`ee` (`voo`, `leem`, `creem`, `veem`); diferenciais abolidos (`para`, `pelo`, `polo`, `pera`) mas **mantidos** `pôr` e `pôde`.

Casos de detalhe, armadilhas de TI e a lista do que **não** é erro: **a seção "Ortografia PT-BR — Acordo de 1990"**. Em dúvida de grafia, consulte o VOLP — não deduza.

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
3. **Se for bilíngue**, carregue a seção "Lado inglês e pipeline bilíngue" agora e siga o pipeline de lá — a ordem é obrigatória.
4. **Varra frase a frase**, marcando qual regra PTC cada trecho viola.
5. **Reescreva cada trecho marcado**, preservando o sentido exato. Se a reescrita fosse custar precisão — uma condição de segurança, um qualificador de escopo, um número — **mantenha o texto longo e sinalize** em vez de simplificar em silêncio.
6. **Consulte as referências** quando a dúvida for de grafia (a seção "Ortografia PT-BR — Acordo de 1990") ou de palavra (a seção "Léxico controlado PT-BR"). Não chute grafia.
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

No modo bilíngue, acrescente a tabela de proposições e — se o linter reverso disparou — a lista de ambiguidades que a fonte teve que resolver. Ver a seção "Lado inglês e pipeline bilíngue".

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

- **a seção "Léxico controlado PT-BR"** — evite→use, conectores ambíguos, variante BR, siglas
- **a seção "Ortografia PT-BR — Acordo de 1990"** — Acordo de 1990 em detalhe, armadilhas de TI, o que não é erro
- **a seção "Lado inglês e pipeline bilíngue"** — regras do lado inglês, pipeline bilíngue, tabela de proposições, decalques EN→PT


---

# Lado inglês e pipeline bilíngue

Carregue este arquivo **antes** de mexer no texto quando o entregável precisar existir nos dois idiomas. O pipeline tem ordem obrigatória e refazer custa caro.

## Regras do inglês controlado

Estas regras parafraseiam as **categorias** do ASD-STE100 (Simplified Technical English), padrão público da ASD — AeroSpace and Defence Industries Association of Europe. Issue 9, janeiro de 2025: 53 regras em 9 seções, mais um dicionário de ~900 palavras aprovadas e ~1.200 a evitar.

> **O que esta skill não faz:** não reproduz o dicionário de ~900 palavras. Esse é o download oficial da ASD, gratuito em <https://www.asd-ste100.org/>. Aqui aplicamos o **princípio** — a palavra mais simples disponível, sempre usada do mesmo jeito — em vez de checar contra lista fixa. Para documentação aeroespacial certificada, a fonte de verdade é o padrão oficial, não esta skill.

### Escolha de palavra
- Uma palavra, um significado. Não conte com o contexto para desambiguar uma palavra que tem várias acepções de dicionário.
- Uma classe gramatical por palavra. `Apply oil to the valve` (substantivo), não `Oil the valve` (verbo).
- Prefira a palavra mais comum e mais curta à formal ou rara. `Obey the safety instructions`, não `Follow` — `follow` também significa "vir depois".

### Formas verbais
- **Permitidas:** infinitivo, imperativo, presente simples, passado simples, futuro simples, e particípio passado **só como adjetivo**.
- **Proibidas:** present perfect, past perfect, e demais construções compostas. `We received the report`, nunca `We have received the report`.
- **`-ing` só como substantivo técnico** ou parte dele, nunca como forma verbal.

### Voz
- Voz ativa obrigatória em procedimento e instrução.
- Passiva só em texto descritivo, e só quando o agente for genuinamente desconhecido ou irrelevante.

### Estrutura da frase
- Uma instrução por frase.
- **≤ 20 palavras** em procedimento; **≤ 25** em texto descritivo.
- **Cluster nominal ≤ 3 palavras.** `fuel pump valve` passa; `high pressure fuel pump inlet valve assembly` não.
- **Sem elipse.** Não omita sujeito, verbo ou artigo para encurtar — o padrão avisa explicitamente que isso cria ambiguidade em vez de clareza.

### Parágrafo e documento
- Um tópico por parágrafo, **≤ 6 frases**.
- Lista vertical (numerada ou com marcadores) para sequência, condição ou enumeração — nunca enterrada em prosa.
- Instrução de segurança abre com o comando ou a condição, nunca no meio da frase.

## Pipeline bilíngue

Ordem serial obrigatória. **Não normalize os dois idiomas em paralelo** a partir do original bruto — cada conjunto de regras puxa para um lado e as duas versões passam a afirmar coisas diferentes. Esse é o risco maior, mais do que o round-trip.

1. **Reescreva na língua fonte**, sob as regras dela. A fonte é sempre **o idioma do input**: texto em inglês → regras STE acima; texto em português → as 8 regras PTC. Esse texto vira a verdade.
2. **Traduza o texto já controlado** — nunca o original bruto.
3. **Aplique as regras da língua alvo** só onde não alterem a proposição.

**Nunca faça round-trip** (`PT → EN → PT`). Cada tradução reintroduz exatamente a ambiguidade que o controle acabou de remover.

### O português funciona como linter do inglês

O ponto que justifica o desenho inteiro.

Se no passo 3 uma regra do português exigir informação que o inglês não tinha — a PTC-1 obriga nomear um ator que o inglês deixou implícito, a PTC-3 obriga decidir se `should` é obrigação ou expectativa — **isso não é problema de tradução. É ambiguidade não resolvida na fonte.**

Volte ao passo 1 e corrija o inglês. É o único mecanismo que impede o tradutor de inventar o ator.

> **EN fonte:** `The report should be sent after validation.`
> PTC-1 pergunta: quem envia? PTC-3 pergunta: `should` é obrigação ou estimativa?
> **→ corrige a fonte:** `The scheduler sends the report after the gateway validates the token.`
> **→ PT:** `O agendador envia o relatório depois que o gateway valida o token.`

Registre na saída toda ambiguidade que o linter reverso encontrou. É informação de valor: mostra onde o texto original mentia por omissão.

## Checagem de equivalência

Não peça a si mesmo "verifique se estão equivalentes" — não é acionável. Extraia uma **tabela de proposições de cada versão de forma independente** e compare célula a célula:

| # | ator | ação | objeto | condição | resultado/erro | valor+unidade | modalidade |
|---|---|---|---|---|---|---|---|
| 1 | scheduler / agendador | send / enviar | report / relatório | after validation | — | — | obrigação |

**Falha se:**
- qualquer célula existe numa versão e não na outra, ou diverge;
- a contagem de passos imperativos difere;
- a contagem de condições difere;
- a contagem de valores numéricos difere;
- um termo do glossário foi traduzido de um jeito numa ocorrência e de outro em outra.

Em `estrito`, exija **alinhamento 1:1 de frase e mesma ordem**, para que o diff seja revisável por humano. Em `leve`, permita recomposição.

Comprimento **não** precisa bater. Não force paridade de contagem de palavras.

## O que não se traduz

Copiar literalmente:
- identificadores, nomes de variável e de campo
- flags de CLI e parâmetros
- strings de log e códigos de erro
- nomes de arquivo e de caminho

**Rótulo de interface:** use o rótulo real do produto localizado. Nunca invente tradução. Se o produto não é localizado, mantenha em inglês e não flexione.

## O que não se copia

Único lugar onde copiar é **errado** — ver PTC-7:

| | PT-BR | EN |
|---|---|---|
| Decimal | `1,5 GB` | `1.5 GB` |
| Milhar | `1.000` | `1,000` |
| Data | `2026-08-02` | `2026-08-02` *(ISO nos dois)* |
| Hora | `14h30` | `2:30 PM` |

## Decalques a evitar

O tradutor literal reproduz a sintaxe inglesa e o texto fica ambíguo em português.

### Sintaxe

| EN | Decalque ❌ | PT ✅ |
|---|---|---|
| `Make sure the service is running.` | Faça certeza de que... | Confirme que o serviço está ativo. |
| `Once the job finishes...` | Uma vez que o job termina... | Quando o job termina... |
| `task queue priority handler` | manipulador de prioridade de fila de tarefas *(4 nós)* | O handler define a prioridade da fila. |
| `Run X, generating Y` | Execute X, gerando Y | Execute X para gerar Y. |
| `you should` | você deveria | *(obrigação)* Faça X. / *(recomendação)* Recomendamos X. |

O terceiro caso é o mais importante: **cluster nominal inglês não vira cadeia de `de` em português.** A PTC-5 limita a cadeia a 2 nós, então o cluster precisa virar oração.

### Falsos amigos

| EN | Decalque ❌ | PT ✅ |
|---|---|---|
| `actually` | atualmente | na verdade |
| `eventually` | eventualmente | por fim / no final |
| `realize` | realizar | perceber |
| `comprehensive` | compreensivo | abrangente |
| `consistent` | consistente | coerente / constante |
| `requirement` | requerimento | requisito |
| `support` | suportar | oferece suporte a / aceita |
| `deprecated` | depreciado | descontinuado |
| `library` | livraria | biblioteca |
| `address` *(an issue)* | endereçar | resolver / tratar |
| `assist` | assistir | ajudar |
| `notice` | notícia | aviso / perceber |
| `parents` | parentes | pais |
| `push` *(git)* | empurrar | enviar / publicar |

## Fator de expansão

Do inglês para o português: **~20-25% em caracteres**, mas só **~10-15% em palavras**. O português contrai preposição + artigo (`of the` → `do`, `to the` → `ao`) e não tem phrasal verb (`turn on` → `ligar`).

Como o limite do STE é em palavras, 20 × 1,15 daria ~23. A folga até 25 na PTC-5 se justifica por outra causa: **desfazer cluster nominal é o verdadeiro expansor.**

> `database connection timeout` *(3 palavras)* → `tempo limite de conexão do banco de dados` *(8 palavras)*

É a própria PTC-5 que força essa expansão. Por isso o limite em português é 25/30, e não 20/25.

## Fontes

- [ASD-STE100 — site oficial](https://www.asd-ste100.org/) · [FAQ](https://asd-ste100.org/STE_faq.html)
- [ASD Europe — Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- [O'Brien, "Controlled Language and Readability"](https://doras.dcu.ie/17153/1/OBrien_CL_and_Readability.pdf) — Dublin City University; estudo com eye-tracking sobre o efeito real de linguagem controlada na legibilidade e na tradução automática


---

# Léxico controlado PT-BR

Aplicado em `estrito` e `descritivo`. **Dispensado em `leve`** — comunicado interno não precisa disso e fica pior com isso.

Não existe dicionário oficial de português controlado (ver `SKILL.md`, "Por que não é o STE traduzido"). Esta lista ataca os vícios reais do português corporativo brasileiro, não o vocabulário geral.

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

## Variante brasileira

O Acordo de 1990 unificou a **ortografia**, não o **léxico**. As formas da coluna direita **não são erros** — são português europeu. Fixamos a variante BR por consistência; nunca marque a outra como incorreta.

### Léxico

| PT-BR *(use)* | PT-PT |
|---|---|
| arquivo | ficheiro |
| usuário | utilizador |
| tela | ecrã |
| mouse | rato |
| equipe / time | equipa |
| celular | telemóvel |
| cadastro | registo |
| aplicativo | aplicação |
| gerenciar | gerir |
| planilha | folha de cálculo |

### Ortografia que difere entre as variantes

Divergências fonéticas que o Acordo preservou de propósito — refletem pronúncia real diferente, não erro.

| PT-BR *(use)* | PT-PT |
|---|---|
| contato | contacto |
| registro | registo |
| setor | sector |
| recepção | receção |
| fato | facto |
| acadêmico | académico |
| econômico | económico |
| gênero | género |

Regra prática: onde o Brasil pronuncia a consoante, o Brasil a escreve. E o timbre tônico brasileiro é fechado (circunflexo), o europeu é aberto (agudo).

## Siglas

- **Gênero e artigo fixos no glossário do projeto.** `a API`, `a URL`, `a VPN`, `o endpoint`, `o commit`. Consistência importa mais que estar "certo" — decida uma vez e congele.
- **Plural sem apóstrofo.** `APIs`, `CDs`, `PRs`. Nunca `API's` — em português o apóstrofo marca elisão (`pau-d'água`), não plural.
- **Expanda na primeira ocorrência** e só então use a sigla: "Interface de Programação de Aplicações (API)".
- Sigla que já entrou na língua como palavra comum não precisa de expansão (`CPF`, `PDF`, `URL`).

## Glossário do projeto

O ASD-STE100 permite que cada organização defina o próprio dicionário de termos técnicos além da base. Aqui é o mesmo mecanismo, e é o único jeito honesto de lidar com vocabulário de domínio.

Ao trabalhar num projeto com termos recorrentes, mantenha uma tabela no próprio repositório:

```markdown
| Termo PT | Termo EN | Gênero/artigo | Definição em 1 linha | Não usar |
|---|---|---|---|---|
| corretor | broker | o corretor | Pessoa que intermedeia a negociação | agente, vendedor |
| imóvel | property | o imóvel | Unidade cadastrada com endereço | propriedade, item |
```

A coluna **"Não usar"** é a que mais paga: é ela que impede o texto de rodar sinônimos para o mesmo conceito, que é exatamente o que a PTC-6 proíbe.


---

# Ortografia PT-BR — Acordo de 1990

Carregue este arquivo quando a dúvida for de **grafia**. Para reescrita de sintaxe, o `SKILL.md` basta.

## Status

- Assinado em Lisboa em 1990-12-16. No Brasil, regulamentado pelo **Decreto nº 6.583/2008**.
- Período de transição de 2009 a 2012, **prorrogado duas vezes** até 2015-12-31.
- **Obrigatório no Brasil desde 2016-01-01.**
- **Fonte autoritativa: o VOLP** (Vocabulário Ortográfico da Língua Portuguesa) da Academia Brasileira de Letras — hoje só online, em <https://www.academia.org.br/nossa-lingua/busca-no-vocabulario>. Não tem API pública. **Em dúvida, consulte. Não deduza.**
- O VOLP define **grafia**, não significado. Para significado, use Houaiss/Michaelis.

> O Acordo unificou a **ortografia**, não o **léxico**. `utilizador`, `ecrã` e `ficheiro` continuam sendo português europeu correto. Ver a seção "Variante brasileira" na seção "Léxico controlado PT-BR".

## Hífen com prefixo

Onde o vocabulário de TI mais erra. Aplique na ordem:

### 1. Prefixo termina em vogal + palavra começa com R ou S → junta e **dobra** a consoante

A regra mais violada em texto técnico brasileiro.

`microsserviço` · `autosserviço` · `antirracismo` · `antissemita` · `antirreligioso` · `contrarregra` · `semirreta` · `minissaia` · `ultrassom` · `microssistema`

### 2. Prefixo termina em vogal + palavra começa com vogal **diferente** → junta

`infraestrutura` · `autoescola` · `autoafirmação` · `extraescolar` · `extraoficial` · `contraexemplo` · `semiaberto` · `semiautomático` · `multiusuário` · `multiplataforma` · `multitarefa` · `interoperabilidade`

### 3. Prefixo termina em vogal + palavra começa com a **mesma** vogal, ou com H → hífen

`anti-inflamatório` · `arqui-inimigo` · `auto-observação` · `contra-almirante` · `anti-higiênico` · `anti-herói` · `super-homem` · `extra-humano`

### 4. `co-` e `re-` juntam **sempre** — mesmo com vogal igual, mesmo com H

Exceção lexicalizada, unânime no VOLP.

`coautor` · `coobrigação` · `cooperar` · `coordenar` · `coprocessador` · `cosseno` · `coabitar`
`reescrever` · `reeleição` · `reenviar` · `reeditar` · `reencontro` · `reindexação`

> Não existe prefixo `ré-` em português. `ré-indexação` está errado — é `reindexação`.

### 5. `pré-`, `pós-`, `pró-` tônicos → hífen **sempre**

`pré-requisito` · `pré-processamento` · `pré-produção` · `pós-processamento` · `pós-venda` · `pró-ativo`

### 6. Prefixo termina em consoante

- **Mesma consoante depois → hífen:** `inter-relação` · `inter-relacionamento` · `inter-racial` · `hiper-resistente` · `super-realista`
- **Letra diferente → junta:** `superusuário` · `superproteção` · `hipermercado` · `intermunicipal` · `interdependência`
- **`sub-` + b, h ou r → hífen:** `sub-rotina` · `sub-região` · `sub-base`. Fora disso junta: `subaquático`, `subsolo`, `subemprego`. Com `h` é facultativo (`subumano` e `sub-humano` ambos registrados).

### 7. Prefixos que sempre levam hífen

`ex-` (`ex-diretor`), `vice-` (`vice-presidente`), `sota-`, `soto-`, `vizo-`.

Por uso consagrado nas gramáticas e no VOLP: `além-`, `aquém-`, `recém-` (`recém-criado`, `recém-implantado`). *Convenção adotada — não confirmei menção literal desses três na Base XVI do texto normativo.*

### 8. `não` + substantivo → **sem** hífen

Mudou com o Acordo. `não conformidade` · `não fumante` · `não governamental`.

## Acentuação

| Mudança | Antes | Agora |
|---|---|---|
| Trema abolido | `freqüência`, `seqüência`, `lingüiça`, `bilíngüe`, `tranqüilo` | `frequência`, `sequência`, `linguiça`, `bilíngue`, `tranquilo` |
| Ditongo aberto `éi`/`ói` em **paroxítona** | `idéia`, `assembléia`, `heróico`, `jibóia`, `geléia` | `ideia`, `assembleia`, `heroico`, `jiboia`, `geleia` |
| Circunflexo em `oo`/`ee` de paroxítona | `vôo`, `enjôo`, `lêem`, `crêem`, `vêem` | `voo`, `enjoo`, `leem`, `creem`, `veem`, `deem` |

**Trema mantido** só em nome próprio estrangeiro e derivados: `Müller`, `mülleriano`, `Bündchen`.

**Ditongo aberto em oxítona mantém acento:** `herói`, `papéis`, `constrói`, `dói`. A regra só derrubou o acento das paroxítonas.

### Acentos diferenciais

**Abolidos:** `para` (verbo, era `pára`) · `pelo` (era `pêlo`) · `polo` (era `pólo`) · `pera` (era `pêra`).

**Mantidos:** `pôr` (verbo) vs `por` (preposição) · `pôde` (pretérito) vs `pode` (presente).

**Facultativo:** `fôrma` vs `forma`, quando houver ambiguidade real na mesma frase.

**Não confundir:** `têm`/`tem` e `vêm`/`vem` (3ª pessoa do plural vs singular) **continuam acentuados** — mas isso não é acento diferencial abolido, é a regra de plural em `-em`, que sempre existiu e permanece. Vale para `contêm`/`contém`, `mantêm`/`mantém`, `provêm`/`provém`.

## Alfabeto

`K`, `W` e `Y` foram oficialmente incorporados — 26 letras. Usados em siglas, símbolos, unidades e estrangeirismos: `km`, `W`, `byte`, `playground`.

## Armadilhas de TI

Grafia correta dos termos que mais aparecem errados em documentação técnica brasileira:

| Errado | Correto | Regra |
|---|---|---|
| micro-serviço, microserviço | **microsserviço** | vogal + s → dobra |
| infra-estrutura | **infraestrutura** | vogal + vogal diferente |
| auto-serviço | **autosserviço** | vogal + s → dobra |
| multi-usuário, multi-plataforma | **multiusuário**, **multiplataforma** | vogal + vogal diferente |
| semi-automático | **semiautomático** | vogal + vogal diferente |
| super-usuário | **superusuário** | consoante + letra diferente |
| subrotina | **sub-rotina** | `sub-` + r |
| co-autor, co-processador | **coautor**, **coprocessador** | `co-` junta sempre |
| ré-indexação, re-indexação | **reindexação** | `re-` junta sempre |
| inter-operabilidade | **interoperabilidade** | consoante + vogal |
| interrelação | **inter-relação** | consoante + mesma consoante |
| não-conformidade | **não conformidade** | `não` perdeu o hífen |
| API's, PR's | **APIs**, **PRs** | apóstrofo não marca plural |
| freqüência | **frequência** | trema abolido |
| idéia | **ideia** | ditongo em paroxítona |

## O que NÃO é erro

Não marque estes como incorretos. São **convenção de estilo** — fixe uma escolha no projeto, documente, e siga.

- **`front-end` / `frontend`**, **`back-end` / `backend`**, **`full-stack` / `fullstack`**, **`data center` / `datacenter`** — empréstimos ingleses não vernaculizados. O VOLP não hifeniza esses termos; não são prefixação portuguesa. As duas formas circulam em publicações técnicas brasileiras.
- **`antispam` vs `antisspam`** — sem grafia pacífica. O VOLP registra `antispam`; a regra estrita do r/s daria `antisspam`. Sinalize a divergência, não "corrija".
- **`micro-ondas`** — grafia consagrada, registrada assim. **Não generalize a partir dela** para deduzir outros casos com `micro-`.
- **`e-mail` vs `email`** — `e-mail` é a forma registrada no VOLP e a recomendada em texto formal; `email` circula amplamente e é aceito por dicionários portugueses.
- **`corrotina`** (coroutine) — neologismo não dicionarizado. Grafado por analogia à regra do r/s.
- **`software`, `hardware`, `site`, `web`** — estrangeirismos já incorporados e dicionarizados. Sem itálico obrigatório. Plural à portuguesa: `softwares`, `sites`.
- **Variantes de PT-PT** (`utilizador`, `ecrã`, `ficheiro`) — português europeu correto. Ver a seção "Léxico controlado PT-BR".

## Estrangeirismos

Não existe orientação normativa da ABL nem norma ABNT dedicada a como grafar estrangeirismo em documentação técnica de TI. *(Procurei e não encontrei — a convenção de itálico vem de prática em trabalhos acadêmicos, não de cláusula numerada que eu possa citar.)* Trate como decisão editorial do projeto:

- Estrangeirismo **dicionarizado** (`software`, `site`, `mouse`, `deletar`): escreva normal, sem itálico, plural à portuguesa.
- Estrangeirismo **não incorporado** (`deployar`, `startar`, `commitar`): são gíria técnica oral. Em texto controlado, prefira o verbo português — `implantar`, `iniciar`, `versionar`. É a PTC-6 aplicada.
- **Identificador de código nunca é traduzido nem flexionado** — nome de flag, campo, arquivo, código de erro. Ver a seção "Lado inglês e pipeline bilíngue".

## Verificação automatizada

Fora de escopo desta skill, mas se a lista curada acima se mostrar insuficiente:

- **Hunspell pt-BR** — ortografia, via CLI: `hunspell -d pt_BR arquivo.txt`
- **LanguageTool** — gramática e estilo, com API REST, distingue as variantes pt-BR e pt-PT
- O **VOLP não tem API** — só consulta manual pela web
