<!-- TEXTO ERRADO DE PROPÓSITO. É a entrada do teste de regressão.
     NÃO corrija o português deste arquivo — ver AGENTS.md.

     Cobre as três tabelas que a `Evite → use` ganhou além da lista original:
     burocratês, gíria de plantão e falsos amigos do inglês. Sem este caso, as
     45 linhas novas não têm asserção nenhuma por trás.

     A âncora é `requisito` porque `requerimento` é o único termo novo com um
     alvo único — `escalar`, `checar` e `logar` têm dois alvos legítimos cada,
     e âncora sobre escolha livre vira FLAKY permanente (AGENTS.md, "Quando
     usar deve-conter"). `requisito` também sobrevive ao plural. -->
# caso: léxico ampliado — burocratês, gíria e falso amigo
nivel: estrito
espera: PTC-6
deve-conter: requisito

## entrada
O time vai puxar os dados do painel e endereçar as divergências. O requerimento de latência não foi atendido, então resete o cache e escale para o plantão. Antes disso, logue no painel e cheque os últimos registros.
