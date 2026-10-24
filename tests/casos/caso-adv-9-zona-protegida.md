<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. Nenhuma regra deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     Armadilha A4 do loop-state (sessão 2026-10-24): até a v1.1, a regra "não
     reescreva identificador, código nem rótulo de interface" morava só em
     `ingles.md`, e o modo monolíngue não a via. Três iscas, cada uma com o
     gatilho exato de uma regra:

     - `Realizar pagamento` é o rótulo real do botão. A PTC-4 e o léxico mandam
       trocar `realizar` + nominalização, e trocar aqui quebra o procedimento:
       o leitor procura um botão que não existe.
     - `version: 1.5` está dentro de um bloco YAML. A PTC-7 troca decimal de
       ponto por vírgula, e a vírgula invalida o arquivo.
     - `logar()` é nome de função. O léxico manda trocar `logar`.

     As âncoras levam o contexto (`version: 1.5`, com dois-pontos) para não
     sobreviverem por acaso em outro lugar do texto. -->
# caso: contra-teste adversarial — rótulo de interface e código ficam intocados
nivel: estrito
espera:
contra-teste: PTC-4, PTC-6, PTC-7
nao-marca: Realizar pagamento, version: 1.5, logar()

## entrada
1. Abra a tela Pedidos.
2. Clique em Realizar pagamento.
3. Confirme que o arquivo `config.yaml` contém esta linha:

```yaml
version: 1.5
```

4. Se o pagamento falhar, a função `logar()` grava o erro em `/var/log/pagamentos.log`.
