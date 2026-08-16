<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     O `caso-04` já é contra-teste da PTC-8, mas com convenção de estilo —
     `front-end`, `data center`, `e-mail`. São palavras que a regra deixa em paz
     por decisão declarada ("O que NÃO é erro"), não por mecânica de hífen.

     Este ataca a mecânica. A PTC-8 dobra `r`/`s` e come o hífen depois de
     prefixo terminado em vogal (`micro` + `serviços` → `microsserviços`). O
     gatilho superficial é "prefixo + palavra começando em r/s", e três formas
     corretas caem nesse gatilho por motivos opostos:

       sub-rede            prefixo termina em CONSOANTE → hífen fica
       microsserviços      prefixo termina em vogal → dobra o s, sem hífen
       pós-processamento   prefixo tônico e acentuado → hífen sempre

     `sub-rede` é o item perigoso, e é termo de rede que aparece em runbook real:
     aplicar a dobra ali produziria `subrrede`, que não existe. As três na mesma
     entrada obrigam a regra a decidir três vezes em direções diferentes.

     `infraestrutura` entra como o quarto: hífen removido pelo Acordo de 1990, e
     é a forma que o `caso-01` planta ERRADA (`infra-estrutura`) do lado positivo.
     Aqui ela está certa e não pode ser mexida — o par cobre os dois sentidos.

     Descartei `pré-requisito` de propósito: `prerrequisito` também é forma
     atestada, então a asserção seria moeda ao ar em vez de decidir. Adversarial
     precisa de item onde só uma grafia está certa.

     Sem sigla (lição do `caso-08`). Sem limiar de legibilidade (contra-teste de
     `espera:` vazia tem saída ≈ entrada). -->
# caso: adversarial PTC-8 — hífen que fica, dobra que não se aplica
nivel: estrito
espera:
contra-teste: PTC-8
nao-marca: sub-rede, microsserviços, pós-processamento, infraestrutura

## entrada
O operador configura a sub-rede de gerência. A infraestrutura dos microsserviços já está ativa. O pós-processamento começa depois da carga.
