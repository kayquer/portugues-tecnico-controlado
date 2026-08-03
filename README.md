# Português Técnico Controlado (PTC)

Skill do [Claude Code](https://claude.com/claude-code) que reescreve texto técnico em português do Brasil para que ele tenha **uma leitura só**.

O leitor de um procedimento não pode perguntar "você quis dizer X ou Y?". Um modelo que consome uma instrução também não. O texto precisa responder antes.

Inspirado no [ASD-STE100](https://www.asd-ste100.org/) (Simplified Technical English), o padrão de linguagem controlada da indústria aeroespacial — mas **não é uma tradução dele**. Ver [Por que não é o STE traduzido](#por-que-não-é-o-ste-traduzido).

---

## O problema

O português esconde informação em lugares que o inglês obriga a declarar.

```
Envia o e-mail e atualiza o status.
```

Quem envia? A terceira pessoa do singular em português colapsa `ele`, `ela`, `você`, `o sistema` e `o usuário` numa forma só. O inglês resolve isso ao exigir o sujeito. O português, não.

```
O processo deve terminar em 5 minutos.
```

Isso é uma regra ou uma estimativa? `deve` carrega obrigação e probabilidade na mesma palavra.

```
Os servidores, que falharam, foram reiniciados.
```

Todos falharam. Sem as vírgulas, só os que falharam foram reiniciados. Uma vírgula muda o escopo, e o erro fica invisível.

Esta skill ataca esses casos com 8 regras.

---

## Instalação

```bash
git clone https://github.com/kayquer/portugues-tecnico-controlado ~/.claude/skills/portugues-tecnico-controlado
```

O Claude Code registra a skill na próxima sessão. A skill não tem dependências: nenhum pacote, nenhuma outra skill, nenhuma chamada de rede.

---

## Uso

Invoque pelo nome:

```
/portugues-tecnico-controlado
```

Ou descreva a tarefa em linguagem natural:

- "reescreve esse runbook em português controlado"
- "tira a ambiguidade desse texto"
- "quero esse procedimento em EN e PT"
- "revisa esse comunicado"

A skill classifica o nível de rigor e o destinatário sozinha quando você não especifica, e declara o que assumiu na primeira linha da resposta.

### Saída

A skill devolve uma tabela que nomeia a regra violada em cada trecho, o texto final, e uma nota sobre o que ela deixou como estava.

```markdown
**Nível:** estrito · **Destinatário:** humano

| Regra | Original | Reescrito |
|---|---|---|
| PTC-1 (`-se` apassivador) | "Faz-se a validação do token." | "O gateway valida o token." |
| PTC-4 (verbo-suporte) | "Realize a conferência dos logs." | "Confira os logs." |
| PTC-8 (hífen r/s) | "micro-serviços" | "microsserviços" |

**Texto final:**
> O gateway valida o token. Confira os logs dos microsserviços.

**Mantido de propósito:** "front-end" — convenção de estilo, não erro ortográfico.
```

---

## As 8 regras

As regras PTC-1 a PTC-5 tratam de **desambiguação** e exigem julgamento. As regras PTC-6 a PTC-8 tratam de **consistência**, funcionam de forma mecânica, e nunca relaxam.

| | Regra | Resumo |
|---|---|---|
| **PTC-1** | Quem faz, aparece | Sujeito explícito. Sem `-se` apassivador, sem `o mesmo`, sem clítico de 3ª pessoa. |
| **PTC-2** | Uma proposição por frase, uma forma verbal | Imperativo para instrução, presente 3ª pessoa para comportamento. Sem gerúndio conector. |
| **PTC-3** | Modalidade e quantidade explícitas | `deve` = obrigação. Probabilidade nunca por modal. Quantificador vago vira número. |
| **PTC-4** | Verbo pleno, não verbo-suporte | `realizar a validação` → `validar`. |
| **PTC-5** | Sintaxe plana | Adjetivo pós-nominal. Cadeia de `de` ≤ 2. Nada entre verbo e objeto. |
| **PTC-6** | Termos congelados, variante BR | Um conceito, um termo. Fixa o português brasileiro. |
| **PTC-7** | Formato de número, data e unidade | Vírgula decimal em PT. Datas em ISO 8601 nos dois idiomas. |
| **PTC-8** | Ortografia PT-BR vigente | Acordo de 1990, obrigatório no Brasil desde 2016-01-01. |

### Exemplos

```diff
- Envia o e-mail e atualiza o status.
+ O serviço envia o e-mail. O worker atualiza o status.        # PTC-1

- Execute o script, gerando o relatório.
+ Execute o script para gerar o relatório.                     # PTC-2

- O processo deve terminar em 5 minutos.
+ O processo termina em até 5 minutos.                         # PTC-3

- Realize a validação dos dados de entrada.
+ Valide os dados de entrada.                                  # PTC-4

- a validação do cadastro do cliente do contrato
+ Valide o cadastro. Esse cadastro pertence ao cliente.        # PTC-5

- Limite de 1.5 GB para 1,000 usuários.
+ Limite de 1,5 GB para 1.000 usuários.                        # PTC-7

- infra-estrutura dos micro-serviços
+ infraestrutura dos microsserviços                            # PTC-8
```

### A regra do hífen que mais paga

A regra PTC-8 cobre o Acordo Ortográfico de 1990 inteiro, mas um caso concentra quase todo o erro em texto de TI: **prefixo terminado em vogal + palavra começada por `r` ou `s` junta e dobra a consoante.**

| Errado | Correto |
|---|---|
| micro-serviço, microserviço | **microsserviço** |
| auto-serviço | **autosserviço** |
| anti-racismo | **antirracismo** |
| contra-regra | **contrarregra** |

O arquivo [`references/ortografia-ptbr.md`](references/ortografia-ptbr.md) traz a tabela completa de prefixos, a acentuação pós-Acordo, e as armadilhas de vocabulário técnico.

---

## Níveis de rigor

Linguagem controlada é deliberadamente plana. Aplicar rigor de procedimento a um comunicado interno produz texto robótico — esse é o erro clássico de quem adota o método. Por isso a skill trabalha em três níveis.

| Nível | Uso |
|---|---|
| `estrito` | procedimento, runbook, saída de agente |
| `descritivo` | documentação de sistema |
| `leve` | comunicado interno |

As regras PTC-1, PTC-7 e PTC-8 **nunca relaxam**. Em comunicado, `o mesmo foi cancelado` e `1,000 clientes` continuam causando dano, e ortografia errada não fica menos errada porque o texto é informal.

O resto sai em `leve`. O léxico controlado fica dispensado e a primeira pessoa passa a ser desejável.

Um comunicado processado em `leve` recebe duas correções:

```diff
  Pessoal, informamos que na próxima segunda-feira será realizada a migração do servidor.
- O mesmo ficará indisponível das 22h às 02h.
+ O servidor ficará indisponível das 22h às 02h.
- Estimamos que aproximadamente 1,000 usuários serão impactados.
+ Estimamos que aproximadamente 1.000 usuários serão impactados.
  Solicitamos que todos efetuem o logout antes do horário.
```

O tom permanece. `informamos`, `solicitamos` e `efetuem o logout` violariam PTC-4 e PTC-6 em nível `estrito`, e o nível `leve` os preserva de propósito.

### Flag `destinatário: agente`

A flag atua sobre `estrito` e muda três coisas:

1. Instrução ao agente usa imperativo; descrição de ferramenta usa presente na 3ª pessoa.
2. Nenhuma anáfora atravessa frase — o consumidor pode truncar o texto.
3. Status usa sujeito e verbo finito, nunca particípio isolado.

```diff
- Arquivo enviado.                          # evento concluído ou propriedade do estado?
+ O agente enviou o arquivo.                # evento
+ O arquivo está no estado ENVIADO.         # propriedade
```

---

## Modo bilíngue

Quando o documento precisa existir em português e inglês, a skill segue um pipeline serial.

**A fonte de verdade é o idioma do input**, não um pivô fixo em inglês:

| Input | Fonte | Derivado |
|---|---|---|
| Inglês | inglês controlado (regras STE) | português controlado |
| Português | português controlado | inglês controlado |

1. A skill reescreve **na língua fonte**, sob as regras dela.
2. A skill traduz **o texto já controlado** — nunca o original bruto.
3. A skill aplica as regras da língua alvo só onde elas não alterem a proposição.

O caminho `PT → EN → PT` nunca acontece: cada tradução reintroduz a ambiguidade que o controle acabou de remover. E o risco maior nem é esse — é a **normalização divergente**. Quando alguém normaliza os dois idiomas em paralelo a partir do original bruto, cada conjunto de regras puxa para um lado e as duas versões passam a afirmar coisas diferentes.

### O português funciona como linter do inglês

Este é o ponto que justifica o desenho inteiro.

Se no passo 3 uma regra do português exigir informação que o inglês não tinha, isso **não é problema de tradução**. É ambiguidade não resolvida na fonte.

```
EN fonte:  The report should be sent after validation.

           PTC-1 pergunta: quem envia?
           PTC-3 pergunta: "should" é obrigação ou expectativa?

EN corrigido:  The scheduler sends the report after the gateway validates the token.
PT derivado:   O agendador envia o relatório depois que o gateway valida o token.
```

A skill volta ao passo 1 e corrige o inglês. Esse é o único mecanismo que impede o tradutor de inventar o ator.

### Verificação de equivalência

A skill extrai uma tabela de proposições **de cada versão de forma independente** e compara célula a célula:

| # | ator | ação | objeto | condição | resultado/erro | valor+unidade | modalidade |
|---|---|---|---|---|---|---|---|

A verificação falha quando uma célula existe numa versão e não na outra, quando a contagem de passos imperativos difere, ou quando um termo do glossário aparece traduzido de dois jeitos.

Detalhes em [`references/ingles.md`](references/ingles.md).

---

## Escopo

### O que a skill faz

- Reescreve texto em português para leitura única, e nomeia a regra que cada trecho violava.
- Preserva todo fato, condição e qualificador de escopo do original.
- Gera o par EN/PT com verificação de equivalência proposicional.
- Ajusta o rigor ao leitor, em vez de aplicar tudo sempre.
- Aplica a ortografia do Acordo de 1990, com atenção ao vocabulário de TI.

### O que a skill não faz

- **Não reproduz o dicionário de ~900 palavras aprovadas da ASD.** Esse documento é o download oficial deles, gratuito em [asd-ste100.org](https://www.asd-ste100.org/). Esta skill aplica o princípio — a palavra mais simples disponível, sempre usada do mesmo jeito — em vez de checar contra lista fixa.
- **Não entrega documentação aeroespacial certificada em STE.** Para isso, o padrão oficial é a fonte de verdade.
- **Não marca variante de português europeu como erro.** `utilizador`, `ecrã` e `ficheiro` estão corretos em PT-PT. A skill *fixa* a variante brasileira por consistência de projeto.
- **Não trata convenção de estilo como norma.** `front-end`/`frontend` e `data center`/`datacenter` são empréstimos que o VOLP não hifeniza. A skill documenta a escolha em vez de apontar erro.
- **Não simplifica texto criativo ou persuasivo.** Copy de marketing perde o que importa sob linguagem controlada.
- **Não corta condição de segurança nem qualificador de escopo para encurtar frase.** A skill sinaliza o custo em vez disso.

---

## Por que não é o STE traduzido

Traduzir as 53 regras do ASD-STE100 uma a uma não funciona, por duas razões simétricas.

**Metade das regras fica vazia em português.** "Uma classe gramatical por palavra" existe porque em inglês `oil` funciona como substantivo e verbo sem mudar de forma. Em português a morfologia já separa `óleo` de `lubrificar`, e a regra não paga nada. O limite de cluster nominal também quase não se aplica: o português converte pilha de substantivos em sintagma preposicionado, e o problema migra para a cadeia de `de`.

**Os vícios reais do português ficam descobertos.** O inglês obriga o sujeito, então o STE nunca precisou de uma regra para isso — enquanto o sujeito nulo é a maior fonte de ambiguidade que o português tem. O mesmo vale para o `-se` apassivador, a posição do adjetivo, o gênero gramatical criando correferência falsa, e a relativa explicativa distinguida só por vírgula.

**Não existe norma equivalente.** Não há "Simplified Technical Portuguese" — nem da ASD, nem da ABNT, nem da ABRAT. Existe pesquisa acadêmica isolada ([Gomes 2011](https://repositorio.ulisboa.pt/entities/publication/96c94c8d-9505-497b-be92-bbaa18cd7a43), Universidade de Lisboa; UFSC 2014), sem adoção industrial. Esta skill não implementa uma norma. Ela aplica o *princípio* da linguagem controlada às características reais do português.

### Sobre a prática da indústria

Circula a ideia de que fabricantes escrevem em STE e traduzem depois. A evidência não sustenta isso.

A **Embraer escreve** a documentação dos E-Jets em Simplified English, e o mercado brasileiro consome os manuais em inglês. O inglês ali é imposição regulatória (ICAO/ATA iSpec 2200), não escolha de qualidade.

A alegação de que linguagem controlada melhora tradução também é empiricamente modesta. O'Brien (Dublin City University) mediu o efeito com eye-tracking e encontrou ganho real, porém marginal, concentrado em textos já complexos. Na tradução automática, as regras não reduziram erros de forma significativa — em francês, o texto controlado produziu 51 erros contra 45 do texto original.

---

## Estrutura

```
portugues-tecnico-controlado/
├── SKILL.md                        # 8 regras, 3 níveis, processo, formato de saída
├── references/
│   ├── lexico.md                   # evite→use, conectores ambíguos, variante BR, siglas
│   ├── ortografia-ptbr.md          # Acordo de 1990, armadilhas de TI, o que não é erro
│   └── ingles.md                   # regras STE-EN, pipeline bilíngue, decalques e falsos amigos
├── tests/                          # harness de regressão — ver Desenvolvimento
├── loops/                          # goal loops e estado entre sessões
├── init.sh                         # roda a verificação
└── AGENTS.md                       # como editar a skill sem quebrá-la
```

**A skill é `SKILL.md` + `references/`.** O resto do repositório é harness de desenvolvimento e não vai para o prompt.

Os arquivos de `references/` carregam sob demanda. O arquivo `ortografia-ptbr.md` entra quando surge dúvida de grafia; o arquivo `ingles.md` entra só quando o par EN/PT importa.

---

## Fontes

- [ASD-STE100 — site oficial](https://www.asd-ste100.org/) · [FAQ](https://asd-ste100.org/STE_faq.html)
- [ASD Europe — Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- O'Brien, [*Controlled Language and Readability*](https://doras.dcu.ie/17153/1/OBrien_CL_and_Readability.pdf) — Dublin City University
- Gomes 2011, [*Contributos para um português controlado*](https://repositorio.ulisboa.pt/entities/publication/96c94c8d-9505-497b-be92-bbaa18cd7a43) — Universidade de Lisboa
- [Decreto nº 6.583/2008](https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/decreto/d6583.htm) — Acordo Ortográfico no Brasil
- [VOLP — Academia Brasileira de Letras](https://www.academia.org.br/nossa-lingua/busca-no-vocabulario) — fonte autoritativa de grafia
- [Base XVI — hífen, texto normativo](https://www.flip.pt/Acordo-Ortografico/Texto/Base-XVI-Do-hifen-nas-formacoes/)

### Pontos tratados como convenção, não como norma

A pesquisa não confirmou três itens, e a skill declara isso em vez de citar norma inexistente: norma ABNT dedicada a itálico em estrangeirismo de documentação técnica; API pública do VOLP; menção literal de `além-`, `aquém-` e `recém-` na Base XVI.

---

## Desenvolvimento

> ⚠️ **Este repositório contém português errado de propósito.** Os casos em `tests/casos/` e os exemplos marcados `❌` são o material de trabalho da skill. Corrigi-los quebra a skill em silêncio. Leia [`AGENTS.md`](AGENTS.md) antes de editar qualquer coisa.

```bash
./init.sh                     # roda todos os casos de regressão
./init.sh caso-01             # um caso só
./init.sh --cobertura         # matriz de cobertura — não chama a API, é instantâneo
PTC_MODELO=opus ./init.sh     # outro modelo (default: sonnet)
PTC_TENTATIVAS=1 ./init.sh    # sem retry, para medir instabilidade
```

O runner concatena `SKILL.md` + `references/*.md` **deste repo** e manda para `claude -p`. Ele testa o arquivo que você acabou de editar, não a cópia instalada em `~/.claude/skills/`.

Como output de LLM não é determinístico, ele não compara texto. Verifica três coisas:

- **cobertura** — toda regra de `espera:` apareceu na tabela de violações
- **falso positivo** — todo termo de `nao-marca:` sobreviveu intacto no texto reescrito
- **âncora** — todo termo de `deve-conter:` apareceu na saída

O segundo é o que impede a skill de virar um corretor que "conserta" português correto. O terceiro cobre o que não tem número de regra próprio — a flag `destinatário: agente` e o pipeline bilíngue, que pela tabela de violações seriam indistinguíveis de um caso comum.

Cada regra precisa de **dois** casos: um que a faz disparar e um contra-teste que prova que ela não dispara onde não deve. `./init.sh --cobertura` monta essa matriz e sai 0 quando ela fecha.

Detalhes do fluxo, definition of done e clean-state checklist em [`AGENTS.md`](AGENTS.md).

Requisitos: [Claude Code](https://claude.com/claude-code) e Python 3. Sem dependências a instalar.

## Créditos

O conceito de aplicar o ASD-STE100 como skill de agente veio de [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) (MIT). Este projeto reescreve as regras do zero para o português e não compartilha código com ele.

O ASD-STE100 pertence à [ASD](https://www.asd-europe.org/) — AeroSpace and Defence Industries Association of Europe. Este projeto não tem vínculo com a ASD e não distribui o conteúdo do padrão.

## Licença

MIT — ver [LICENSE](LICENSE).
