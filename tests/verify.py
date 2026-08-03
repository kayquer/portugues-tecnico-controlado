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
AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent

VERDE, VERMELHO, CINZA, RESET = "\033[32m", "\033[31m", "\033[90m", "\033[0m"


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
        "entrada": entrada.strip(),
    }


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
    if len(sys.argv) > 1:
        casos = [c for c in casos if sys.argv[1] in c.stem]
    if not casos:
        sys.exit("erro: nenhum caso encontrado em tests/casos/")

    skill = carregar_skill()
    print(f"{CINZA}skill: {len(skill.splitlines())} linhas · "
          f"modelo: {MODELO} · {len(casos)} caso(s){RESET}\n")

    falhas = 0
    for caminho in casos:
        caso = parse_caso(caminho)
        print(f"{caso['nome']:.<40} ", end="", flush=True)

        saida = rodar(skill, caso)
        if saida is None:
            print(f"{VERMELHO}ERRO{RESET}  (claude falhou ou estourou o timeout)")
            falhas += 1
            continue

        ok, faltou, proibidos = avaliar(caso, saida)
        if ok:
            print(f"{VERDE}PASS{RESET}  ({len(caso['espera'])}/{len(caso['espera'])} regras)")
        else:
            falhas += 1
            print(f"{VERMELHO}FAIL{RESET}")
            if faltou:
                print(f"    faltou:          {', '.join('PTC-' + n for n in faltou)}")
            if proibidos:
                print(f"    corrigiu indevidamente: {', '.join(proibidos)}")

    total = len(casos)
    print(f"\n{total - falhas}/{total} casos ok")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
