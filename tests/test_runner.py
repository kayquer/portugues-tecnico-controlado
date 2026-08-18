#!/usr/bin/env python3
"""Check do próprio runner. Não chama a API — roda em `./init.sh` antes dos casos.

Verifica as decisões do `verify.py` que os casos de teste **não** alcançam:

  veredito()   PASS/FLAKY/ESCALOU/FAIL — reproduzir um ESCALOU de verdade
               depende do modelo menor falhar, que é o que não se controla
  cobertura()  o filtro `PTC_ADVERSARIAL`, que decide o critério de parada
               de `loops/goal-falso-positivo.md`
  métrica      o gate de legibilidade: que ele reprova, que ele aprova, que
               não mede a saída inteira, e que **não escala** para o opus
  colisão      termo que o `lexico.md` proíbe e o `SKILL.md` prescreve como ✅
               — os dois vão concatenados no mesmo prompt

Uso: python3 tests/test_runner.py
"""
import io
import re
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import legibilidade  # noqa: E402
import verify  # noqa: E402

# `dublar()` troca `verify.rodar` por um fake e não desfaz. Guardado aqui, antes
# de qualquer teste rodar, para o check do `rodar` de verdade não pegar o dublê.
RODAR_REAL = verify.rodar


def caso_falso(**extra):
    c = {"nome": "caso-x", "nivel": "estrito", "destinatario": "", "bilingue": False,
         "espera": ["1"], "nao_marca": [], "contra_teste": [], "deve_conter": [],
         "flesch_min": None, "pal_frase_max": None, "entrada": "texto"}
    c.update(extra)
    return c


VERDE = "**Texto final:**\nok\n\n| PTC-1 | a | b |"
VERMELHO = "**Texto final:**\nok\n\nsem tabela"

# Uma frase longa, de palavras longas: flesch baixo, palavras/frase alto. Serve
# aos dois lados do gate — reprova limiar exigente, passa limiar frouxo.
DIFICIL = ("**Texto final:**\n> A implementação da infraestrutura de "
           "monitoramento dos microsserviços possibilita a identificação "
           "antecipada de indisponibilidades sistêmicas recorrentes.\n\n"
           "| PTC-1 | a | b |")


def dublar(respostas):
    """Substitui `rodar` por uma sequência fixa. Devolve os modelos chamados."""
    chamados = []
    fila = list(respostas)

    def fake(skill, caso, modelo=verify.MODELO):
        chamados.append(modelo)
        assert fila, f"chamada a mais ao modelo (já foram {chamados})"
        return fila.pop(0)

    verify.rodar = fake
    return chamados


def teste_pass():
    verify.TENTATIVAS = 3
    chamados = dublar([VERDE])
    estado, *_ = verify.veredito("skill", caso_falso())
    assert estado == "PASS", estado
    assert chamados == [verify.MODELO], chamados


def teste_flaky():
    """FLAKY carrega o motivo da falha que ele escondeu.

    Sem isso, soluço de API e asserção quebrada saem idênticos na tela e a única
    forma de separar é remedir o caso isolado 5× — que custou uma investigação
    inteira na rodada 4 do goal-falso-positivo.
    """
    verify.TENTATIVAS = 3
    dublar([VERMELHO, VERDE])
    estado, tentativa, falhas = verify.veredito("skill", caso_falso())
    assert estado == "FLAKY", estado
    assert tentativa == 2, tentativa
    assert ("faltou", "PTC-1") in falhas, falhas


def teste_flaky_por_timeout_nao_inventa_motivo():
    """O espelho: timeout e depois PASS sai com `falhas` vazia.

    Vazio é o que faz o runner imprimir "sem resposta do modelo". Preencher com
    a última avaliação faria infra voltar a se disfarçar de regressão da skill,
    que é exatamente o problema que o motivo impresso existe para desfazer.
    """
    verify.TENTATIVAS = 3
    dublar([None, VERDE])
    estado, _, falhas = verify.veredito("skill", caso_falso())
    assert estado == "FLAKY", estado
    assert falhas == [], falhas


