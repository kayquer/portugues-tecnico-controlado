<!-- TEXTO ERRADO DE PROPÓSITO. É a entrada do teste de regressão.
     NÃO corrija o português deste arquivo — ver AGENTS.md.

     Único caso que exercita a flag `destinatario: agente` (SKILL.md, "Flag
     destinatário: agente"). Ela não é um quarto nível — só muda três coisas
     sobre `estrito`, e nenhuma delas tem número PTC próprio. Por isso a
     asserção precisa de `deve-conter`: pela regra citada, este caso seria
     indistinguível de um PTC-1 comum.

     `espera:` é vazio de propósito. A entrada viola PTC-1 (o `Ele`) e a skill
     conserta sempre, mas etiqueta a linha ora como `PTC-1`, ora como
     "Destinatário agente" — os comportamentos da flag não têm número próprio.
     Medido: 4/5 na citação, 5/5 na correção. Asserção sobre a etiqueta é moeda
     ao ar; PTC-1 já tem 3 casos positivos que a citam sem essa concorrência.

     `ao servidor` custou uma medição. A entrada era `Pacote enviado às 14h30`,
     e a âncora deu 3/5: com marca de tempo, a skill oscila entre `O agente
     envia` e `O agente enviou` — as duas certas, porque a entrada não diz se
     aquilo é log de evento passado ou comportamento recorrente. O complemento
     direcional força a leitura de ação em presente, que é a mesma das outras
     duas frases. Mesma lição do caso-08: âncora medida sobre entrada ambígua
     na própria dimensão testada não mede nada. -->
# caso: flag agente — anáfora entre frases e status em particípio isolado
nivel: estrito
destinatario: agente
espera:
deve-conter: O agente envia o pacote
flesch-min: 68

## entrada
O agente lê o manifesto. Ele valida a assinatura do pacote. Pacote enviado ao servidor.
