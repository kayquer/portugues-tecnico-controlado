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
