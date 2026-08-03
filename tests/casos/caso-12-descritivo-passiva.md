<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. As regras NÃO devem disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md.

     Este caso existe para a **tabela de níveis**, não para uma regra. O risco
     que o AGENTS.md nomeia é relaxar uma linha da tabela sem quebrar teste
     nenhum; antes deste caso, `descritivo` tinha um caso só (`caso-07`, sobre
     modal) e as linhas que divergem de `estrito` não eram testadas por nada.

     Duas frases ancoram linhas que só são legais em `descritivo`:

     1. `é gerado`  — voz passiva sem ator (linha "Voz passiva": proibida em estrito)
     2. `tempo de resposta do serviço de fila` — cadeia de `de` de 3 nós (≤2 em estrito)

     A terceira frase (`Verifica-se`) sobrevivia 2/6 quando a skill se
     contradizia: a tabela de níveis liberava `-se` passivo em `descritivo`, e o
     teste mecânico do corpo da PTC-1 (`é/são + particípio`) classificava
     justamente este `-se` como proibido. Os dois iam concatenados no mesmo
     prompt e o modelo decidia diferente a cada rodada — mesma família do
     `apenas` em `loop-state.md`.

     Resolvido a favor da tabela: o teste mecânico ganhou cláusula de nível.
     Só por isso `Verifica-se` entrou em `nao-marca` e o caso passou a declarar
     `contra-teste: PTC-1`. -->
# caso: contra-teste de nível — o que `descritivo` libera e `estrito` proíbe
nivel: descritivo
espera:
contra-teste: PTC-1, PTC-5
nao-marca: é gerado, tempo de resposta do serviço de fila, Verifica-se

## entrada
O relatório é gerado ao fim de cada ciclo. Verifica-se a integridade dos arquivos antes do envio. O tempo de resposta do serviço de fila permanece abaixo de 200 ms.
