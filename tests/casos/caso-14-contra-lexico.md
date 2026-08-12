<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md.

     Ampliar o léxico de 29 para 75 linhas cria falso positivo: é o item do
     definition of done que o AGENTS.md diz ser o que mais escapa. Cada termo
     abaixo está no sentido em que a tabela manda **manter**:

       suporta      aguentar carga — o sentido legítimo de `suportar` em PT;
                    a linha nova só proíbe `suportar` = aceitar/ser compatível
       Atualmente   "no momento" — o sentido correto em PT. A linha nova só
                    trata `atualmente` como tradução errada de `actually`
       Execute      verbo pleno com objeto concreto. A PTC-4 lista `executar`
                    entre os verbos leves e o próprio SKILL.md usa `Execute o
                    script` como resposta ✅ — contradição que já existia e que
                    a linha dividida no léxico resolve. Este é o teste dela
       sensíveis    `dado sensível` é outro sentido, fora da linha nova -->
# caso: contra-teste do léxico ampliado — sentidos legítimos
nivel: estrito
espera:
contra-teste: PTC-6
nao-marca: suporta 500 conexões, Atualmente, Execute o script, dados sensíveis

## entrada
O servidor suporta 500 conexões simultâneas. Atualmente o serviço opera em duas regiões. Execute o script de verificação. O relatório não expõe dados sensíveis.
