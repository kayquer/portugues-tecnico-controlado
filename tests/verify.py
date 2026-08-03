#!/usr/bin/env python3
"""Runner de regressão da skill PTC.

Roda cada caso de `casos/` contra o SKILL.md **deste repo** (não a cópia
instalada em ~/.claude/skills/) e confere quais regras PTC dispararam.

Não compara texto — output de LLM não é determinístico. Compara o conjunto de
regras citadas na tabela de saída:

  cobertura       toda regra de `espera:` apareceu
  falso positivo  nenhum termo de `nao-marca:` foi marcado

Regra extra não reprova. Uso: ./init.sh   ou   python3 tests/verify.py [caso]
"""
import os
import re
import subprocess
import sys
from pathlib import Path

MODELO = os.environ.get("PTC_MODELO", "sonnet")
TIMEOUT = int(os.environ.get("PTC_TIMEOUT", "300"))
TENTATIVAS = int(os.environ.get("PTC_TENTATIVAS", "3"))
AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent

VERDE, VERMELHO, AMARELO, CINZA, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"


def carregar_skill():
    """Concatena a skill do repo. Testa o arquivo em edição, não o instalado."""
    partes = [REPO / "SKILL.md"]
    partes += sorted((REPO / "references").glob("*.md"))
    faltando = [p for p in partes if not p.exists()]
    if faltando:
        sys.exit(f"erro: arquivo da skill não encontrado: {faltando[0]}")
    return "\n\n---\n\n".join(p.read_text(encoding="utf-8") for p in partes)


def parse_caso(caminho):
    texto = caminho.read_text(encoding="utf-8")
    cabecalho, marcador, entrada = texto.partition("## entrada")
    if not marcador:
        sys.exit(f"erro: {caminho.name} não tem o marcador '## entrada'")
    meta = dict(re.findall(r"^([\w-]+):[ \t]*(.+)$", cabecalho, re.MULTILINE))

    def lista(chave):
        bruto = meta.get(chave, "").strip()
        return [x.strip() for x in bruto.split(",") if x.strip()] if bruto else []

    return {
        "nome": caminho.stem,
        "nivel": meta.get("nivel", "estrito"),
        "espera": lista("espera"),
        "nao_marca": lista("nao-marca"),
        "contra_teste": lista("contra-teste"),
        "entrada": entrada.strip(),
    }


def cobertura(casos):
    """Matriz regra × (caso positivo, contra-teste). Não chama o Claude.

    É o critério de parada mecânico do goal loop em `loops/goal-cobertura.md`:
    uma regra só está coberta quando existe caso que a faz disparar E caso que
    prova que ela não dispara onde não deve.
    """
    pos = {str(n): [] for n in range(1, 9)}
    neg = {str(n): [] for n in range(1, 9)}
    for caminho in casos:
        c = parse_caso(caminho)
        for r in c["espera"]:
            pos.get(r.split("-")[-1], []).append(c["nome"])
        for r in c["contra_teste"]:
            neg.get(r.split("-")[-1], []).append(c["nome"])

    print(f"{'regra':<8}{'positivo':<14}contra-teste")
    for n in map(str, range(1, 9)):
        m = lambda v: f"{VERDE}✓{RESET} ({len(v)})" if v else f"{VERMELHO}✗{RESET}     "
        print(f"PTC-{n:<4}{m(pos[n]):<23}{m(neg[n])}")

    falta_pos = [n for n in map(str, range(1, 9)) if not pos[n]]
    falta_neg = [n for n in map(str, range(1, 9)) if not neg[n]]
    print(f"\npositivo:     {8 - len(falta_pos)}/8"
          + (f"  faltam {', '.join('PTC-' + n for n in falta_pos)}" if falta_pos else "  ✓"))
    print(f"contra-teste: {8 - len(falta_neg)}/8"
          + (f"  faltam {', '.join('PTC-' + n for n in falta_neg)}" if falta_neg else "  ✓"))
    return 1 if (falta_pos or falta_neg) else 0


def rodar(skill, caso):
    prompt = (
        f"{skill}\n\n"
        "---\n\n"
        "Aplique as regras acima ao texto abaixo. "
        f"Nível: {caso['nivel']}. "
        "Responda no formato de saída padrão da skill, com a tabela que nomeia "
        "cada regra PTC violada.\n\n"
        f"{caso['entrada']}"
    )
    # Prompt vai por stdin, não por argv: ele começa com o frontmatter `---`
    # do SKILL.md, que o CLI interpretaria como flag desconhecida.
    try:
        r = subprocess.run(
            ["claude", "-p", "--model", MODELO],
            input=prompt, capture_output=True, text=True, timeout=TIMEOUT,
        )
    except FileNotFoundError:
        sys.exit("erro: `claude` não está no PATH. Instale o Claude Code.")
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        print(f"\n    {CINZA}{r.stderr.strip()[:200]}{RESET}", file=sys.stderr)
        return None
    return r.stdout


