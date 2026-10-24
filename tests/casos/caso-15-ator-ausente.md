<!-- TEXTO ERRADO DE PROPÓSITO. É a entrada do teste de regressão.
     NÃO corrija o português deste arquivo — ver AGENTS.md.

     Cobre a armadilha A1/A2 do loop-state (sessão 2026-10-24): a PTC-1 obriga
     a nomear o ator e a PTC-3 obriga o número, e a entrada não dá nenhum dos
     dois. A saída certa é o marcador, nunca `o agendador apaga` nem `até 50
     arquivos`. O texto é descrição de comportamento, não procedimento — por
     isso o imperativo ao leitor não serve de saída, e o `estrito` proíbe a
     passiva sem ator.

     `deve-conter: a confirmar` pega o marcador no texto final e a seção
     "A confirmar", e a busca é case-insensitive. -->
# caso: ator e número ausentes viram marcador, não fato inventado
nivel: estrito
espera: PTC-1, PTC-3
deve-conter: a confirmar
nao-marca:

## entrada
Descrição do comportamento noturno do servidor de arquivos:

Os logs são rotacionados toda noite. Depois da rotação, alguns arquivos antigos são apagados.
