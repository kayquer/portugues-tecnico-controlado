<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     A PTC-6 tem três contra-testes positivos (`caso-01`, `caso-13`) e nenhum
     adversarial. O gatilho superficial atacado aqui é **"expanda na primeira
     ocorrência"** (`SKILL.md:130`), que está escrito sem exceção nenhuma —
     enquanto `lexico.md:165` dispensa a expansão de sigla que já entrou na
     língua como palavra comum (`CPF`, `PDF`, `URL`). Os dois vão concatenados
     no mesmo prompt.

     Isso não é hipótese: o `caso-08` perdeu a âncora `chave de API do banco de
     dados` porque a skill expandiu para `chave da Interface de Programação de
     Aplicações (API) do banco de dados`. Na época o diagnóstico parou em
     "asserção frágil" e a âncora foi encurtada. O mecanismo nunca foi testado
     como possível falso positivo da própria PTC-6.

     `URL` é a âncora decisiva porque está **nomeada** na lista de dispensa do
     léxico — ali só uma forma está certa. `CPU` e `HTTP` são da mesma classe e
     aparecem em runbook real, mas não estão na lista: entram como confirmação,
     não como o item que decide.

     As âncoras incluem o artigo e a preposição (`a URL do painel`, `uso de
     CPU`) de propósito: a expansão insere o nome por extenso ANTES do
     parêntese, então o substring morre exatamente no erro que ele existe para
     pegar. `URL` sozinho sobreviveria dentro de `(URL)` — âncora inerte.

     Segundo gatilho da mesma regra, de brinde: `instância`, `painel` e `time`
     repetem sem sinônimo, então o "um conceito, um termo" não tem o que
     congelar. `time` é variante BR (`equipe`/`time`), não anglicismo.

     Sem limiar de legibilidade — contra-teste de `espera:` vazia tem saída ≈
     entrada, e o número asseraria a entrada. -->
# caso: adversarial PTC-6 — sigla consagrada não pede expansão
nivel: estrito
espera:
contra-teste: PTC-6
nao-marca: a URL do painel, uso de CPU, resposta HTTP, URLs das instâncias

## entrada
O operador abre a URL do painel. O painel exibe o uso de CPU por instância. O time confere o código de resposta HTTP na coluna final. As URLs das instâncias ativas ficam na aba lateral.
