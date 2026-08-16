#!/usr/bin/env python3
"""Runner de regressão da skill PTC.

Roda cada caso de `casos/` contra o SKILL.md **deste repo** (não a cópia
instalada em ~/.claude/skills/) e confere quais regras PTC dispararam.

Não compara texto — output de LLM não é determinístico. Verifica quatro coisas:

  cobertura       toda regra de `espera:` apareceu na tabela de violações
  falso positivo  todo termo de `nao-marca:` sobreviveu no texto final
  âncora          todo termo de `deve-conter:` apareceu na saída
  legibilidade    o texto final passa dos limiares `flesch-min:`/`pal-frase-max:`

Regra extra não reprova. Uso: ./init.sh   ou   python3 tests/verify.py [caso]
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import legibilidade

MODELO = os.environ.get("PTC_MODELO", "sonnet")
# Automatiza o passo que o AGENTS.md manda fazer à mão: um caso que falha em
# modelo menor pode ter sido corrigido sem a regra ter sido citada. Concluir
# quebra da skill sem checar isso é o erro caro. Vazio desliga.
MODELO_ESCALA = os.environ.get("PTC_MODELO_ESCALA", "opus").strip()
TIMEOUT = int(os.environ.get("PTC_TIMEOUT", "300"))
TENTATIVAS = int(os.environ.get("PTC_TENTATIVAS", "3"))
# Contra-teste escrito junto com a regra testa a leitura legítima óbvia. O
# adversarial testa português correto que *se parece* com a violação — outra
# coisa. Ver loops/goal-falso-positivo.md.
ADVERSARIAL = os.environ.get("PTC_ADVERSARIAL", "") not in ("", "0")
PREFIXO_ADV = "caso-adv"
AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent

VERDE, VERMELHO, AMARELO, CINZA, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"

REGRAS = [str(n) for n in range(1, 9)]  # PTC-1..PTC-8
NIVEIS = ("estrito", "descritivo", "leve")
CHAVES = ("nivel", "espera", "nao-marca", "contra-teste",
          "bilingue", "destinatario", "deve-conter",
          "flesch-min", "pal-frase-max")
# Rótulos de falha, na ordem em que saem na tela. `métrica` é o único que não
# escala para o modelo caro — ver `veredito`.
ROTULOS = ("faltou", "corrigiu indevidamente", "não apareceu", "métrica")


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

    def numero(chave, lo, hi):
        """Lê um limiar. Fora da faixa ou não numérico, mata o runner.

        `flesch-min: alto` explodiria com ValueError no meio de uma rodada
        paga; `flesch-min: 250` é inalcançável e daria FAIL permanente que
        parece regressão da skill.
        """
        bruto = meta.get(chave, "").strip()
        if not bruto:
            return None
        try:
            v = float(bruto.replace(",", "."))
        except ValueError:
            erro(f"{chave}: '{bruto}' não é número")
        if not lo <= v <= hi:
            erro(f"{chave}: {v:g} fora da faixa [{lo:g}, {hi:g}]")
        return v

    caso = {
        "nome": caminho.stem,
        "nivel": meta.get("nivel", "estrito").strip(),
        "destinatario": meta.get("destinatario", "").strip(),
        "bilingue": meta.get("bilingue", "").strip().lower() in ("sim", "yes", "true"),
        "espera": regras("espera"),
        "nao_marca": lista("nao-marca"),
        "contra_teste": regras("contra-teste"),
        "deve_conter": lista("deve-conter"),
        # Limiar de legibilidade do **texto final**. Só existe onde foi medido
        # — ver "O limiar se mede, não se chuta" no AGENTS.md.
        # Faixa larga de propósito: a escala de Martins é nominal, não limitada.
        # Medido neste repo — burocratês 35, o caso-01 cru 52, reescrita PTC boa
        # ~104, período único de palavras longas −79. O teto real da fórmula é
        # ~163 (uma palavra monossilábica por frase); acima disso o limiar é
        # inalcançável e vira FAIL permanente com cara de regressão.
        "flesch_min": numero("flesch-min", -100, 160),
        "pal_frase_max": numero("pal-frase-max", 1, 100),
        "entrada": entrada.strip(),
    }

    if caso["nivel"] not in NIVEIS:
        erro(f"nivel: '{caso['nivel']}' não existe (use {', '.join(NIVEIS)})")
    # Limiar conta como asserção: o guard existe contra typo que produz verde
    # silencioso, e chave válida com número válido não é typo — ela assere algo
    # medido.
    if not (caso["espera"] or caso["nao_marca"] or caso["deve_conter"]
            or caso["flesch_min"] is not None or caso["pal_frase_max"] is not None):
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

    Com `PTC_ADVERSARIAL=1`, a segunda coluna só conta `caso-adv-*` — critério
    de `loops/goal-falso-positivo.md`. Contar contra-teste total não serviria
    ali: a matriz já está fechada, e regra com 4 contra-testes escritos junto
    com ela sairia "pronta" sem uma linha adversarial.
    """
    rotulo = "adversarial" if ADVERSARIAL else "contra-teste"
    pos = {n: [] for n in REGRAS}
    neg = {n: [] for n in REGRAS}
    for caminho in casos:
        c = parse_caso(caminho)
        for n in c["espera"]:
            pos[n].append(c["nome"])
        if ADVERSARIAL and not c["nome"].startswith(PREFIXO_ADV):
            continue
        for n in c["contra_teste"]:
            neg[n].append(c["nome"])

    print(f"{'regra':<8}{'positivo':<14}{rotulo}")
    for n in REGRAS:
        m = lambda v: f"{VERDE}✓{RESET} ({len(v)})" if v else f"{VERMELHO}✗{RESET}     "
        print(f"PTC-{n:<4}{m(pos[n]):<23}{m(neg[n])}")

    total = len(REGRAS)
    falta_pos = [n for n in REGRAS if not pos[n]]
    falta_neg = [n for n in REGRAS if not neg[n]]
    print(f"\npositivo:     {total - len(falta_pos)}/{total}"
          + (f"  faltam {', '.join('PTC-' + n for n in falta_pos)}" if falta_pos else "  ✓"))
    print(f"{rotulo + ':':<14}{total - len(falta_neg)}/{total}"
          + (f"  faltam {', '.join('PTC-' + n for n in falta_neg)}" if falta_neg else "  ✓"))
    return 1 if (falta_pos or falta_neg) else 0


