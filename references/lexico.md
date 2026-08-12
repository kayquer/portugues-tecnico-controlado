# Léxico controlado PT-BR

Aplicado em `estrito` e `descritivo`. **Dispensado em `leve`** — comunicado interno não precisa disso e fica pior com isso.

Não existe dicionário oficial de português controlado (ver `SKILL.md`, "Por que não é o STE traduzido"). Esta lista ataca os vícios reais do português corporativo brasileiro, não o vocabulário geral.

## Evite → use

| Evite | Use | Por quê |
|---|---|---|
| realizar / efetuar / proceder a | o verbo pleno (`validar`, `enviar`, `conferir`) | verbo-suporte; esconde a ação (PTC-4) |
| utilizar | usar | sílaba a mais, zero ganho |
| possuir | ter | `possuir` implica posse jurídica |
| disponibilizar | dar acesso a / publicar / entregar | três ações diferentes num verbo só |
| necessitar de / demandar | precisar de / exigir | — |
| solicitar | pedir | — |
| o mesmo / a mesma | repita o substantivo | correferência falsa (PTC-1) |
| no sentido de / a fim de que | para | — |
| através de *(meio)* | por / por meio de | `através` é atravessar |
| em função de / face a | por causa de / para | `em função de` também é matemático |
| no âmbito de | em | — |
| sendo que | ponto final | conector vazio |
| onde *(não-lugar)* | em que / reescreva | — |
| eventualmente | às vezes **ou** no futuro | escolha um; falso amigo de `eventually` |
| inclusive | e também **ou** até | dois sentidos em PT-BR |
| vir a ser / estar sendo | ser / está | perífrase oca |
| impactar | afetar / aumentar / reduzir | diga a direção |
| performance | desempenho | — |
| garantir *(que X funciona)* | verificar / confirmar | um agente não garante, verifica |
| validar | verificar **ou** aprovar | dois sentidos; congele um por projeto |
| atualizar | atualizar *(update)* / recarregar *(refresh)* | dois sentidos |
| acessar | abrir / ler / consultar | genérico demais |
| gerar | criar / calcular / exportar | genérico demais |
| apresentar erro | exibe erro / retorna erro / falha com | três coisas diferentes |
| tratar | capturar *(exceção)* / resolver *(problema)* | — |
| subir / derrubar / startar | iniciar / parar / implantar | gíria de plantão |
| vale ressaltar / é importante notar | corte | metatexto |
| basicamente / simplesmente / apenas *(hedge: `é apenas um bug menor`)* | corte | minimizador; muda o fato |
| apenas / somente *(quantidade: `apenas um teste`)* | mantenha | não é hedge: restringe a quantidade. Cortar muda o fato, e a PTC-5 prescreve `apenas` para o sentido anteposto |
| executar *(+ nominalização: `executar a validação`)* | o verbo pleno (`valide`) | verbo-suporte (PTC-4) |
| executar *(+ objeto concreto: `execute o script`)* | mantenha | ali `executar` **é** o verbo pleno. A PTC-4 só proíbe a construção com nominalização |

### Burocratês

Fórmula de ofício que sobreviveu no e-mail corporativo. Some sem levar informação junto.

| Evite | Use | Por quê |
|---|---|---|
| vimos por meio desta / venho por meio deste | corte | abertura vazia; a primeira frase já devia ser o assunto |
| segue anexo / segue em anexo | o relatório está anexado | `segue` esconde quem envia (PTC-1) e a concordância de `anexo` gera dúvida |
| conforme alinhado / conforme conversado | conforme a decisão de 2026-03-14 | referência sem rastro: ninguém consegue conferir |
| para conhecimento / para ciência | corte, ou diga a ação esperada | não diz se o leitor precisa fazer algo |
| no que tange a / no tocante a | sobre | — |
| a partir do momento em que | quando | — |
| tendo em vista que | porque | — |
| de forma a / de modo a | para | — |
| sem prejuízo de | e também **ou** sem cancelar | adição e ressalva na mesma expressão |
| dar início a | iniciar | verbo-suporte (PTC-4) |
| fazer uso de | usar | verbo-suporte (PTC-4) |
| ter conhecimento de | saber | verbo-suporte (PTC-4) |
| levar em consideração | considerar | verbo-suporte (PTC-4) |
| ter como objetivo | servir para | verbo-suporte (PTC-4) |
| entrar em contato com | contate / ligue para / escreva para | verbo-suporte, e o canal fica implícito |
| a princípio / em princípio | inicialmente **ou** em tese | dois sentidos opostos: provisório e teórico |
| aderente a | conforme a / compatível com | anglicismo de `compliant`; em PT `aderente` é o que gruda |

### Gíria de plantão

Vocabulário de conversa de time que não sobrevive a um runbook lido às 3h da manhã.

| Evite | Use | Por quê |
|---|---|---|
| rodar | executar *(script)* / funcionar *(serviço)* | dois sentidos |
| puxar | buscar / baixar / consultar | três operações diferentes |
| bater *(com)* | conferir com / coincidir com | — |
| quebrar | falhar / interromper / ficar inválido | três resultados diferentes |
| estourar | exceder o limite / lançar exceção | dois sentidos |
| cair | ficar indisponível / falhar / ser encerrado | três sentidos |
| logar | registrar em log **ou** entrar na conta | dois sentidos opostos na mesma palavra |
| setar | definir | anglicismo sem ganho |
| resetar | reiniciar / limpar / restaurar o padrão | três operações diferentes |
| deployar | implantar / publicar | anglicismo sem ganho |
| acionar | chamar / notificar / iniciar | três ações diferentes |
| escalar | aumentar a capacidade **ou** encaminhar ao nível superior | dois sentidos técnicos opostos |
| otimizar | reduzir / acelerar / diminuir o custo | diga a direção, como em `impactar` |
| checar | verificar / conferir | anglicismo; e não distingue os dois |

