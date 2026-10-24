<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste adversarial. A regra NÃO deve
     disparar aqui. NÃO 'melhore' este texto — ver AGENTS.md.

     A PTC-9 lista `robusto`, `fundamental` e `transparente` como inflação.
     Aqui os três são termo técnico com sentido próprio, e trocá-los muda o
     fato: `estimador robusto` é uma classe de estimador, `teorema fundamental
     do cálculo` é o nome do teorema, `proxy transparente` é o proxy que o
     cliente não configura. A regra decide pelo teste "o que se perde?", não
     pela palavra — este caso prova isso.

     Cada âncora só tem uma forma certa (disciplina 1 do loop-state). Não há
     conector na entrada: `Dessa forma` causal admite `Por isso` como reescrita
     legítima, e uma âncora com duas respostas certas não decide nada.
     Sem sigla, para a expansão da PTC-6 não matar substring. -->
# caso: contra-teste adversarial — termo técnico que parece inflação
nivel: descritivo
espera:
contra-teste: PTC-9
nao-marca: estimador robusto, teorema fundamental, proxy transparente

## entrada
O módulo de estatística usa um estimador robusto da mediana. O estimador tolera até 20% de valores discrepantes. A prova de convergência depende do teorema fundamental do cálculo. O tráfego passa por um proxy transparente. O cliente não configura o proxy.