def teste_rodar_diz_por_que_o_cli_falhou():
    """CLI que sai != 0 **sem stderr** imprimia uma linha cinza vazia.

    É o que acontece no limite de taxa, e a suite de 2026-08-16 saiu com 18
    delas: o runner sabia que a chamada tinha falhado e não dizia nada. Mesma
    família do FLAKY sem motivo, e igualmente barato de consertar.
    """
    class CliMudo:
        returncode, stdout, stderr = 7, "", ""

    original = verify.subprocess.run
    verify.subprocess.run = lambda *a, **k: CliMudo()
    try:
        buf = io.StringIO()
        with redirect_stderr(buf):
            assert RODAR_REAL("skill", caso_falso()) is None
    finally:
        verify.subprocess.run = original
    assert "7" in buf.getvalue(), buf.getvalue()


def teste_escalou():
    """O caminho que só existe aqui: falha nas 3 tentativas, passa no escalado."""
    verify.TENTATIVAS = 3
    verify.MODELO_ESCALA = "opus"
    chamados = dublar([VERMELHO, VERMELHO, VERMELHO, VERDE])
    estado, *_ = verify.veredito("skill", caso_falso())
    assert estado == "ESCALOU", estado
    assert chamados == [verify.MODELO] * 3 + ["opus"], chamados


def teste_escalou_e_falhou():
    verify.TENTATIVAS = 1
    verify.MODELO_ESCALA = "opus"
    dublar([VERMELHO, VERMELHO])
    estado, _, falhas = verify.veredito("skill", caso_falso())
    assert estado == "FAIL", estado
    assert ("faltou", "PTC-1") in falhas, falhas


def teste_timeout_nao_escala():
    """Sem resposta para avaliar, escalar gastaria o modelo caro em nada."""
    verify.TENTATIVAS = 2
    verify.MODELO_ESCALA = "opus"
    chamados = dublar([None, None])
    estado, *_ = verify.veredito("skill", caso_falso())
    assert estado == "FAIL", estado
    assert "opus" not in chamados, chamados


def teste_escala_desligada():
    verify.TENTATIVAS = 1
    verify.MODELO_ESCALA = ""
    chamados = dublar([VERMELHO])
    estado, *_ = verify.veredito("skill", caso_falso())
    assert estado == "FAIL", estado
    assert chamados == [verify.MODELO], chamados


def teste_metrica_nao_escala():
    """O check mais importante: o modo de falha é invisível.

    Falha só de métrica que escalasse gastaria opus em silêncio e etiquetaria um
    FAIL legítimo de legibilidade como colisão de rótulo — que é o significado
    documentado de ESCALOU. O sintoma na tela seria idêntico.
    """
    verify.TENTATIVAS = 2
    verify.MODELO_ESCALA = "opus"
    chamados = dublar([DIFICIL, DIFICIL])
    estado, _, falhas = verify.veredito("skill", caso_falso(flesch_min=90))
    assert estado == "FAIL", estado
    assert "opus" not in chamados, chamados
    assert all(r == "métrica" for r, _ in falhas), falhas


def teste_metrica_escala_com_rotulo():
    """O espelho: falha mista escala. O guard é sobre o rótulo, não sobre
    'este caso tem métrica'."""
    verify.TENTATIVAS = 1
    verify.MODELO_ESCALA = "opus"
    # `sem tabela` não cita PTC-1 → falha de rótulo E de métrica; o opus devolve
    # texto fácil com a tabela.
    ruim = VERMELHO.replace("ok", "A implementação da infraestrutura possibilita "
                                  "a identificação antecipada de indisponibilidades.")
    chamados = dublar([ruim, VERDE])
    estado, _, _ = verify.veredito("skill", caso_falso(flesch_min=90))
    assert estado == "ESCALOU", estado
    assert "opus" in chamados, chamados


def teste_normaliza_igual_nos_dois_lados():
    """A comparabilidade inteira mora aqui: entrada crua e texto final em
    blockquote têm de medir igual, senão o antes/depois compara coisas
    diferentes e o limiar calibrado não significa nada."""
    cru = "O agendador valida o token.\nEle envia o relatório ao servidor."
    saida = ("**Texto final:**\n> O agendador valida o token.\n"
             "> Ele envia o relatório ao servidor.\n")
    assert legibilidade.medir(cru) == legibilidade.medir(verify.texto_final(saida))


def teste_decimal_nao_racha_frase():
    """`count_sentences` racha em qualquer `.`, então `1.5 GB` seriam duas
    frases — e a PTC-7 troca `1.5` por `1,5`, o que mudaria a contagem entre
    entrada e texto final por um motivo que não é legibilidade."""
    ponto = legibilidade.medir("O disco tem 1.5 GB livres e o pacote é o 3.11.")
    virgula = legibilidade.medir("O disco tem 1,5 GB livres e o pacote é o 3,11.")
    assert ponto.frases == virgula.frases == 1, (ponto, virgula)


