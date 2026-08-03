# Goal: fechar a matriz de cobertura das 8 regras

Goal loop no formato do [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) (lecture-13, project-07). Rode com `/loop` sem intervalo — o modelo se auto-pauta.

## Objetivo

Cada uma das 8 regras PTC precisa de **dois** casos em `tests/casos/`:

1. **positivo** — um texto que faz a regra disparar (declarado em `espera:`)
2. **contra-teste** — um texto onde a regra **não** deve disparar, provando que ela não gera falso positivo (declarado em `contra-teste:` e com os termos em `nao-marca:`)

O contra-teste é o que importa. Um caso que só prova o acerto positivo deixa passar o modo de falha mais comum de linguagem controlada: **corrigir o que já estava certo**.

## Verificação

```bash
./init.sh --cobertura    # matriz regra × (positivo, contra-teste). Exit 0 = fechada.
./init.sh                # todos os casos continuam verdes. Exit 0 = ok.
```

**As duas precisam sair 0.** Fechar a matriz quebrando um caso existente não conta como progresso.

## Condição de parada

Pare quando **qualquer uma** ocorrer:

- `./init.sh --cobertura` sai 0 **e** `./init.sh` sai 0 — objetivo atingido
- 12 rodadas completadas
- 2 rodadas seguidas sem nenhum caso novo entrar verde — o loop travou, escale para humano
- Um caso antes verde ficou vermelho e 1 rodada não recuperou — pare e reporte, não insista

## Restrições

**Não altere** para fazer a matriz fechar:

- `SKILL.md` e `references/*.md` — o objetivo é cobrir a skill com testes, não mudar a skill. Se um contra-teste revelar falso positivo real, **pare e reporte**; corrigir a regra é outra sessão, com outro escopo.
- `tests/verify.py` — mexer no avaliador para o caso passar é fraudar a verificação.
- Casos existentes — só adicione. Alterar `espera:` de caso que já existe mascara regressão.

**Não invente** contra-teste artificial. O texto tem que ser português que alguém escreveria de verdade. Um contra-teste que ninguém escreveria não protege contra nada.

## Por rodada

1. Rode `./init.sh --cobertura` e escolha **uma** regra sem contra-teste.
2. Escreva um texto realista em que aquela regra **não** deve disparar. Pense em qual leitura correta a regra poderia atropelar:
   - **PTC-1** — sujeito nulo legítimo (coordenação com o mesmo sujeito; imperativo ao leitor); `-se` pronominal inerente (`o serviço se reinicia`), que **não** é apassivador
   - **PTC-2** — gerúndio em perífrase durativa correta (`está processando`); relativa restritiva sem vírgula
   - **PTC-3** — `deve` legítimo de obrigação; número já explícito que não precisa virar outro número
   - **PTC-5** — adjetivo anteposto **intencional** (`apenas um teste`); cadeia de `de` com termo lexicalizado (`chave de API do banco de dados` conta 2 nós, não 4)
   - **PTC-7** — número que já está no formato certo; identificador de código com ponto (`v1.5`, `python3.11`) que **não** é decimal
3. Crie o caso com `contra-teste:` declarando a regra e `nao-marca:` listando os termos que devem sobreviver.
4. Rode `./init.sh <novo-caso>`. Verde → siga. Vermelho → o caso está errado **ou** você achou falso positivo real; decida qual, e no segundo caso pare e reporte.
5. Rode `./init.sh` inteiro para confirmar que nada mais quebrou.
6. Anote a rodada em `loops/loop-state.md`.

## Escopo por rodada

**Uma regra por rodada.** Duas ao mesmo tempo impedem saber qual caso quebrou o quê — a mesma razão que o `AGENTS.md` dá para mudanças na skill.

## Custo

A suite completa são 12 chamadas ao Claude quando tudo passa de primeira, mais uma por retentativa (`PTC_TENTATIVAS`, default 3). Prefira `./init.sh <caso-novo>` durante a rodada e deixe a suite inteira para o fim de cada rodada. `--cobertura` é grátis.