def rodar(skill, caso, modelo=MODELO):
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
            ["claude", "-p", "--model", modelo],
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


def checar_metrica(caso, alvo):
    """Compara o texto final com os limiares do caso. Devolve falhas.

    Sai na primeira linha quando o caso não declara limiar — assim o textstat
    nem chega a ser importado nos casos que não pediram métrica.
    """
    if caso["flesch_min"] is None and caso["pal_frase_max"] is None:
        return []
    # Sem fallback para a saída inteira (ao contrário de `nao-marca`): medir a
    # tabela de violações — que repete a frase original, tem pipes e nomes de
    # regra — dá um número que passa ou reprova por acidente.
    if alvo is None:
        return [("métrica", "não achei o 'Texto final:' na saída — não dá para medir")]
    m = legibilidade.medir(alvo)
    if m is None:
        return [("métrica", "texto curto demais para medir (nenhuma palavra)")]

    fora = []
    if caso["flesch_min"] is not None and m.flesch < caso["flesch_min"]:
        fora.append(("métrica", f"flesch {m.flesch:.1f} < {caso['flesch_min']:g}"))
    if caso["pal_frase_max"] is not None and m.pal_frase > caso["pal_frase_max"]:
        fora.append(("métrica",
                     f"palavras/frase {m.pal_frase:.1f} > {caso['pal_frase_max']:g}"))
    return fora


