<!-- TEXTO ERRADO DE PROPÓSITO. É a entrada do teste de regressão.
     NÃO corrija o português deste arquivo — ver AGENTS.md. -->
# caso: procedimento com vícios plantados
nivel: estrito
espera: PTC-1, PTC-2, PTC-3, PTC-4, PTC-5, PTC-6, PTC-7, PTC-8
nao-marca: front-end, usuário

## entrada
Procedimento de Restauração de Backup

Antes de iniciar, deve-se realizar a validação do ambiente. Faz-se o backup do banco de dados, sendo que o mesmo deve ser armazenado em disco com no mínimo 1.5 GB livres. Após a conclusão, o operador deve verificar a infra-estrutura dos micro-serviços, gerando um relatório de não-conformidade caso encontre divergências.

Utilize as API's de monitoramento para acompanhar. A freqüência de verificação deveria ser de 5 em 5 minutos. Trata-se de um simples teste que possui como objetivo garantir que o front-end esteja disponível para o usuário final.
