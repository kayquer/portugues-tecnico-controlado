<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md.

     Duas coisas neste caso são deliberadas e já custaram uma sessão:

     1. `nao-marca` não cita `chave de API do banco de dados` inteiro. A PTC-6
        expande `API` na 1ª ocorrência e o substring literal some sem que a PTC-5
        tenha disparado. `do banco de dados` prova a mesma coisa (a cadeia de `de`
        não foi quebrada) e sobrevive à expansão.

     2. `não a suíte inteira` não é enfeite. Sem esse contraste, `apenas` lê tanto
        como quantificador (um teste só) quanto como minimizador (`é só rodar um
        teste`) — e o léxico manda cortar minimizador. Um contra-teste ambíguo na
        própria dimensão que ele testa não prova nada. -->
# caso: contra-teste PTC-5 — anteposição intencional e cadeia lexicalizada
nivel: estrito
espera:
contra-teste: PTC-5
nao-marca: apenas um teste, do banco de dados

## entrada
Rode apenas um teste, não a suíte inteira. A chave de API do banco de dados fica no cofre.