def avaliar(caso, saida):
    """Devolve (ok, falhas), com `falhas` = [(rótulo, detalhe)], vazia se passou.

    Lista de pares em vez de uma variável por asserção: eram três, viraram
    quatro, e cada asserção nova mudava a aridade de `avaliar`, `veredito` e
    `main` ao mesmo tempo. Agora nenhuma das três muda de novo.
    """
    falhas = []
    citadas = set(re.findall(r"PTC-(\d+)\b", saida))
    falhas += [("faltou", f"PTC-{n}")
               for n in sorted(set(caso["espera"]) - citadas, key=int)]

    alvo = texto_final(saida)
    # Contra-teste: o termo tem de sobreviver intacto no texto reescrito. Sem
    # seção final não dá para isolar, e o fallback para a saída inteira facilita
    # achar o termo — erra para o lado de não reprovar, de propósito. A métrica
    # não cai nesse fallback (ver `checar_metrica`): lá ele não teria direção.
    falhas += [("corrigiu indevidamente", t) for t in caso["nao_marca"]
               if t.lower() not in (alvo or saida).lower()]

    # `deve-conter` procura na saída **inteira**, não no texto final: o que ele
    # existe para provar — tabela de proposições do modo bilíngue, registro do
    # linter reverso — fica fora do texto reescrito por desenho.
    falhas += [("não apareceu", t) for t in caso["deve_conter"]
               if t.lower() not in saida.lower()]

    falhas += checar_metrica(caso, alvo)
    return (not falhas), falhas


def veredito(skill, caso):
    """Roda o caso até decidir. Devolve (estado, tentativa, falhas).

    Separado de `main` porque é a única lógica de decisão do runner e é a que
    não dá para verificar com chamada real: reproduzir um `ESCALOU` de verdade
    depende do modelo menor falhar, que é justamente o que não se controla.
    `tests/test_runner.py` a exercita com `rodar` dublado.
    """
    falhas = []

    # Output de LLM oscila: um caso pode falhar numa rodada e passar na
    # seguinte. Sem retry, a suite acusa regressão que não existe — e pior,
    # cada rodada acusa um caso diferente. Repetir separa quebra de ruído.
    for tentativa in range(1, TENTATIVAS + 1):
        saida = rodar(skill, caso)
        if saida is None:
            falhas = []  # sem resposta, não há o que avaliar
            continue
        ok, falhas = avaliar(caso, saida)
        if ok:
            return ("PASS" if tentativa == 1 else "FLAKY"), tentativa, []

    # Modelo menor às vezes aplica a correção e não cita a regra na tabela, e a
    # asserção lê a tabela. Antes isto era passo manual do AGENTS.md, e
    # esquecê-lo faz um FAIL de rótulo passar por quebra da skill.
    #
    # Métrica fica **fora** do gatilho: `ESCALOU` quer dizer uma coisa só — o
    # modelo menor aplicou a correção e não citou a regra. Texto difícil de ler
    # não é colisão de rótulo, e opus reescrever melhor não desmente regressão
    # nenhuma; escalar por métrica gastaria o modelo caro e ainda etiquetaria um
    # FAIL legítimo como problema de citação, envenenando o loop-state.
    # `falhas` vazia = timeout, e depois de timeout escalar gasta em nada.
    escalavel = [f for f in falhas if f[0] != "métrica"]
    if MODELO_ESCALA and MODELO_ESCALA != MODELO and escalavel:
        saida = rodar(skill, caso, MODELO_ESCALA)
        if saida is not None:
            ok, falhas = avaliar(caso, saida)
            if ok:
                return "ESCALOU", tentativa, []

    return "FAIL", tentativa, falhas


def metricas(skill, casos):
    """Mede antes/depois de cada caso e **imprime**. Não gateia, sempre sai 0.

    É o instrumento de calibração dos limiares. O AGENTS.md já manda medir
    âncora antes de escrevê-la ("Âncora se mede, não se chuta"); limiar é a
    mesma doutrina. Escrever `flesch-min` sem rodar isto 5× produz um gate que
    reprova por oscilação normal do modelo — FLAKY permanente que some no ruído.

    Se este modo reprovasse, ele viraria o gate e o limiar continuaria chutado.
    Por isso `return 0` sempre. Custa 1 chamada por caso: não é grátis como
    `--cobertura`.
    """
    def fmt(m):
        return f"flesch {m.flesch:6.1f} · p/f {m.pal_frase:5.1f}" if m else f"{'—':>25}"

    print(f"{'caso':<34}{'entrada':<28}{'texto final':<28}Δ")
    for caminho in casos:
        caso = parse_caso(caminho)
        print(f"{caso['nome']:.<34}", end="", flush=True)
        antes = legibilidade.medir(caso["entrada"])
        saida = rodar(skill, caso)
        depois = legibilidade.medir(texto_final(saida)) if saida else None
        delta = (f"{depois.flesch - antes.flesch:+.1f} / "
                 f"{depois.pal_frase - antes.pal_frase:+.1f}" if antes and depois
                 else f"{CINZA}sem medida{RESET}")
        print(f"{fmt(antes):<28}{fmt(depois):<28}{delta}")
    print(f"\n{CINZA}Δ = flesch / palavras-por-frase. Rode 5× e use o PIOR "
          f"'texto final' como base do limiar. Ver AGENTS.md.{RESET}")
    return 0


