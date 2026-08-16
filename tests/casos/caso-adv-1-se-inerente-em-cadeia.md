<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     O `caso-05` já é contra-teste da PTC-1, com UM `-se` inerente isolado
     (`o serviço se reinicia`). O gatilho superficial da regra é a partícula
     `se`, e um `se` sozinho numa frase é fácil de absolver. Aqui são três
     `-se` em cadeia, em frases seguidas: a densidade é o ataque.

     O teste mecânico do `SKILL.md:50` é *"se dá para reescrever com é/são +
     particípio sem mudar o sentido, é o `se` proibido"*. Os três reprovam o
     teste, cada um por um motivo diferente:

       se conecta ao broker   `é conectado` inverte quem age — outro fato
       se recusa a repetir    `é recusado a repetir` é agramatical
       se comporta como       `é comportado` não existe

     O goal file sugeria `o processo se encerra e se registra` para este
     terreno. Descartei: `se registra` reescreve como `é registrado` sem perder
     nada, então o teste mecânico o classifica como proibido **com razão**, e a
     asserção viraria moeda ao ar. Mesma disciplina que descartou
     `pré-requisito` na rodada 5 e `plano de reversão` na rodada 1 — adversarial
     precisa de item onde só uma forma está certa.

     As âncoras não levam o `e` da coordenação de propósito. A PTC-2 pode
     quebrar a coordenação em duas frases com razão (uma proposição por frase
     em `estrito`), e `e se recusa` morreria nessa reescrita legítima sem a
     PTC-1 ter dado falso positivo nenhum — a armadilha do `caso-08`. Sem o
     `e`, a âncora sobrevive à quebra e morre só se o `-se` sumir, que é o erro
     procurado. A coordenação de sujeito nulo já é âncora do `caso-05`.

     Sem limiar de legibilidade — contra-teste de `espera:` vazia tem saída ≈
     entrada, e o número asseraria a entrada. -->
# caso: adversarial PTC-1 — `-se` pronominal inerente em cadeia
nivel: estrito
espera:
contra-teste: PTC-1
nao-marca: se conecta ao broker, se recusa a repetir, se comporta como

## entrada
O cliente se conecta ao broker e se recusa a repetir a chamada. O supervisor se comporta como observador até o fim da carga.