### Falsos amigos do inglês

Aparecem em texto traduzido e em documentação escrita por quem lê em inglês o dia inteiro.

| Evite | Use | Por quê |
|---|---|---|
| assumir *(supor)* | supor / presumir | em PT `assumir` é assumir responsabilidade |
| endereçar *(tratar)* | tratar / resolver | em PT `endereçar` é pôr endereço |
| suportar *(aceitar)* | aceitar / ser compatível com | em PT `suportar` é aguentar carga — e esse sentido é legítimo |
| sensível *(significativo)* | significativo / relevante | `dado sensível` é outro sentido e fica |
| requerimento | requisito | em PT `requerimento` é petição |
| compreensivo | completo / abrangente | em PT `compreensivo` é quem compreende os outros |
| efetivo | eficaz | em PT `efetivo` é permanente ou de fato |
| prover | fornecer / dar | decalque de `provide`; raro em PT-BR fora de tradução |
| reportar | relatar / informar / registrar | `reportar-se a` é subordinar-se: outro sentido |
| submeter | enviar | em PT `submeter` é sujeitar alguém a algo |
| abortar | interromper / cancelar | — |
| deletar | excluir / apagar | anglicismo sem ganho |
| atualmente *(tradução de `actually`)* | na verdade | `atualmente` em PT é "no momento": inverte o sentido |

## Conectores ambíguos

O ASD-STE100 resolve ambiguidade lexical com um dicionário de ~900 palavras. Em português o veneno está concentrado nos conectores — esta tabela é o análogo funcional.

| Conector | Ambiguidade | Use |
|---|---|---|
| `uma vez que` | causal ou temporal | `porque` / `quando` |
| `como` *(início de frase)* | causal, comparativo, conforme | `porque` / `conforme` |
| `desde que` | temporal ou condicional | `se` / `a partir de` |
| `à medida que` | proporcional ou temporal | `quando` / `conforme` |
| `na medida em que` | causal, e trocado com `à medida que` o tempo todo | `porque` |
| `enquanto` | temporal ou adversativo | `enquanto` *(só temporal)* / `mas` |
| `inclusive` | "até mesmo" ou "aliás" | `até` / `e também` |
| `sendo que` | nenhuma — é cola | ponto final |
| `e/ou` | proibido | escolha `e` ou `ou`; se inclusivo mesmo: `A, B, ou os dois` |

## Variante brasileira

O Acordo de 1990 unificou a **ortografia**, não o **léxico**. As formas da coluna direita **não são erros** — são português europeu. Fixamos a variante BR por consistência; nunca marque a outra como incorreta.

### Léxico

| PT-BR *(use)* | PT-PT |
|---|---|
| arquivo | ficheiro |
| usuário | utilizador |
| tela | ecrã |
| mouse | rato |
| equipe / time | equipa |
| celular | telemóvel |
| cadastro | registo |
| aplicativo | aplicação |
| gerenciar | gerir |
| planilha | folha de cálculo |

### Ortografia que difere entre as variantes

Divergências fonéticas que o Acordo preservou de propósito — refletem pronúncia real diferente, não erro.

| PT-BR *(use)* | PT-PT |
|---|---|
| contato | contacto |
| registro | registo |
| setor | sector |
| recepção | receção |
| fato | facto |
| acadêmico | académico |
| econômico | económico |
| gênero | género |

Regra prática: onde o Brasil pronuncia a consoante, o Brasil a escreve. E o timbre tônico brasileiro é fechado (circunflexo), o europeu é aberto (agudo).

## Siglas

- **Gênero e artigo fixos no glossário do projeto.** `a API`, `a URL`, `a VPN`, `o endpoint`, `o commit`. Consistência importa mais que estar "certo" — decida uma vez e congele.
- **Plural sem apóstrofo.** `APIs`, `CDs`, `PRs`. Nunca `API's` — em português o apóstrofo marca elisão (`pau-d'água`), não plural.
- **Expanda na primeira ocorrência** e só então use a sigla: "Interface de Programação de Aplicações (API)".
- Sigla que já entrou na língua como palavra comum não precisa de expansão (`CPF`, `PDF`, `URL`).

## Glossário do projeto

O ASD-STE100 permite que cada organização defina o próprio dicionário de termos técnicos além da base. Aqui é o mesmo mecanismo, e é o único jeito honesto de lidar com vocabulário de domínio.

Ao trabalhar num projeto com termos recorrentes, mantenha uma tabela no próprio repositório:

```markdown
| Termo PT | Termo EN | Gênero/artigo | Definição em 1 linha | Não usar |
|---|---|---|---|---|
| corretor | broker | o corretor | Pessoa que intermedeia a negociação | agente, vendedor |
| imóvel | property | o imóvel | Unidade cadastrada com endereço | propriedade, item |
```

A coluna **"Não usar"** é a que mais paga: é ela que impede o texto de rodar sinônimos para o mesmo conceito, que é exatamente o que a PTC-6 proíbe.
