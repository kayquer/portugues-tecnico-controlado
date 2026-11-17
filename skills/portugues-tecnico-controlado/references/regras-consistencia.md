# Regras PTC-6 a PTC-9 — consistência e sinal

PTC-6 a PTC-8 são mecânicas: terminologia, formato e grafia. A PTC-9 tira o trecho que não carrega proposição. Resumo e ordem de uso no `SKILL.md`.

## PTC-6 — Termos congelados, variante BR

- **Um conceito, um termo, sempre o mesmo** — inclusive dos dois lados do par bilíngue.
- **Sigla com gênero e artigo fixos** no glossário do projeto (`a API`, `a URL`, `o endpoint`). Consistência importa mais que estar "certo". Plural sem apóstrofo: `APIs`, nunca `API's`. Expanda na primeira ocorrência.
- **Fixe a variante brasileira**: `arquivo` (não `ficheiro`), `usuário` (não `utilizador`), `tela` (não `ecrã`), `mouse` (não `rato`), `equipe`/`time` (não `equipa`), `cadastro` (não `registo`), `aplicativo` (não `aplicação`).
- Aplique o léxico evite→use, os conectores ambíguos e o glossário de siglas: **`references/lexico.md`**.

> **O Acordo de 1990 unificou a ortografia, não o léxico.** `utilizador` e `ecrã` **não são erros** — são português europeu. Esta skill *fixa* a variante BR por consistência de projeto. Nunca marque uma variante regional legítima como incorreta.

## PTC-7 — Formato de número, data e unidade

Aqui o erro não é de estilo, é **dado errado**.

- **Decimal:** vírgula em PT, ponto em EN. `1,5 GB` (PT) = `1.5 GB` (EN). Deixar `1.5` num texto PT lê-se como mil e quinhentos.
- **Milhar:** `1.000` (PT) vs `1,000` (EN) — inverso perfeito. Fonte de erro de ordem de grandeza 1000×.
- **Data: ISO 8601 (`2026-08-02`) nos dois idiomas.** `02/08/2026` é 2 de agosto em PT e 8 de fevereiro em EN. Se o contexto exigir extenso, escreva o mês por nome. Para converter, leia a data pela convenção do original: em texto PT, `02/08/2026` é DD/MM, logo `2026-08-02`. Se o original é EN, mistura as duas convenções ou vem de fonte desconhecida, não converta no chute: `[a confirmar: 02/08/2026 é 2 de agosto ou 8 de fevereiro?]`.
- **Hora:** 24 h, `14h30`. Nunca `2:30 PM` em PT.
- **Unidade:** espaço entre número e símbolo (`10 MB`, `200 ms`); símbolo nunca traduzido nem pluralizado (`5 kg`, não `5 kgs`).
- **Intervalo:** `de 10 a 20`, nunca `10-20` (colide com sinal de menos).

## PTC-8 — Ortografia PT-BR vigente

Acordo Ortográfico de 1990, **obrigatório no Brasil desde 2016-01-01** (Decreto 6.583/2008, transição prorrogada até 2015-12-31). Fonte autoritativa: **VOLP da Academia Brasileira de Letras**.

Quatro situações respondem por quase todo o erro de hífen em texto de TI:

| Situação | Grafia | Exemplo |
|---|---|---|
| prefixo em vogal + **r/s** | junta e **dobra** a consoante | `microsserviço`, `autosserviço`, `antirracismo` |
| prefixo em vogal + vogal **diferente** | junta | `infraestrutura`, `extraescolar`, `multiusuário` |
| `co-`, `re-` | juntam **sempre** | `coautor`, `coprocessador`, `reescrever`, `reindexação` |
| `pré-`, `pós-`, `pró-` tônicos | hífen **sempre** | `pré-requisito`, `pós-processamento` |

Fora dessas quatro, **não deduza** — as demais situações estão em `references/ortografia-ptbr.md`, "Hífen com prefixo": vogal igual ou `h` depois do prefixo (`anti-inflamatório`, `super-homem`), prefixo terminado em consoante (`inter-relação`, mas `superusuário`), `sub-` + b/h/r (`sub-rotina`), e `não` + substantivo, que perdeu o hífen com o Acordo (`não conformidade`).

Também: trema abolido (`frequência`, `sequência`, `bilíngue`); ditongo aberto em paroxítona sem acento (`ideia`, `assembleia`, `heroico`); sem circunflexo em `oo`/`ee` (`voo`, `leem`, `creem`, `veem`); diferenciais abolidos (`para`, `pelo`, `polo`, `pera`) mas **mantidos** `pôr` e `pôde`.

Casos de detalhe, armadilhas de TI e a lista do que **não** é erro: **`references/ortografia-ptbr.md`**. Em dúvida de grafia, consulte o VOLP — não deduza.

