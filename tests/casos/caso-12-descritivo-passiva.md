<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. As regras NÃO devem disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md.

     Este caso existe para a **tabela de níveis**, não para uma regra. O risco
     que o AGENTS.md nomeia é relaxar uma linha da tabela sem quebrar teste
     nenhum; antes deste caso, `descritivo` tinha um caso só (`caso-07`, sobre
     modal) e as linhas que divergem de `estrito` não eram testadas por nada.

     Duas frases ancoram linhas que só são legais em `descritivo`:

     1. `é gerado`  — voz passiva sem ator (linha "Voz passiva": proibida em estrito)
     2. `tempo de resposta do serviço de fila` — cadeia de `de` de 3 nós (≤2 em estrito)

     A terceira frase (`Verifica-se`) NÃO está em `nao-marca`, e isso é
     deliberado. Medida 6×, ela sobrevive 2/6: a skill ora mantém, ora converte
     para `A integridade dos arquivos é verificada`, ora inventa ator (`o sistema
     verifica`). Não é asserção frágil — é a skill se contradizendo:

       · tabela de níveis: `PTC-1 sem -se passivo` = "ok em descrição sem ator"
       · corpo da PTC-1: teste mecânico "se dá para reescrever com é/são +
         particípio sem mudar o sentido, é o `se` proibido" — que classifica
         justamente este `-se` como proibido

     Os dois trechos vão concatenados no mesmo prompt, então o modelo decide
     diferente a cada rodada. Mesma família do `apenas` em `loop-state.md`.
     Corrigir a regra é outra sessão; `contra-teste:` não declara PTC-1 porque
     este caso não consegue provar PTC-1 enquanto a contradição existir. -->
# caso: contra-teste de nível — o que `descritivo` libera e `estrito` proíbe
nivel: descritivo
espera:
contra-teste: PTC-5
nao-marca: é gerado, tempo de resposta do serviço de fila

## entrada
O relatório é gerado ao fim de cada ciclo. Verifica-se a integridade dos arquivos antes do envio. O tempo de resposta do serviço de fila permanece abaixo de 200 ms.
