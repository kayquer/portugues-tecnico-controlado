<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     O `caso-08` já é contra-teste da PTC-5, mas do outro bullet dela: posição
     do adjetivo (`apenas um teste`). O bullet da **cadeia de `de` ≤ 2 nós**
     nunca teve contra-teste adversarial — o `do banco de dados` do `caso-08`
     entrou como âncora encurtada por acidente de expansão de sigla, não como
     ataque à contagem.

     O gatilho superficial é contar preposição. As duas frases têm TRÊS
     preposições encadeadas cada uma e mesmo assim estão dentro do limite,
     porque o próprio `SKILL.md:114` diz que termo lexicalizado conta como UM
     nó — e nomeia `banco de dados` e `fila de mensagens` entre eles:

       a fila de mensagens no banco de dados      [fila de mensagens] + [banco de dados] = 2
       a taxa de erro do ponto de montagem        [taxa de erro] + [ponto de montagem] = 2

     Quem contar `de` em vez de contar nó acha 3 e quebra a frase. É o falso
     positivo procurado, e ele custa: quebrar `fila de mensagens` em duas
     frases inventa uma entidade `fila` que não existe no sistema.

     As âncoras são a cadeia inteira, não o termo lexicalizado sozinho:
     `fila de mensagens` sobreviveria à quebra da cadeia — âncora inerte, mesmo
     erro do check morto da rodada 1. Só a cadeia inteira morre no erro certo.

     Sem sigla, lição do `caso-08`: `chave de API` é o exemplo canônico deste
     bullet e foi descartado de propósito, porque a PTC-6 expande a sigla na
     primeira ocorrência e mataria o substring sem a PTC-5 ter disparado.

     Sem limiar de legibilidade — contra-teste de `espera:` vazia tem saída ≈
     entrada, e o número asseraria a entrada. -->
# caso: adversarial PTC-5 — cadeia de `de` com termo lexicalizado
nivel: estrito
espera:
contra-teste: PTC-5
nao-marca: fila de mensagens no banco de dados, taxa de erro do ponto de montagem

## entrada
O worker grava a fila de mensagens no banco de dados. O operador confere a taxa de erro do ponto de montagem.
