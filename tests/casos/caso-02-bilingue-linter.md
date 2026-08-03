<!-- TEXTO ERRADO DE PROPÓSITO. É a entrada do teste de regressão.
     NÃO corrija o português deste arquivo — ver AGENTS.md.

     `espera: PTC-1, PTC-3` cobre o linter reverso: a entrada planta ator omitido
     (PTC-1 pergunta quem consome) e `should` (PTC-3 pergunta obrigação ou
     expectativa). É o mecanismo que `ingles.md:50` chama de justificativa do
     desenho inteiro.

     `deve-conter` cobre o resto do pipeline. Sem ele, o caso passava com a skill
     só reescrevendo o português: nada exigia que o par EN/PT existisse. A tabela
     de proposições (SKILL.md:237) é emitida apenas no modo bilíngue, então a
     presença dela prova que o pipeline rodou. Âncora curta de propósito — pega
     "Tabela de proposições" e "Proposições", e a busca é case-insensitive. -->
# caso: bilíngue com linter reverso
nivel: estrito
bilingue: sim
espera: PTC-1, PTC-3
deve-conter: proposiç
nao-marca:

## entrada
Traduza para português e devolva o par EN/PT.

Once the upstream job has completed, the output artifact should be consumed.
