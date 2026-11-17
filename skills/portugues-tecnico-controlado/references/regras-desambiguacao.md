# Regras PTC-1 a PTC-5 — desambiguação

Atacam onde o português deixa duas leituras. Exigem julgamento. Resumo e ordem de uso no `SKILL.md`.

## PTC-1 — Quem faz, aparece

A regra número um, porque em português a 3ª pessoa do singular colapsa `ele`/`ela`/`você`/`o sistema`/`o usuário` numa forma só. Tudo que o inglês desambigua ao obrigar o sujeito, o português perde.

- **Sujeito lexical em toda oração finita.** Única exceção: imperativo dirigido ao leitor.
- **Contra-regra obrigatória:** em coordenação com o mesmo sujeito, **não** repita — senão o texto vira gagueira. Se o sujeito muda, quebre em duas frases.
- **Sem `-se` apassivador ou indeterminador.** Teste mecânico, sem metalinguagem: *se dá para reescrever com "é/são + particípio" sem mudar o sentido, é o `se` proibido.* `Faz-se a validação` → `A validação é feita` ✅ logo é proibido. Já `o serviço se reinicia` (pronominal inerente) passa.
  **O teste só reprova em `estrito`.** Em `descritivo`, `-se` apassivador sem ator relevante fica — a mesma licença que a tabela de níveis dá à voz passiva. `Verifica-se a integridade dos arquivos` ✅ em descrição de sistema, ❌ em procedimento. Não invente ator (`o sistema verifica`) para fugir do `-se`: ator inventado é fato inventado.
- **Sem clítico de 3ª pessoa** (`o`, `a`, `os`, `as`, `lhe`), **sem mesóclise** (`far-se-á`), **sem `o mesmo`**, **sem demonstrativo apontando para fora da frase.** Repita o substantivo.
- **Ator que o original não diz não se inventa, em nenhum nível.** Nomear o ator só vale quando o texto ou o contexto dizem quem é. O contexto diz quando o trecho tem um só ator e a frase sem sujeito continua a sequência dele: em `O instalador baixa o pacote. Ele confere o hash. Pacote extraído em /opt.`, quem extrai é o instalador, e um marcador ali é falsa dúvida. A dúvida é real quando o trecho não nomeia ator nenhum ou quando dois atores servem. Se o contexto não diz: em procedimento, a ação vai para o leitor no imperativo (`Faz-se o backup` → `Faça o backup`). Fora de procedimento, o ator vira marcador, `[a confirmar: quem faz o backup?]`, e a pergunta entra na seção "A confirmar" da saída. Texto com lacuna visível é aceitável. Texto com um fato que ninguém afirmou não é.

> ❌ Envia o e-mail e atualiza o status. *(quem?)*
> ⚠️ O serviço envia o e-mail e o serviço atualiza o status. *(explicitação idiota)*
> ✅ O serviço envia o e-mail e atualiza o status. *(mesmo ator)*
> ✅ O serviço envia o e-mail. O worker atualiza o status. *(atores diferentes)*

> ❌ A configuração usa o certificado padrão. Ele expira em 90 dias. *("ele" = certificado ou a configuração?)*
> ✅ A configuração usa o certificado padrão. O certificado expira em 90 dias.

Argumento extra para banir o `-se`: ele colide com o `se` condicional na mesma frase.

> ❌ Se o arquivo existe, faz-se o backup.
> ✅ Se o arquivo existe, faça o backup. *(procedimento: quem faz é o leitor)*
> ✅ Se o arquivo existe, [a confirmar: quem faz o backup?] faz o backup. *(descrição: o original não diz o ator)*

Os ✅ com ator nomeado nesta seção (`O serviço`, `O worker`) supõem que o contexto diz quem age. Sem esse contexto, a forma certa é o marcador.

## PTC-2 — Uma proposição por frase, uma forma verbal

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

## PTC-3 — Modalidade e quantidade explícitas

`deve` em português é obrigação **e** probabilidade na mesma forma. Isso é indecidível e precisa ser resolvido na escrita.

| Modal | Sentido único permitido | Substitui |
|---|---|---|
| `deve` | obrigação | `deverá`, `há de`, `é necessário que` |
| `pode` | permissão | — |
| `consegue` | capacidade técnica | `pode` no sentido de capacidade |
| — | probabilidade: **proibido usar modal** — dê número ou escreva `talvez` | `deveria`, `poderia`, `deve ser que` |

- **Zero hedge, sem inflar a certeza.** `deveria funcionar` → `funciona` (há evidência no texto), `deve funcionar` (é requisito) ou `talvez funcione` (é incerto). Se o texto não decide qual, use o marcador. Tirar o hedge sem evidência transforma uma incerteza em fato inventado.
- **Quantificador vago vira o número que a fonte dá.** Se o texto diz o limite em outro ponto, `alguns registros` → `até 50 registros`. Se a fonte não dá número, não estime: escreva `[a confirmar: quantos registros?]`. A mesma regra vale para `pode demorar` → `leva até [a confirmar: quanto tempo?]`.
- **Negação antes do quantificador.** `Nem todos os arquivos foram enviados`, nunca `Todos os arquivos não foram enviados`.

> ❌ O processo deve terminar em 5 minutos. *(regra ou estimativa?)*
> ✅ O processo termina em até 5 minutos. *(estimativa)*
> ✅ Encerre o processo em até 5 minutos. *(obrigação)*

## PTC-4 — Verbo pleno, não verbo-suporte

O alvo é a construção com **verbo leve** — `fazer`/`realizar`/`efetuar`/`proceder a`/`executar`/`promover` + nominalização. Não é a nominalização em si.

> ❌ Realize a validação dos dados de entrada. → ✅ Valide os dados de entrada.

**Nominalização legítima permanece.** `A validação de entrada rejeita CPFs inválidos` está correto — ali o substantivo é o termo do domínio. Não mexa.

## PTC-5 — Sintaxe plana

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
