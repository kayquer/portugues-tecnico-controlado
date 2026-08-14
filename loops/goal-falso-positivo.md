# Goal: caçar falso positivo com contra-teste adversarial

Goal loop no formato do [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) (lecture-13, project-07). Rode com `/loop` sem intervalo — o modelo se auto-pauta.

Sucessor do `goal-cobertura.md`, que fechou a matriz 8/8 e 8/8.

## Objetivo

Cada uma das 8 regras precisa de um caso `caso-adv-<regra>-<slug>.md` cuja entrada seja **português técnico correto** que dispara os gatilhos superficiais da regra sem cometer a violação.

Os contra-testes que já existem foram escritos junto com a regra, pelo mesmo raciocínio que a regra usa: cada um testa a leitura legítima **óbvia** (`o serviço se reinicia` não é `-se` apassivador; `v1.5` não é decimal). Isso prova que a regra não é grosseiramente errada. Não prova que ela não atropela português correto que **se parece** com a violação — que é o modo de falha que o `AGENTS.md` nomeia como o que mais escapa.

A diferença é de origem: o contra-teste normal parte da regra e pergunta "onde ela não deve valer". O adversarial parte de um texto bom e pergunta "o que aqui a regra pode confundir com erro".

## Verificação

```bash
PTC_ADVERSARIAL=1 ./init.sh --cobertura   # 8/8 na coluna adversarial. Exit 0 = fechada.
./init.sh                                  # suite continua verde. Exit 0 = ok.
```

**As duas precisam sair 0.** A primeira é grátis.

## Condição de parada

Pare quando **qualquer uma** ocorrer:

- as duas verificações saem 0 — objetivo atingido
- 10 rodadas completadas
- 2 rodadas seguidas sem caso novo verde **e** sem achado registrado — o loop travou, escale para humano
- Um caso antes verde ficou vermelho e 1 rodada não recuperou — pare e reporte

## Restrições

**Não altere:**

- `SKILL.md` e `references/*.md` — achar falso positivo é o **produto** deste loop; consertá-lo é outra sessão, com outro escopo. Um loop que caça e conserta na mesma rodada não sabe dizer se o conserto criou o próximo achado.
- `tests/verify.py` — mexer no avaliador para o caso passar é fraudar a verificação.
- Casos existentes — só adicione.

**Não invente** contra-teste artificial. Se ninguém escreveria aquele texto, ele não protege contra nada. Adversarial é texto **plausível** que confunde, não texto torturado.

## Por rodada

1. `PTC_ADVERSARIAL=1 ./init.sh --cobertura` e escolha **uma** regra em `✗`.

2. Escreva a entrada. Terrenos por regra, do mais provável ao menos:

   | Regra | O que pode ser confundido com a violação |
   |---|---|
   | **léxico** (cai em PTC-4/5) | `escalar` como crescer carga, `checar` onde `verificar` mudaria o registro, `atualmente` opondo-se a um estado anterior de fato, `sensível` como perceptível. O léxico saiu de 29 para 75 linhas e só o `caso-14` o cobre — com 4 termos. |
   | **PTC-2** | perífrase durativa correta em cadeia (`está processando enquanto grava`); relativa restritiva longa sem vírgula |
   | **PTC-3** | `deve` de obrigação normativa em texto descritivo; número já explícito que a regra tentaria trocar por outro número |
   | **PTC-7** | `python3.11`, `v1.5`, CIDR `/24`, semver `1.10.2` ao lado de `1.2`, porta `:8080`, hash curto |
   | **PTC-8** | `front-end`, `back-end`, `e-mail`; e o par perigoso da cláusula de fronteira: plural de sigla, que é PTC-6 e não PTC-8 |
   | **PTC-1** | `-se` inerente em cadeia (`o processo se encerra e se registra`) |
   | **PTC-6** | sigla consagrada que não pede expansão (`CPU`, `URL`, `HTTP`) |

3. `./init.sh caso-adv-...`
   - **Verde** → siga para 5.
   - **FAIL, FLAKY ou ESCALOU** → não conclua nada ainda. Vá para 4.

4. Diagnóstico antes de veredito. A tabela do `AGENTS.md` decide, nesta ordem:

   - **`ESCALOU`** (falhou no modelo default, passou no escalado) → **não é falso positivo**. É colisão de rótulo: modelo menor aplicou e não citou. Registre e siga.
   - **`corrigiu indevidamente: <termo>`** → **primeiro olhe a saída bruta.** Pode ser asserção frágil: o termo morreu por reescrita legítima de *outra* regra. Precedente: `chave de API do banco de dados` sumiu porque a PTC-6 expande `API`, sem a PTC-5 ter dado falso positivo nenhum. Encurte para o núcleo mínimo que ainda prova a regra e refaça.
   - **sobreviveu ao encurtamento** → meça: 5× com `PTC_TENTATIVAS=1`. **Falso positivo real** se falhar ≥2/5. Uma falha isolada não é achado — foi o que absolveu o `caso-02` duas vezes.
   - **achado confirmado** → registre em `loop-state.md` com a entrada, o trecho da saída bruta e a contagem. O caso **não entra** em `tests/casos/`: deixaria a suite vermelha, e a suite vermelha não é o produto. Fica no `loop-state` até a sessão de conserto. Precedente: `caso-12`, achado em 08-03 e consertado na sessão seguinte.
   - A regra conta como coberta pelo achado. Siga.

5. `./init.sh` inteiro. Anote a rodada em `loops/loop-state.md`.

## Escopo por rodada

**Uma regra por rodada** — mesma razão do `goal-cobertura.md` e do `AGENTS.md`: duas ao mesmo tempo impedem saber qual entrada provocou o quê.

## Custo

Um caso adversarial custa 1-3 chamadas; a medição de 5× só entra quando o caso sai vermelho ou instável. A suite completa ao fim da rodada são 14+. Ordem de grandeza: ~20 chamadas por rodada.

`--cobertura` e `tests/test_runner.py` são grátis. Prefira `./init.sh <caso-novo>` durante a rodada.