def main():
    casos = sorted((AQUI / "casos").glob("*.md"))
    if not casos:
        sys.exit("erro: nenhum caso encontrado em tests/casos/")

    if "--cobertura" in sys.argv:
        return cobertura(casos)

    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if argumentos:
        casos = [c for c in casos if argumentos[0] in c.stem]
        if not casos:
            sys.exit(f"erro: nenhum caso casa com '{argumentos[0]}'")

    skill = carregar_skill()

    if "--metricas" in sys.argv:
        return metricas(skill, casos)

    print(f"{CINZA}skill: {len(skill.splitlines())} linhas · "
          f"modelo: {MODELO} · {len(casos)} caso(s){RESET}\n")

    reprovados = instaveis = escalados = com_metrica = 0
    for caminho in casos:
        caso = parse_caso(caminho)
        print(f"{caso['nome']:.<40} ", end="", flush=True)

        estado, tentativa, falhas = veredito(skill, caso)

        n = len(caso["espera"])
        if estado == "ESCALOU":
            escalados += 1
            print(f"{AMARELO}ESCALOU{RESET} (falhou em {MODELO}, passou em {MODELO_ESCALA})")
        elif estado == "PASS":
            print(f"{VERDE}PASS{RESET}  ({n}/{n} regras)")
        elif estado == "FLAKY":
            instaveis += 1
            print(f"{AMARELO}FLAKY{RESET} (passou na {tentativa}ª de {TENTATIVAS})")
        else:
            reprovados += 1
            com_metrica += any(r == "métrica" for r, _ in falhas)
            print(f"{VERMELHO}FAIL{RESET}  ({TENTATIVAS} tentativas)")
            for rotulo in ROTULOS:
                itens = [d for r, d in falhas if r == rotulo]
                if itens:
                    print(f"    {rotulo + ':':<24}{', '.join(itens)}")
            # Lista vazia: nunca houve resposta para avaliar. Continua FAIL —
            # caso não verificado não é caso verde —, mas dizer qual das duas
            # coisas aconteceu é o que separa quebra da skill de ruído de infra.
            # Sem esta linha as duas saem idênticas na tela.
            if not falhas:
                print(f"    {CINZA}sem resposta do modelo (timeout de {TIMEOUT}s ou "
                      f"erro da API) — não é regressão da skill{RESET}")

    total = len(casos)
    print(f"\n{total - reprovados}/{total} casos ok", end="")
    extra = []
    if instaveis:
        extra.append(f"{instaveis} instável(is)")
    if escalados:
        extra.append(f"{escalados} escalado(s)")
    print(f" · {AMARELO}{' · '.join(extra)}{RESET}" if extra else "")
    if instaveis:
        print(f"{CINZA}flaky recorrente = asserção frágil ou regra ambígua. "
              f"Ver AGENTS.md.{RESET}")
    if escalados:
        print(f"{CINZA}escalado = {MODELO} não citou a regra que aplicou. "
              f"É rótulo, não quebra — mas olhe a saída bruta.{RESET}")
    if com_metrica:
        print(f"{CINZA}métrica fora de faixa não escala para {MODELO_ESCALA} — é "
              f"legibilidade, não rótulo. Rode --metricas 5× antes de mexer no "
              f"limiar.{RESET}")
    return 1 if reprovados else 0


if __name__ == "__main__":
    sys.exit(main())
