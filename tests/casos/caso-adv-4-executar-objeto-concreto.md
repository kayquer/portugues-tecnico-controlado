<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     Adversarial, não contra-teste comum: o `caso-10` parte da regra e mostra
     nominalização legítima como **sujeito** (`A validação de entrada rejeita
     CPFs inválidos`). Este parte de um runbook plausível e pergunta o que a
     PTC-4 pode confundir com erro — `executar` + substantivo, que é o gatilho
     superficial literal da regra ("verbo leve + nominalização").

     A fronteira está escrita em `lexico.md:40-41`: `executar a validação` é
     verbo-suporte, `execute o script` é o verbo pleno. Essa distinção veio de
     um conserto de contradição e **não tem asserção nenhuma atrás dela** — é
     prosa em duas linhas de tabela. Se a PTC-4 voltar a atropelar o segundo
     caso, nada no harness percebe.

     Os três objetos são concretos de propósito — `script`, `testes`, `script`.
     Evitei `plano de reversão`: ali `reversão` **é** nominalização, e a linha
     ficaria discutível em vez de decisiva. Adversarial precisa ser texto que
     alguém escreveria, não texto torturado.

     Sem sigla, pela lição do `caso-08`: a PTC-6 expande sigla na 1ª ocorrência
     e mataria o substring de `nao-marca` sem a PTC-4 ter disparado.

     Sem limiar de legibilidade: contra-teste de `espera:` vazia tem saída
     ≈ entrada, então o número asseraria a entrada. Ver AGENTS.md, "O limiar se
     mede, não se chuta". -->
# caso: adversarial PTC-4 — `executar` com objeto concreto é verbo pleno
nivel: estrito
espera:
contra-teste: PTC-4
nao-marca: execute o script, execute os testes

## entrada
Execute o script de migração antes da janela de manutenção. Execute os testes de integração no ambiente de homologação. Se os testes falharem, execute o script de reversão e avise o time de plantão.