def teste_metrica_sem_texto_final():
    """Sem a seção final não há o que medir. Cair para a saída inteira mediria a
    tabela de violações — número que passa ou reprova por acidente."""
    sem_secao = "| PTC-1 | a | b |\n\nnão emiti texto final"
    ok, falhas = verify.avaliar(caso_falso(flesch_min=50), sem_secao)
    assert not ok
    assert falhas == [("métrica", "não achei o 'Texto final:' na saída — "
                                  "não dá para medir")], falhas


def teste_gate_metrica_reprova_e_aprova():
    """O par. Só o lado que reprova deixaria passar um gate travado em vermelho."""
    exigente, _ = verify.avaliar(caso_falso(flesch_min=90, pal_frase_max=5), DIFICIL)
    frouxo, falhas = verify.avaliar(caso_falso(flesch_min=-100, pal_frase_max=99), DIFICIL)
    assert not exigente
    assert frouxo, falhas


def teste_medida_curta():
    """Texto sem palavra devolve None — não ZeroDivisionError, não 0.0."""
    assert legibilidade.medir("") is None
    assert legibilidade.medir("\n\n| a | b |\n") is None


def teste_flesch_ordena():
    """Ordenação, não valor absoluto: pega fórmula invertida e sinal trocado sem
    pinar a silabação do Pyphen num número mágico."""
    facil = legibilidade.medir("O disco está cheio. Apague um arquivo. Tente de novo.")
    dificil = legibilidade.medir(
        "A implementação da infraestrutura de monitoramento dos microsserviços "
        "possibilita a identificação antecipada de indisponibilidades sistêmicas.")
    assert facil.flesch > dificil.flesch, (facil, dificil)
    assert facil.pal_frase < dificil.pal_frase, (facil, dificil)


def teste_filtro_adversarial():
    """A suite real: com o filtro ligado, contra-teste comum não conta."""
    casos = sorted((verify.AQUI / "casos").glob("*.md"))
    assert casos, "nenhum caso em tests/casos/"

    def rodar_matriz(adversarial):
        verify.ADVERSARIAL = adversarial
        buf = io.StringIO()
        with redirect_stdout(buf):
            saida = verify.cobertura(casos)
        return saida, buf.getvalue()

    codigo_off, texto_off = rodar_matriz(False)
    codigo_on, texto_on = rodar_matriz(True)

    assert "contra-teste:" in texto_off and "adversarial:" in texto_on
    # Se o filtro não filtrar, os dois saem idênticos e o gate não gateia nada.
    assert texto_off != texto_on, "PTC_ADVERSARIAL não mudou a matriz"
    # A matriz adversarial só fecha quando **todas** as 8 regras têm um
    # `caso-adv-*` declarando-as em `contra-teste` — não quando existe um caso
    # adversarial qualquer. A versão anterior assumia a segunda coisa e era
    # código morto enquanto `caso-adv-*` não existia; o primeiro caso escrito
    # (PTC-4, 2026-08-16) derrubou a suite inteira sem nenhuma regressão real.
    regras_adv = {r for c in casos if c.stem.startswith(verify.PREFIXO_ADV)
                  for r in verify.parse_caso(c)["contra_teste"]}
    fechada = len(regras_adv) == len(verify.REGRAS)
    assert codigo_on == (0 if fechada else 1), (codigo_on, sorted(regras_adv))
    assert codigo_off == 0, "a matriz normal deveria estar fechada"


# Colisões conhecidas entre o `lexico.md` e o `SKILL.md`, com o motivo de cada
# uma ainda estar aqui. Não é allowlist de conveniência: é a lista de dívidas
# triadas, e o check falha nos **dois** sentidos — colisão nova entra, colisão
# resolvida tem de sair. Allowlist que só cresce vira o check morto da rodada 1.
COLISOES = {
    "validar": "item 3 do loop-state, sem oscilação medida. `lexico.md:30` manda "
               "congelar um sentido (verificar OU aprovar); o SKILL.md prescreve "
               "`Valide` em três exemplos ✅",
    "gerar": "mesma dívida. `lexico.md:33` chama de genérico demais; `SKILL.md:76` "
             "prescreve `para gerar o relatório` ✅",
    "atualizar": "mesma dívida. `lexico.md:31` separa update/refresh; "
                 "`SKILL.md:56-57` prescreve `atualiza o status` ✅",
    "a mesma": "falso positivo de granularidade de linha: o ✅ da linha 51 marca "
               "`Verifica-se a integridade`, e `a mesma licença` é prosa vizinha",
    "realizar": "falso positivo de granularidade de linha: a linha 107 tem ❌ e ✅, "
                "e `Realize` está do lado ❌",
}


