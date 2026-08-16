<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     O `caso-07` já é contra-teste da PTC-3, mas em `descritivo` e sobre `deve`
     de obrigação e número já explícito. Não toca em `pode` nem em `talvez`.
     Este roda em `estrito` e vai atrás da tensão interna da própria regra.

     `SKILL.md:95` diz **"Zero hedge"**. `SKILL.md:93` **prescreve `talvez`**
     como a forma aprovada de dizer probabilidade, já que modal ali é proibido.
     Os dois vão concatenados no mesmo prompt. É a assinatura exata do achado do
     `apenas` (loop-state, 2026-08-03): a mesma palavra prescrita numa linha e
     condenada em outra, e o modelo decidindo diferente a cada rodada. Aquele foi
     resolvido dividindo a entrada em hedge × quantidade (`lexico.md:38-39`); o
     `talvez` **não tem divisão equivalente** — aparece uma vez, numa célula, e
     nada diz que ele não é hedge.

     Se a skill cortar `Talvez`, ela tem duas saídas e as duas são achado:
     trocar por modal (`o índice pode estar desatualizado`) viola a linha da
     própria tabela que proíbe modal para probabilidade; inventar número inventa
     fato. É por isso que a âncora é `talvez` sozinho — qualquer uma das duas
     mata o substring.

     `pode cancelar` cobre o outro lado não testado: `pode` de permissão é o
     único sentido que a tabela de modais autoriza, e é fácil confundir com o
     `pode` de capacidade que ela manda trocar por `consegue`.

     Tirei `a qualquer momento` da primeira frase de propósito. Ele *parece*
     quantificador vago (PTC-3 manda virar número), mas é escopo irrestrito, que
     número nenhum expressa — discutível demais. Asserção que decide vale mais
     que asserção que abrange, e é uma regra por rodada.

     Sem sigla (lição do `caso-08`) e sem limiar de legibilidade (contra-teste de
     `espera:` vazia tem saída ≈ entrada). -->
# caso: adversarial PTC-3 — `talvez` é a forma prescrita, não hedge
nivel: estrito
espera:
contra-teste: PTC-3
nao-marca: pode cancelar, talvez, deve reconstruir

## entrada
O operador pode cancelar a execução. O relatório leva até 30 segundos. Talvez o índice esteja desatualizado. O operador deve reconstruir o índice antes da próxima carga.
