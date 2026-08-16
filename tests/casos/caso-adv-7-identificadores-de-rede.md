<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     O `caso-09` já é contra-teste da PTC-7 e cobre `v1.5`, `3.11` e `1,5 GB` —
     o ponto que separa versão de decimal. Sobrou o resto do terreno que o
     goal-falso-positivo lista e ninguém testou: porta, CIDR, semver de três
     campos ao lado de semver de dois, e hash curto.

     Todos são gatilho superficial idêntico ao da regra — dígito, ponto, dígito —
     e nenhum é número decimal. `1.10.2` é o caso mais perigoso: trocar o ponto
     por vírgula não só quebra o identificador como inverte a ordenação, porque
     `1.10.2` é maior que `1.2` em semver e menor em decimal. A frase compara as
     duas de propósito, para que o erro tenha consequência visível no texto.

     `10.0.0.0/24` e `:8080` sobrevivem ou não sobrevivem inteiros — são âncoras
     exatas, sem risco de morrerem por reescrita legítima de outra regra (a
     armadilha do `caso-08`). Mesmo motivo para o hash `a3f9c21`.

     Sem sigla escrita por extenso: `CIDR` viraria expansão da PTC-6 e mataria o
     substring sem a PTC-7 ter disparado.

     Sem limiar de legibilidade — contra-teste de `espera:` vazia tem saída
     ≈ entrada, e o número asseraria a entrada. Vale notar que este caso também é
     o pior possível para a métrica: `normaliza()` troca ponto entre dígitos por
     vírgula para não rachar frase, então mede `1,10,2`. Não afeta asserção
     nenhuma aqui, mas não ponha limiar neste caso depois. -->
# caso: adversarial PTC-7 — porta, CIDR, semver e hash não são decimais
nivel: estrito
espera:
contra-teste: PTC-7
nao-marca: :8080, 10.0.0.0/24, 1.10.2, a3f9c21

## entrada
O balanceador escuta na porta :8080. A rede interna usa o bloco 10.0.0.0/24. O agente compara a versão 1.10.2 com a versão 1.2 e escolhe a versão maior. O operador registra o commit a3f9c21 no relatório.
