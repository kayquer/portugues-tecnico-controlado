#!/usr/bin/env python3
"""Legibilidade em PT-BR sobre os **contadores** do textstat.

O textstat NÃO tem português. `LANG_CONFIGS` (`backend/utils/constants.py`,
v0.7.12) tem `en, de, es, fr, it, nl, pl, ru, hu` — e `set_lang("pt_BR")` **não
levanta erro**: cai nas constantes do inglês em silêncio. `flesch_reading_ease`
sobre texto português devolve um número calibrado para inglês. Número errado,
sem aviso — que é o pecado capital deste repo, não uma imprecisão aceitável.

Por isso daqui só se usa o que é válido em PT:

    syllable_count   via Pyphen, que tem `hyph_pt_BR.dic` — `set_lang` muda isto
    lexicon_count    palavras
    sentence_count   frases

E a fórmula é **nossa**: Flesch adaptado ao PT-BR por Martins et al. 1996 (USP
São Carlos), que reescreve os pesos porque palavra em português é cerca de três
vezes maior que em inglês.

    248,835 − 1,015 · (palavras/frases) − 84,6 · (sílabas/palavras)

Nada aqui sai na tela do usuário da skill. É instrumento de harness: os limiares
`flesch-min:` / `pal-frase-max:` dos casos em `tests/casos/`.
"""
import re
import sys
from collections import namedtuple

Medida = namedtuple("Medida", "flesch pal_frase sil_pal palavras frases")

try:
    import textstat as _ts_mod
except ImportError:
    _ts_mod = None


def _textstat():
    """Devolve o módulo, ou mata o runner.

    `sys.exit`, não `return None`: um caso que declara limiar e não acha a
    dependência tem de parar a rodada. Métrica que "não roda" e conta como
    verde é exatamente o caso verde que não verifica nada.
    """
    if _ts_mod is None:
        sys.exit("erro: textstat não instalado — python3 -m venv .venv && "
                 ".venv/bin/pip install -r requirements.txt")
    return _ts_mod


BLOCKQUOTE = re.compile(r"^\s*>+\s?")
LINHA_TABELA = re.compile(r"^\s*\|")
LINHA_TITULO = re.compile(r"^\s*#{1,6}\s")
MARCADOR = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
# `_` sozinho fica: `nome_arquivo` é identificador, e a PTC-7 é justamente sobre
# identificadores. Comer o underscore fundiria duas palavras numa.
ENFASE = re.compile(r"\*\*|__|[`*]")
# `count_sentences` racha em qualquer `.` — `1.5 GB` vira duas frases. Aqui isso
# é grave: a PTC-7 troca `1.5 GB` por `1,5 GB`, então entrada e texto final
# sairiam com contagens diferentes por um motivo que não é legibilidade.
DECIMAL = re.compile(r"(?<=\d)\.(?=\d)")
FIM_DE_FRASE = ".!?:;"


def normaliza(texto):
    """Tira o markdown e devolve prosa corrida, pronta para contar.

    **Uma função só, usada nos dois lados.** A entrada do caso é texto cru; o
    texto final da skill sai como blockquote dentro de uma resposta com tabela.
    Se as duas normalizações divergirem, o antes/depois compara coisas
    diferentes e o limiar calibrado não significa nada.
    """
    linhas = []
    for linha in (texto or "").splitlines():
        linha = BLOCKQUOTE.sub("", linha)
        if LINHA_TABELA.match(linha) or LINHA_TITULO.match(linha):
            continue
        linha = DECIMAL.sub(",", MARCADOR.sub("", linha))
        linha = ENFASE.sub("", linha).strip()
        if not linha:
            continue
        # ponytail: título vira frase própria em vez de fundir com o parágrafo
        # seguinte (`Procedimento de Restauração de Backup` do caso-01). Isso
        # deflaciona palavras/frase — mas identicamente nos dois lados, então o
        # delta sobrevive. Trocar por segmentador de verdade só se algum caso
        # precisar do número absoluto em vez do delta.
        if linha[-1] not in FIM_DE_FRASE:
            linha += "."
        linhas.append(linha)
    return " ".join(linhas)


def medir(texto):
    """Devolve a `Medida` do texto, ou `None` se não houver o que medir.

    `None`, nunca `0.0` nem `100.0`: quem chama transforma isso em falha
    explícita. Um número inventado para texto vazio passaria ou reprovaria por
    acidente.
    """
    ts = _textstat()
    # Só afeta a silabação do Pyphen — as constantes de fórmula do textstat não
    # têm PT (ver docstring do módulo). `count_syllables` é cacheado por
    # `(texto, lang)`, então alternar idioma não devolve resultado velho.
    ts.set_lang("pt_BR")

    limpo = normaliza(texto)
    palavras = ts.lexicon_count(limpo)
    frases = ts.sentence_count(limpo)
    if not palavras or not frases:
        return None

    pal_frase = palavras / frases
    sil_pal = ts.syllable_count(limpo) / palavras
    # Flesch adaptado ao PT-BR, Martins et al. 1996. Sem clamp em [0, 100]: a
    # escala é nominal e transborda nas duas pontas. Medido neste repo — o
    # comunicado burocrático do caso-03 dá 35, o caso-01 cru dá 52, uma
    # reescrita PTC boa passa de 100, e um período único de palavras longas dá
    # −79. Prender o fundo em 0 apagaria justo a diferença entre ruim e péssimo,
    # que é o que se olha ao calibrar limiar.
    flesch = 248.835 - 1.015 * pal_frase - 84.6 * sil_pal
    return Medida(flesch, pal_frase, sil_pal, palavras, frases)