def termos_do_lexico():
    """Coluna "Evite" das tabelas evite→use do `lexico.md`.

    Termo com alguma linha cujo uso é `mantenha` fica **fora**: essa linha é a
    resolução da colisão, não uma exceção. Foi assim que `apenas` e `executar`
    foram consertados, e é o que faz este check se calar sozinho quando o
    sentido é dividido — em vez de exigir uma entrada em `COLISOES`.
    """
    evite = {}
    cabecalho = False
    for linha in (verify.REPO / "references/lexico.md").read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            cabecalho = False
            continue
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if celulas[0] == "Evite":
            cabecalho = True
            continue
        if not cabecalho or set("".join(celulas)) <= set("-: "):
            continue
        for termo in celulas[0].split("/"):
            # `apenas *(hedge: ...)*` → `apenas`: o parentético diz o sentido,
            # não faz parte do termo.
            termo = re.sub(r"\*?\(.*?\)\*?", "", termo).strip(" *`").lower()
            if termo:
                evite.setdefault(termo, []).append(celulas[1].lower())
    return {t for t, usos in evite.items() if not any("mantenha" in u for u in usos)}


def raiz_lexical(termo):
    """`validar` → `valid`, para casar `Valide`, `valida` e `validação`.

    ponytail: corte de infinitivo, não stemmer. O piso de 4 letras é o que
    impede `gerar` → `ger` de casar `gerúndio` e `gerenciar`; em troca `gera`
    (sem o `r`) escapa, e `gerar` só é pego pela linha 76. Medido: com o piso,
    5 termos; sem ele, ruído em cima de `ger`, `sub` e `ca`. Subir para um
    stemmer de verdade só se um termo real passar batido.
    """
    corte = re.fullmatch(r"(.+?)(ar|er|ir)", termo)
    return corte.group(1) if corte and len(corte.group(1)) >= 4 else termo


def teste_colisao_lexico_skill():
    """O procedimento que existia só em prosa desde 2026-08-12.

    `apenas` e `executar` ficaram meses com o `SKILL.md` prescrevendo ✅ o que o
    `lexico.md` mandava cortar. Os dois arquivos vão concatenados no mesmo
    prompt, então o modelo decidia diferente a cada rodada — e nenhum caso pega
    isso, porque a saída sai *certa* metade das vezes.

    Só linhas com ✅ são varridas: é o único marcador inequívoco de "forma
    prescrita" no arquivo. Varrer o arquivo inteiro acha 12 termos a mais, todos
    prosa ou lado ❌ do exemplo. A coluna "Reescrito" do formato de saída
    (linha 227) também prescreve e fica de fora — hoje todo termo de lá já é
    pego por um ✅.
    """
    linhas = [l for l in (verify.REPO / "SKILL.md").read_text(encoding="utf-8").splitlines()
              if "✅" in l]
    assert linhas, "nenhuma linha com ✅ no SKILL.md — o check varreria nada"

    achadas = {t for t in termos_do_lexico()
               if any(re.search(rf"\b{re.escape(raiz_lexical(t))}\w*", l, re.IGNORECASE)
                      for l in linhas)}
    assert achadas == set(COLISOES), (
        "colisão léxico ↔ SKILL.md mudou."
        f"\n       novas:   {sorted(achadas - set(COLISOES))}"
        f"\n       sumiram: {sorted(set(COLISOES) - achadas)}"
        "\n       Nova: o léxico proíbe um termo que o SKILL.md prescreve como ✅."
        "\n       Divida o sentido no léxico (linha com uso `mantenha`) ou triague"
        "\n       em COLISOES com o motivo. Sumiu: resolvida — apague a entrada.")


if __name__ == "__main__":
    testes = [v for k, v in sorted(globals().items()) if k.startswith("teste_")]
    for t in testes:
        t()
    print(f"{verify.CINZA}runner: {len(testes)} checks ok{verify.RESET}")
