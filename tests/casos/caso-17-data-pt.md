<!-- TEXTO ERRADO DE PROPÓSITO. É a entrada do teste de regressão.
     NÃO corrija o português deste arquivo — ver AGENTS.md.

     Armadilha A9 do loop-state (sessão 2026-10-24): a PTC-7 mandava converter
     data para ISO e não dizia como ler `02/08/2026`. Em texto PT a leitura é
     DD/MM, então a saída certa é `2026-08-02`, sem marcador. Quem converte
     para `2026-02-08` leu como americano; quem devolve só a pergunta
     "A confirmar" não aplicou a cláusula nova, que diz que texto PT decide.

     O dia é ≤ 12 de propósito: é o único caso em que as duas leituras são
     datas válidas e o erro não aparece sozinho. -->
# caso: data numérica em texto PT é DD/MM
nivel: estrito
espera: PTC-7
deve-conter: 2026-08-02
nao-marca:

## entrada
O certificado do gateway vence em 02/08/2026. Renove o certificado até 01/08/2026.
