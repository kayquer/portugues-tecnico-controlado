# Ruído de texto gerado (PTC-9)

Catálogo da PTC-9. O critério é o do `SKILL.md`: **se o trecho sai e nenhum fato, condição ou instrução se perde, ele é ruído.** As listas abaixo são onde esse ruído costuma aparecer em texto técnico escrito ou revisado por modelo. Elas não são lista de palavras proibidas.

Adaptado da skill [deai-text](https://github.com/kayquer/deai-text), que cataloga os padrões de escrita de IA em inglês e em todos os gêneros. Daqui ficou só o que serve a texto técnico em PT-BR e não contradiz as outras oito regras. Ver "O que não veio da deai-text" no fim.

## Sempre sai

Vale nos três níveis, inclusive em `leve`, e vale para a própria saída da skill.

| Evite | Use | Por quê |
|---|---|---|
| Claro! / Com certeza! / Perfeito! | corte | resposta a uma pergunta que o leitor do documento não fez |
| Ótima pergunta / Excelente observação | corte | elogio ao interlocutor; o documento não tem interlocutor |
| Espero ter ajudado / Espero que isso ajude | corte | fecho de conversa |
| Fique à vontade para / Qualquer dúvida, estou à disposição | corte, ou o canal real (`Dúvidas: #infra-plantao`) | oferta sem canal: ninguém consegue usá-la |
| Vamos lá / Vamos explorar / Vamos entender | corte e comece pelo assunto | abertura falsamente colaborativa que atrasa o assunto |
| Neste documento, vamos abordar… / A seguir, veremos… | corte, ou um sumário com os títulos reais | anuncia o texto em vez de ser o texto |
| Em resumo, vimos que… *(no fim de seção curta)* | corte | repete o que o leitor acabou de ler |
| Com base nas informações disponíveis / Até onde sei | corte, ou diga qual fonte falta | limite do modelo que vazou para o documento |
| O futuro é promissor / Só o tempo dirá / Uma coisa é certa | corte | conclusão que serve para qualquer texto |
| Vou analisar passo a passo / Pensando nisso de forma estruturada | corte e entregue a conclusão | andaime de raciocínio que vazou para a prosa |

## Enchimento

Sai em `estrito` e `descritivo`; recomendado em `leve`.

| Evite | Use | Por quê |
|---|---|---|
| além disso / ademais / outrossim *(abrindo frase que só acrescenta)* | corte, ou `e` | a frase seguinte já é a próxima ideia; o conector não diz relação nenhuma |
| nesse sentido / dessa forma / desse modo *(sem relação causal)* | corte, ou `por isso` se a causa é real | soa como conclusão lógica e não conclui nada |
| quando se trata de X | sobre X, ou comece por X | rodeio |
| no cenário atual / nos dias de hoje / em um mundo cada vez mais… | a data ou o fato concreto, ou corte | contexto sem conteúdo |
| em suma / em síntese / em conclusão | corte | a conclusão tem de ser visível sem rótulo |
| vale destacar / cabe ressaltar / é importante mencionar | corte | metatexto; a PTC-6 já corta `vale ressaltar` |
| notavelmente / curiosamente / surpreendentemente | corte | diz ao leitor o que sentir sobre o fato |
| sem dúvida / certamente / de fato / indiscutivelmente | corte | reforço que não acrescenta evidência; oposto simétrico do hedge da PTC-3 |
| estudos mostram / especialistas apontam / pesquisas indicam | a fonte (`o relatório X de 2025`), ou corte a atribuição | autoridade sem nome: ninguém consegue conferir. É a PTC-1 aplicada a quem afirma |
| é sabido que / é consenso que | corte, ou a fonte | idem |

## Evasão de cópula

Sai em `estrito` e `descritivo`.

| Evite | Use | Por quê |
|---|---|---|
| atua como / funciona como / se configura como | é | verbo pomposo no lugar de `ser` |
| conta com / dispõe de / possui | tem | idem; `possuir` já está no léxico |
| apresenta *(no sentido de ter)* | tem / mostra | `apresentar erro` é outra entrada, no léxico |
| representa *(no sentido de ser)* | é | — |
| se destaca por | é / tem, mais o fato | destaque não demonstrado |

## Inflação

Sai em `estrito` e `descritivo` quando não há critério verificável junto. Com o critério, o adjetivo costuma sobrar: corte e deixe o número.

| Evite | Use | Por quê |
|---|---|---|
| robusto *(elogio vago)* | o critério: `tolera a queda de 1 nó`, `aceita 10.000 req/s` | promete sem dizer o quê |
| abrangente / completo *(sem dizer o que cobre)* | o escopo: `cobre os 12 endpoints públicos` | idem |
| de ponta / de última geração / estado da arte | a versão ou a comparação | envelhece no dia seguinte |
| sem atrito / transparente *(seamless)* / fluido | o que o usuário não precisa fazer | decalque de marketing |
| alavancar / potencializar / impulsionar | usar / aumentar X em N | verbo de apresentação comercial |
| crucial / fundamental / essencial / primordial *(como ênfase)* | `obrigatório` (é requisito) ou corte | ênfase que não diz se é obrigação; a PTC-3 quer o modal unívoco |
| divisor de águas / revolucionário / transformador | o que mudou, com número | inflação de importância |
| ecossistema *(metáfora)* | o conjunto real: `os 4 serviços e a fila` | vago |
| não é só X, é Y *(contraste fabricado)* | afirme Y | ninguém disse que era só X |

## O que fica

O teste da PTC-9 é "o que se perde?", não "a palavra apareceu?". Ficam:

- **Termo técnico com sentido próprio:** `estimador robusto`, `teorema fundamental`, `estado fundamental`, `cobertura abrangente` quando o texto diz qual é a cobertura, `transparente` no sentido de proxy transparente.
- **Conector com relação lógica real:** em `O cache expira em 60 s. Dessa forma, uma alteração leva até 60 s para aparecer.`, o conector marca a consequência, e cortar apaga a causa. Pode virar `Por isso`, que é mais exato. Não pode sumir.
- **Atribuição com fonte:** `O relatório de incidentes de 2026-03 mostra 14 falhas.`
- **1ª pessoa e tom social em `leve`:** `Contamos com vocês` em comunicado é cortesia que a tabela de níveis permite. A PTC-9 não fecha o que `leve` abriu.

## O que não veio da deai-text

A deai-text manda também variar o tamanho das frases, ter opinião, tomar partido e escrever em 1ª pessoa, porque texto de IA é "relentlessly neutral". Para prosa de autor, isso está certo. Para texto controlado, não: em `estrito` a forma uniforme e neutra **é** o objetivo, e frase curta seguida de frase longa só por ritmo esconde qual delas é a instrução. A PTC-9 adota o que tira ruído e deixa de fora o que acrescenta voz.

Dois itens da deai-text já tinham regra aqui e continuam rotulados nela: o rodízio de sinônimos é PTC-6 e o gerúndio analítico em cadeia é PTC-2.