INICIO_TEXTO_FINAL = re.compile(r"\*\*Texto final:?\*\*|^#+\s*Texto final", re.IGNORECASE | re.MULTILINE)
FIM_TEXTO_FINAL = re.compile(
    r"\*\*Mantido de propósito|\*\*Não corrigido|\*\*Sinalizado|\*\*Deixado",
    re.IGNORECASE,
)


def texto_final(saida):
    """Extrai só o texto reescrito.

    A tabela de violações repete a frase original inteira na coluna "Original",
    então procurar termos ali acusa falso positivo: `arquivo` e `tela` aparecem
    numa linha de PTC-2 sem terem sido tocados. O texto final é o único lugar
    onde dá para afirmar que a skill mudou — ou não mudou — um termo.
    """
    ini = INICIO_TEXTO_FINAL.search(saida)
    if not ini:
        return None
    resto = saida[ini.end():]
    fim = FIM_TEXTO_FINAL.search(resto)
    return resto[: fim.start()] if fim else resto


def avaliar(caso, saida):
    """Devolve (ok, faltou, corrigidos_indevidamente)."""
    citadas = set(re.findall(r"PTC-([1-8])\b", saida))
    esperadas = {r.split("-")[1] for r in caso["espera"]}
    faltou = sorted(esperadas - citadas, key=int)

    # Contra-teste: o termo tem de sobreviver intacto no texto reescrito.
    alvo = texto_final(saida)
    if alvo is None:
        alvo = saida  # sem seção de texto final, não dá para isolar — usa tudo
    proibidos = [t for t in caso["nao_marca"] if t.lower() not in alvo.lower()]

    return (not faltou and not proibidos), faltou, proibidos


def main():
    casos = sorted((AQUI / "casos").glob("*.md"))
    if not casos:
        sys.exit("erro: nenhum caso encontrado em tests/casos/")

    if "--cobertura" in sys.argv:
        return cobertura(casos)

    if len(sys.argv) > 1:
        casos = [c for c in casos if sys.argv[1] in c.stem]
        if not casos:
            sys.exit(f"erro: nenhum caso casa com '{sys.argv[1]}'")

    skill = carregar_skill()
    print(f"{CINZA}skill: {len(skill.splitlines())} linhas · "
          f"modelo: {MODELO} · {len(casos)} caso(s){RESET}\n")

    falhas = instaveis = 0
    for caminho in casos:
        caso = parse_caso(caminho)
        print(f"{caso['nome']:.<40} ", end="", flush=True)

        # Output de LLM oscila: um caso pode falhar numa rodada e passar na
        # seguinte. Sem retry, a suite acusa regressão que não existe — e pior,
        # cada rodada acusa um caso diferente. Repetir separa quebra de ruído.
        for tentativa in range(1, TENTATIVAS + 1):
            saida = rodar(skill, caso)
            if saida is None:
                ok, faltou, proibidos = False, [], []
                continue
            ok, faltou, proibidos = avaliar(caso, saida)
            if ok:
                break

        n = len(caso["espera"])
        if ok and tentativa == 1:
            print(f"{VERDE}PASS{RESET}  ({n}/{n} regras)")
        elif ok:
            instaveis += 1
            print(f"{AMARELO}FLAKY{RESET} (passou na {tentativa}ª de {TENTATIVAS})")
        else:
            falhas += 1
            print(f"{VERMELHO}FAIL{RESET}  ({TENTATIVAS} tentativas)")
            if faltou:
                print(f"    faltou:          {', '.join('PTC-' + x for x in faltou)}")
            if proibidos:
                print(f"    corrigiu indevidamente: {', '.join(proibidos)}")
            # Sem nenhum dos dois: nunca houve resposta para avaliar. Continua
            # FAIL — caso não verificado não é caso verde —, mas dizer qual das
            # duas coisas aconteceu é o que separa quebra da skill de ruído de
            # infra. Sem esta linha as duas saem idênticas na tela.
            if not faltou and not proibidos:
                print(f"    {CINZA}sem resposta do modelo (timeout de {TIMEOUT}s ou "
                      f"erro da API) — não é regressão da skill{RESET}")

    total = len(casos)
    print(f"\n{total - falhas}/{total} casos ok", end="")
    print(f" · {AMARELO}{instaveis} instável(is){RESET}" if instaveis else "")
    if instaveis:
        print(f"{CINZA}flaky recorrente = asserção frágil ou regra ambígua. "
              f"Ver AGENTS.md.{RESET}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
