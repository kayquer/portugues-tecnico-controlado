#!/usr/bin/env python3
"""Gera as versões portáteis da skill a partir de SKILL.md + references/.

A skill é escrita para o Claude Code: frontmatter YAML e `references/` carregadas
sob demanda por caminho relativo. Fora dali nada disso existe, então o bundle
achatado precisa de três consertos — tirar o frontmatter, tirar o aviso de edição,
e reescrever os caminhos que apontariam para arquivos ausentes.

  python3 tools/build.py              escreve dist/ e docs/index.html
  python3 tools/build.py --verificar  não escreve; exit 1 se algo estiver defasado

O `--verificar` roda no init.sh antes dos casos: é grátis, não chama a API, e é
o que impede dist/ e docs/ de divergirem do prompt sem ninguém notar.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ORIGEM = "https://github.com/kayquer/portugues-tecnico-controlado"

# Seções que o compacto corta. Se uma delas sumir do SKILL.md, o build morre em
# vez de emitir um bundle silenciosamente truncado — renomear um H2 passa a ser
# um erro visível.
CORTA_NO_COMPACTO = ("Por que não é o STE traduzido", "Limites", "Referências")
# Do léxico o compacto leva as duas tabelas que substituem o dicionário da ASD,
# mais as siglas: a PTC-6 manda aplicar o glossário de siglas por nome, e sem a
# seção o compacto prometeria uma coisa que não está nele.
MANTEM_DO_LEXICO = ("Evite → use", "Conectores ambíguos", "Siglas")

NOTA_PACOTE = (
    "Este arquivo é o pacote completo. Onde o texto mandar consultar outra seção, "
    "ela já está aqui embaixo — não há arquivo externo para carregar."
)


def erro(msg):
    sys.exit(f"erro: {msg}")


def le(caminho):
    p = REPO / caminho
    if not p.exists():
        erro(f"arquivo não encontrado: {caminho}")
    return p.read_text(encoding="utf-8")


def frontmatter(texto):
    """Separa o frontmatter YAML do corpo. Devolve (campos, corpo)."""
    if not texto.startswith("---\n"):
        erro("SKILL.md não começa com frontmatter YAML")
    _, bruto, corpo = texto.split("---\n", 2)
    campos = dict(re.findall(r"^(\w+):\s*(.+)$", bruto, re.MULTILINE))
    return campos, corpo.lstrip("\n")


def secoes(texto):
    """Fatia um markdown em [(titulo_h2 ou None, bloco)], preservando a ordem."""
    partes = re.split(r"^(## .+)$", texto, flags=re.MULTILINE)
    saida = [(None, partes[0])]
    for titulo, corpo in zip(partes[1::2], partes[2::2]):
        saida.append((titulo[3:].strip(), titulo + corpo))
    return saida


FORA_DO_COMPACTO = "a versão completa desta skill"


def reescreve_caminhos(texto, refs, presentes):
    """Troca `references/X.md` pelo que existe de fato no bundle.

    Reference que entrou vira o título da seção dela. Reference que ficou de
    fora — no compacto, ortografia e inglês ficam — aponta para a versão
    completa. Mandar para uma seção ausente seria pior que o caminho quebrado.
    """
    for r in refs:
        alvo = f"references/{r['arquivo']}"
        destino = f'a seção "{r["titulo"]}"' if r["arquivo"] in presentes else FORA_DO_COMPACTO
        for forma in (f"`{alvo}`", alvo, f"`{r['arquivo']}`"):
            texto = texto.replace(forma, destino)
    # O destino começa com artigo, e o caminho substituído vinha depois de
    # preposição: "estão em `references/x.md`" viraria "estão em a seção".
    # Numa skill de português controlado isso é a pior vitrine possível.
    texto = re.sub(r"\bem (a (?:seção|versão))", r"n\1", texto)
    texto = re.sub(r"\bde (a (?:seção|versão))", r"d\1", texto)
    return texto


def monta_completo(skill_corpo, refs):
    texto = "\n\n---\n\n".join([skill_corpo] + [r["texto"] for r in refs])
    for r in refs:
        if f"references/{r['arquivo']}" not in texto:
            erro(f"references/{r['arquivo']} não é citado em lugar nenhum — "
                 "o mapa de seções está errado")
    return reescreve_caminhos(texto, refs, {r["arquivo"] for r in refs})


# Exemplo didático: some no compacto. Nota normativa em blockquote (o `>` da
# PTC-6 sobre variante europeia) fica — é regra, não ilustração.
EXEMPLO = re.compile(r"^>.*[❌✅⚠️]")


def monta_compacto(skill_corpo, refs):
    blocos = []
    vistos = set()
    for titulo, bloco in secoes(skill_corpo):
        if titulo in CORTA_NO_COMPACTO:
            vistos.add(titulo)
            continue
        blocos.append(bloco)
    faltando = set(CORTA_NO_COMPACTO) - vistos
    if faltando:
        erro(f"seção que o compacto corta não existe mais no SKILL.md: {sorted(faltando)}")

    lexico = next((r for r in refs if r["arquivo"] == "lexico.md"), None)
    if lexico is None:
        erro("references/lexico.md sumiu — o compacto depende dele")
    tabelas, vistas = [], set()
    for titulo, bloco in secoes(lexico["texto"]):
        if titulo in MANTEM_DO_LEXICO:
            vistas.add(titulo)
            tabelas.append(bloco)
    faltando = set(MANTEM_DO_LEXICO) - vistas
    if faltando:
        erro(f"seção que o compacto mantém não existe mais no léxico: {sorted(faltando)}")

    texto = "".join(blocos).rstrip() + "\n\n---\n\n# " + lexico["titulo"] + "\n\n" + "".join(tabelas)
    texto = reescreve_caminhos(texto, refs, {"lexico.md"})
    texto = "\n".join(l for l in texto.splitlines() if not EXEMPLO.match(l))
    # Cada exemplo removido deixa o buraco dele. Sem isso o compacto sai com
    # três e quatro linhas em branco seguidas onde havia um bloco ❌/✅.
    return re.sub(r"\n{3,}", "\n\n", texto).rstrip() + "\n"


def cabecalho(titulo, versao, subtitulo):
    return (
        f"# {titulo}\n\n"
        f"{subtitulo}\n\n"
        f"Versão {versao} · {ORIGEM}\n\n"
        f"{NOTA_PACOTE}\n\n---\n\n"
    )


def gerar():
    campos, corpo = frontmatter(le("SKILL.md"))
    versao = campos.get("version", "0.0.0")
    descricao = campos.get("description", "").strip('"').split(" Triggers -")[0]

    # Tira o aviso HTML para quem edita a skill: fora do repo ele não faz sentido
    # e ainda manda o leitor abrir um AGENTS.md que ele não tem.
    corpo = re.sub(r"^<!--.*?-->\n+", "", corpo, count=1, flags=re.DOTALL)

    refs = []
    for p in sorted((REPO / "references").glob("*.md")):
        texto = p.read_text(encoding="utf-8")
        refs.append({"arquivo": p.name, "texto": texto,
                     "titulo": texto.splitlines()[0].lstrip("# ").strip()})
    if not refs:
        erro("references/ está vazio")

    completo = monta_completo(corpo, refs)
    compacto = monta_compacto(corpo, refs)

    curto = "Reescreve texto técnico em português do Brasil para ter uma leitura só."
    saidas = {
        "dist/ptc-completo.md":
            cabecalho("Português Técnico Controlado (PTC)", versao, descricao) + completo,
        "dist/ptc-compacto.md":
            cabecalho("Português Técnico Controlado (PTC) — versão curta", versao,
                      curto + " Versão reduzida, sem exemplos: para campo de instrução "
                      "com limite de caracteres.") + compacto,
        # Não se chama AGENTS.md de propósito. Codex e opencode leem AGENTS.md
        # aninhado, e um dentro de dist/ mandaria o agente reescrever este repo
        # em português controlado — o oposto do que o AGENTS.md da raiz manda.
        # O `curl -o AGENTS.md` do destino resolve o nome no download.
        "dist/ptc-agents.md":
            cabecalho("Português Técnico Controlado (PTC)", versao,
                      descricao + "\n\nSalve este arquivo como `AGENTS.md` na raiz do seu "
                      "projeto. Codex, opencode, Jules e Aider o leem automaticamente; "
                      "o Gemini CLI espera o mesmo conteúdo em `GEMINI.md`.") + completo,
        "dist/ptc.mdc":
            "---\n"
            f"description: {curto}\n"
            "alwaysApply: false\n"
            "---\n\n" + cabecalho("Português Técnico Controlado (PTC)", versao, descricao)
            + completo,
        "dist/ptc-chat.txt":
            cabecalho("Português Técnico Controlado (PTC) — versão curta", versao,
                      curto + " Cole em instruções de Projeto (ChatGPT), Space "
                      "(Perplexity) ou instrução de sistema.") + compacto,
    }

    modelo = le("tools/index.template.html")
    for marca in ("{{COMPLETO}}", "{{COMPACTO}}", "{{VERSAO}}"):
        if marca not in modelo:
            erro(f"tools/index.template.html não tem o marcador {marca}")
    # `</script` fecharia o bloco text/plain que carrega os bundles na página.
    escapa = lambda t: t.replace("</script", "<\\/script")
    saidas["docs/index.html"] = (modelo
                                 .replace("{{COMPLETO}}", escapa(saidas["dist/ptc-completo.md"]))
                                 .replace("{{COMPACTO}}", escapa(saidas["dist/ptc-compacto.md"]))
                                 .replace("{{VERSAO}}", versao))
    return saidas


def main():
    saidas = gerar()
    verificar = "--verificar" in sys.argv

    if verificar:
        defasados = [n for n, c in saidas.items()
                     if not (REPO / n).exists() or (REPO / n).read_text(encoding="utf-8") != c]
        if defasados:
            print("defasado (rode `python3 tools/build.py`):", file=sys.stderr)
            for n in defasados:
                print(f"  {n}", file=sys.stderr)
            return 1
        print(f"dist/ e docs/ em dia ({len(saidas)} arquivos)")
        return 0

    for nome, conteudo in saidas.items():
        destino = REPO / nome
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(conteudo, encoding="utf-8")
        print(f"  {nome}  ({len(conteudo) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
