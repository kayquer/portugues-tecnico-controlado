#!/usr/bin/env python3
"""Check do próprio runner. Não chama a API — roda em `./init.sh` antes dos casos.

Verifica as duas decisões do `verify.py` que os casos de teste **não** alcançam:

  veredito()   PASS/FLAKY/ESCALOU/FAIL — reproduzir um ESCALOU de verdade
               depende do modelo menor falhar, que é o que não se controla
  cobertura()  o filtro `PTC_ADVERSARIAL`, que decide o critério de parada
               de `loops/goal-falso-positivo.md`

Uso: python3 tests/test_runner.py
"""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify  # noqa: E402


def caso_falso(**extra):
    c = {"nome": "caso-x", "nivel": "estrito", "destinatario": "", "bilingue": False,
         "espera": ["1"], "nao_marca": [], "contra_teste": [], "deve_conter": [],
         "entrada": "texto"}
    c.update(extra)
    return c


VERDE = "**Texto final:**\nok\n\n| PTC-1 | a | b |"
VERMELHO = "**Texto final:**\nok\n\nsem tabela"


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
    verify.TENTATIVAS = 3
    dublar([VERMELHO, VERDE])
    estado, tentativa, *_ = verify.veredito("skill", caso_falso())
    assert estado == "FLAKY", estado
    assert tentativa == 2, tentativa


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
    estado, _, faltou, *_ = verify.veredito("skill", caso_falso())
    assert estado == "FAIL", estado
    assert faltou == ["1"], faltou


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
    adv = [c for c in casos if c.stem.startswith(verify.PREFIXO_ADV)]
    assert codigo_on == (0 if adv else 1), (codigo_on, len(adv))
    assert codigo_off == 0, "a matriz normal deveria estar fechada"


if __name__ == "__main__":
    testes = [v for k, v in sorted(globals().items()) if k.startswith("teste_")]
    for t in testes:
        t()
    print(f"{verify.CINZA}runner: {len(testes)} checks ok{verify.RESET}")