**Fronteira com a PTC-6.** Plural de sigla (`API's` → `APIs`), gênero e artigo de sigla e variante BR (`ficheiro` → `arquivo`) **parecem** ortografia e não são: rotule como **PTC-6**. Aqui só entra o que o Acordo de 1990 decide — hífen, acento, trema, grafia da palavra comum.

## PTC-9 — Sem ruído de texto gerado

Texto escrito por modelo tem vícios próprios, e nenhum deles cria duas leituras: eles ocupam espaço sem afirmar nada. O teste é um só: **se o trecho sai e nenhum fato, condição ou instrução se perde, ele é ruído.** O leitor de procedimento lê tudo, e cada frase vazia custa atenção que a condição de segurança da frase seguinte precisava.

**Sempre sai, nos três níveis:**
- **Artefato de chatbot e metatexto:** `Claro!`, `Ótima pergunta`, `Espero ter ajudado`, `Vamos lá`, `Neste documento, vamos explorar…`, `Fique à vontade para…`, `Em resumo, vimos que…`.
- **Aviso de limite do modelo:** `Com base nas informações disponíveis`, `Até onde sei`.
- **Conclusão genérica:** `O futuro é promissor`, `Só o tempo dirá`, `Uma coisa é certa`.

**Sai em `estrito` e `descritivo`, recomendado em `leve`:**
- **Transição de enchimento:** `Além disso`, `Ademais`, `Nesse sentido`, `Dessa forma` *(sem relação causal real)*, `Quando se trata de`, `No cenário atual`, `Em suma`. Se a frase seguinte já é a próxima ideia, o conector sai. Se ele diz uma relação lógica real, use o conector exato (`porque`, `por isso`, `mas`).
- **Calibração de confiança:** `Notavelmente`, `Curiosamente`, `Sem dúvida`, `De fato`, `Vale destacar que`. O fato não fica mais verdadeiro com o advérbio.
- **Atribuição vaga:** `Estudos mostram`, `Especialistas apontam`, `É sabido que`. Cite a fonte ou corte a atribuição. É a PTC-1 aplicada a quem afirma.
- **Evasão de cópula:** `atua como`, `se configura como`, `conta com`, `dispõe de`, `apresenta` *(no sentido de "tem")* → `é`, `tem`.
- **Inflação:** `robusto`, `abrangente`, `de ponta`, `sem atrito`, `alavancar`, `potencializar`, `divisor de águas`, `revolucionário`, `crucial`, `fundamental`. Troque por critério verificável (`aceita 10.000 requisições por segundo`) ou corte. Sem critério na fonte, não invente um: corte o adjetivo.
- **Contraste fabricado:** `Não é só X, é Y`, quando ninguém disse que era só X. Afirme Y.

> ❌ Além disso, vale destacar que a solução conta com uma arquitetura robusta de microsserviços que potencializa a escalabilidade.
> ✅ A solução tem arquitetura de microsserviços. *(o resto não afirmava nada que dê para conferir)*

> ❌ Ótima pergunta! Para reiniciar o serviço, execute o comando abaixo. Espero ter ajudado!
> ✅ Para reiniciar o serviço, execute o comando abaixo.

**Densidade, não caça à palavra.** Os itens de inflação e de transição viram violação pela recorrência ou pelo vazio, não pela presença. Um `Dessa forma` que marca consequência real fica, ou vira `Por isso`. Termo técnico também fica: `estimador robusto`, `teorema fundamental`, `cobertura abrangente de testes` quando o texto diz qual é a cobertura. Antes de cortar, faça o teste da regra: o que se perde?

**A própria saída da skill segue a PTC-9.** Nada de `Claro! Aqui está o texto revisado` antes da tabela, e nada de `Espero que ajude` depois do texto final. Negrito em frase inteira, emoji em título e título genérico (`Visão geral`, `Conclusão`) também ficam de fora do que a skill escreve.

**Fronteira com outras regras.** Rodízio de sinônimos para o mesmo conceito é **PTC-6**. Gerúndio em cadeia (`…, refletindo X e evidenciando Y`) é **PTC-2**. Hedge (`talvez`, `pode ser que`) é **PTC-3**. Rotule com a regra de lá e use a PTC-9 só para o que nenhuma outra cobre.

**O que a PTC-9 não pede.** Guias de "humanizar texto de IA" mandam variar o tamanho das frases, ter opinião e escrever em 1ª pessoa. Isso contradiz `estrito`, em que a forma uniforme e neutra é o objetivo. Em `leve`, a 1ª pessoa já é permitida pela tabela de níveis. A PTC-9 tira o ruído e não acrescenta voz.

Catálogo evite → use completo: **`references/ruido-ia.md`**.
