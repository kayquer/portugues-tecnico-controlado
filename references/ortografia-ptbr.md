# Ortografia PT-BR — Acordo de 1990

Carregue este arquivo quando a dúvida for de **grafia**. Para reescrita de sintaxe, o `SKILL.md` basta.

## Status

- Assinado em Lisboa em 1990-12-16. No Brasil, regulamentado pelo **Decreto nº 6.583/2008**.
- Período de transição de 2009 a 2012, **prorrogado duas vezes** até 2015-12-31.
- **Obrigatório no Brasil desde 2016-01-01.**
- **Fonte autoritativa: o VOLP** (Vocabulário Ortográfico da Língua Portuguesa) da Academia Brasileira de Letras — hoje só online, em <https://www.academia.org.br/nossa-lingua/busca-no-vocabulario>. Não tem API pública. **Em dúvida, consulte. Não deduza.**
- O VOLP define **grafia**, não significado. Para significado, use Houaiss/Michaelis.

> O Acordo unificou a **ortografia**, não o **léxico**. `utilizador`, `ecrã` e `ficheiro` continuam sendo português europeu correto. Ver a seção "Variante brasileira" em `lexico.md`.

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
- **Variantes de PT-PT** (`utilizador`, `ecrã`, `ficheiro`) — português europeu correto. Ver `lexico.md`.

## Estrangeirismos

Não existe orientação normativa da ABL nem norma ABNT dedicada a como grafar estrangeirismo em documentação técnica de TI. *(Procurei e não encontrei — a convenção de itálico vem de prática em trabalhos acadêmicos, não de cláusula numerada que eu possa citar.)* Trate como decisão editorial do projeto:

- Estrangeirismo **dicionarizado** (`software`, `site`, `mouse`, `deletar`): escreva normal, sem itálico, plural à portuguesa.
- Estrangeirismo **não incorporado** (`deployar`, `startar`, `commitar`): são gíria técnica oral. Em texto controlado, prefira o verbo português — `implantar`, `iniciar`, `versionar`. É a PTC-6 aplicada.
- **Identificador de código nunca é traduzido nem flexionado** — nome de flag, campo, arquivo, código de erro. Ver `ingles.md`.

## Verificação automatizada

Fora de escopo desta skill, mas se a lista curada acima se mostrar insuficiente:

- **Hunspell pt-BR** — ortografia, via CLI: `hunspell -d pt_BR arquivo.txt`
- **LanguageTool** — gramática e estilo, com API REST, distingue as variantes pt-BR e pt-PT
- O **VOLP não tem API** — só consulta manual pela web
