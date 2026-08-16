<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     O `caso-06` já é contra-teste da PTC-2, mas testa a leitura legítima óbvia:
     `está processando` (perífrase durativa) e `que falharam` — relativa de duas
     palavras, curta demais para tentar ninguém a cortar. Este parte de um texto
     de estado plausível e ataca o que sobra: uma restritiva **longa**, de dez
     palavras, sem vírgula.

     É o terreno perigoso da regra porque PTC-2 proíbe relativa explicativa (a
     com vírgula) em estrito, e o tamanho é o que convida ao erro — quanto mais
     longa a restritiva, mais ela *parece* aposto e mais tenta uma vírgula. A
     vírgula ali não é estilo: `arquivos que o operador enviou` são alguns
     arquivos, `arquivos, que o operador enviou,` são todos. Muda o escopo.

     Por isso `nao-marca` é `arquivos que o operador` e não `que o operador
     enviou`: a segunda sobreviveria à inserção da vírgula, que é justamente o
     falso positivo procurado. A âncora tem de morrer quando o erro acontece.

     Cada frase tem uma proposição e no máximo uma subordinada — de propósito.
     Uma entrada com `enquanto` daria duas proposições numa frase, e aí dividir
     seria comportamento **correto** da PTC-2: a asserção viraria moeda ao ar em
     vez de decidir alguma coisa.

     Sem sigla (lição do `caso-08`) e sem limiar de legibilidade (contra-teste de
     `espera:` vazia tem saída ≈ entrada; o número asseraria a entrada). -->
# caso: adversarial PTC-2 — relativa restritiva longa não leva vírgula
nivel: estrito
espera:
contra-teste: PTC-2
nao-marca: arquivos que o operador, está reprocessando

## entrada
O agendador está processando a fila de entrada. Os arquivos que o operador enviou durante a janela de manutenção anterior permanecem no diretório temporário. O serviço está reprocessando os lotes rejeitados.
