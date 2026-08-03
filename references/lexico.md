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

## Conectores ambíguos

O ASD-STE100 resolve ambiguidade lexical com um dicionário de ~900 palavras. Em português o veneno está concentrado nos conectores — esta tabela é o análogo funcional.

| Conector | Ambiguidade | Use |
|---|---|---|
| `uma vez que` | causal ou temporal | `porque` / `quando` |
| `como` *(início de frase)* | causal, comparativo, conforme | `porque` / `conforme` |
| `desde que` | temporal ou condicional | `se` / `a partir de` |
| `à medida que` | proporcional ou temporal | `quando` / `conforme` |
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
