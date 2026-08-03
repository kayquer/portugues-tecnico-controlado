<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md.

     Nível `estrito` de propósito. O outro contra-teste da PTC-4 (`caso-03`) roda
     em `leve`, onde a tabela de níveis marca a regra como **dispensada** — ele
     prova que a tabela funciona, não que a regra sabe onde parar.

     A entrada evita sigla: a PTC-6 expande sigla na 1ª ocorrência e mataria o
     substring de `nao-marca` sem que a PTC-4 tivesse disparado (lição do caso-08). -->
# caso: contra-teste PTC-4 — nominalização legítima permanece
nivel: estrito
espera:
contra-teste: PTC-4
nao-marca: validação de entrada, relatório de conformidade

## entrada
A validação de entrada rejeita CPFs inválidos. O agendador grava o relatório de conformidade no cofre.
