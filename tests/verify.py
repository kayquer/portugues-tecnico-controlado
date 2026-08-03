#!/usr/bin/env python3
"""Runner de regressão da skill PTC.

Roda cada caso de `casos/` contra o SKILL.md **deste repo** (não a cópia
instalada em ~/.claude/skills/) e confere quais regras PTC dispararam.

Não compara texto — output de LLM não é determinístico. Verifica três coisas:

  cobertura       toda regra de `espera:` apareceu na tabela de violações
  falso positivo  todo termo de `nao-marca:` sobreviveu no texto final
  âncora          todo termo de `deve-conter:` apareceu na saída

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

REGRAS = [str(n) for n in range(1, 9)]  # PTC-1..PTC-8
NIVEIS = ("estrito", "descritivo", "leve")
CHAVES = ("nivel", "espera", "nao-marca", "contra-teste",
          "bilingue", "destinatario", "deve-conter")


def carregar_skill():
    """Concatena a skill do repo. Testa o arquivo em edição, não o instalado."""
    partes = [REPO / "SKILL.md"]
    partes += sorted((REPO / "references").glob("*.md"))
    faltando = [p for p in partes if not p.exists()]
    if faltando:
        sys.exit(f"erro: arquivo da skill não encontrado: {faltando[0]}")
    return "\n\n---\n\n".join(p.read_text(encoding="utf-8") for p in partes)


def parse_caso(caminho):
    """Lê e **valida** um caso. Erro de cabeçalho mata o runner, não vira verde.

    Um caso é uma asserção. Chave com typo, regra inexistente ou contra-teste
    sem termo que sobreviva produzem um caso que passa sem verificar nada — e
    um caso desses é pior que caso nenhum, porque conta como cobertura.
    """
    def erro(msg):
        sys.exit(f"erro: {caminho.name}: {msg}")

    texto = caminho.read_text(encoding="utf-8")
    cabecalho, marcador, entrada = texto.partition("## entrada")
    if not marcador:
        erro("não tem o marcador '## entrada'")
    meta = dict(re.findall(r"^([\w-]+):[ \t]*(.+)$", cabecalho, re.MULTILINE))

    if desconhecidas := sorted(set(meta) - set(CHAVES)):
        erro(f"chave desconhecida: {', '.join(desconhecidas)}"
             f"\n       conhecidas: {', '.join(CHAVES)}")

    def lista(chave):
        bruto = meta.get(chave, "").strip()
        return [x.strip() for x in bruto.split(",") if x.strip()] if bruto else []

    def regras(chave):
        """Normaliza `PTC-4` para `4` e recusa o que não é regra."""
        saida = []
        for r in lista(chave):
            n = r.split("-")[-1]
            if n not in REGRAS:
                erro(f"{chave}: '{r}' não é regra (esperado PTC-1..PTC-{REGRAS[-1]})")
            saida.append(n)
        return saida

    caso = {
        "nome": caminho.stem,
        "nivel": meta.get("nivel", "estrito").strip(),
        "destinatario": meta.get("destinatario", "").strip(),
        "bilingue": meta.get("bilingue", "").strip().lower() in ("sim", "yes", "true"),
        "espera": regras("espera"),
        "nao_marca": lista("nao-marca"),
        "contra_teste": regras("contra-teste"),
        "deve_conter": lista("deve-conter"),
        "entrada": entrada.strip(),
    }

    if caso["nivel"] not in NIVEIS:
        erro(f"nivel: '{caso['nivel']}' não existe (use {', '.join(NIVEIS)})")
    if not (caso["espera"] or caso["nao_marca"] or caso["deve_conter"]):
        erro("nenhuma asserção — 'espera', 'nao-marca' e 'deve-conter' vazios.\n"
             "       Um caso assim passa verde sem verificar nada. "
             "Causa comum: typo no nome da chave.")
    # `contra-teste` só alimenta a matriz de cobertura; quem assere é `nao-marca`.
    # Sem essa checagem, declarar a regra bastava para a matriz contá-la coberta.
    # ponytail: exige `nao-marca` não vazio, não um termo por regra — amarrar
    # termo↔regra pediria anotação por termo. Subir isso se um caso com 2
    # contra-testes e 1 termo virar problema de verdade.
    if caso["contra_teste"] and not caso["nao_marca"]:
        erro("'contra-teste' declara regra mas 'nao-marca' está vazio.\n"
             "       A matriz contaria a regra como coberta sem asserção nenhuma.")
    return caso


def cobertura(casos):
    """Matriz regra × (caso positivo, contra-teste). Não chama o Claude.

    É o critério de parada mecânico do goal loop em `loops/goal-cobertura.md`:
    uma regra só está coberta quando existe caso que a faz disparar E caso que
    prova que ela não dispara onde não deve.
    """
    pos = {n: [] for n in REGRAS}
    neg = {n: [] for n in REGRAS}
    for caminho in casos:
        c = parse_caso(caminho)
        for n in c["espera"]:
            pos[n].append(c["nome"])
        for n in c["contra_teste"]:
            neg[n].append(c["nome"])

    print(f"{'regra':<8}{'positivo':<14}contra-teste")
    for n in REGRAS:
        m = lambda v: f"{VERDE}✓{RESET} ({len(v)})" if v else f"{VERMELHO}✗{RESET}     "
        print(f"PTC-{n:<4}{m(pos[n]):<23}{m(neg[n])}")

    total = len(REGRAS)
    falta_pos = [n for n in REGRAS if not pos[n]]
    falta_neg = [n for n in REGRAS if not neg[n]]
    print(f"\npositivo:     {total - len(falta_pos)}/{total}"
          + (f"  faltam {', '.join('PTC-' + n for n in falta_pos)}" if falta_pos else "  ✓"))
    print(f"contra-teste: {total - len(falta_neg)}/{total}"
          + (f"  faltam {', '.join('PTC-' + n for n in falta_neg)}" if falta_neg else "  ✓"))
    return 1 if (falta_pos or falta_neg) else 0


def rodar(skill, caso):
    # Os três parâmetros do Passo 0 da skill. `destinatario` e `bilingue` só
    # mudam o comportamento se chegarem ao prompt — antes eram lidos do
    # cabeçalho e descartados, e o caso bilíngue passava só porque a própria
    # entrada pedia o par EN/PT em prosa.
    params = f"Nível: {caso['nivel']}."
    if caso["destinatario"]:
        params += f" Destinatário: {caso['destinatario']}."
    if caso["bilingue"]:
        params += " Bilíngue: sim."
    prompt = (
        f"{skill}\n\n"
        "---\n\n"
        "Aplique as regras acima ao texto abaixo. "
        f"{params} "
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
    """Devolve (ok, faltou, corrigidos_indevidamente, nao_apareceu)."""
    citadas = set(re.findall(r"PTC-(\d+)\b", saida))
    faltou = sorted(set(caso["espera"]) - citadas, key=int)

    # Contra-teste: o termo tem de sobreviver intacto no texto reescrito.
    alvo = texto_final(saida) or saida  # sem seção final, não dá para isolar
    proibidos = [t for t in caso["nao_marca"] if t.lower() not in alvo.lower()]

    # `deve-conter` procura na saída **inteira**, não no texto final: o que ele
    # existe para provar — tabela de proposições do modo bilíngue, registro do
    # linter reverso — fica fora do texto reescrito por desenho.
    ausentes = [t for t in caso["deve_conter"] if t.lower() not in saida.lower()]

    return (not (faltou or proibidos or ausentes)), faltou, proibidos, ausentes


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
                ok, faltou, proibidos, ausentes = False, [], [], []
                continue
            ok, faltou, proibidos, ausentes = avaliar(caso, saida)
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
            if ausentes:
                print(f"    não apareceu:    {', '.join(ausentes)}")
            # Sem nenhum dos três: nunca houve resposta para avaliar. Continua
            # FAIL — caso não verificado não é caso verde —, mas dizer qual das
            # duas coisas aconteceu é o que separa quebra da skill de ruído de
            # infra. Sem esta linha as duas saem idênticas na tela.
            if not (faltou or proibidos or ausentes):
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
