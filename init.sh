#!/usr/bin/env bash
# Verificação da skill PTC. Roda os casos de tests/casos/ contra o SKILL.md
# deste repo. Ver AGENTS.md para o fluxo de desenvolvimento.
#
#   ./init.sh                    todos os casos
#   ./init.sh caso-01            um caso (match por substring)
#   ./init.sh --cobertura        matriz de cobertura (não chama a API)
#   ./init.sh --metricas         legibilidade antes/depois, sem gatear (1 chamada/caso)
#   PTC_MODELO=opus ./init.sh    outro modelo (default: sonnet)
#   PTC_TENTATIVAS=1 ./init.sh   sem retry (para medir instabilidade)
#   PTC_MODELO_ESCALA=           não repete em opus quando o caso falha
#   PTC_ADVERSARIAL=1 ./init.sh --cobertura   só conta contra-teste caso-adv-*
set -euo pipefail
cd "$(dirname "$0")"

# O python3 do sistema costuma ser externally-managed (PEP 668), e aí um
# `pip install` global falha. Preferir o venv quando ele existe evita o modo de
# falha chato: instalar no venv e o runner continuar dizendo que falta, porque o
# pip do venv e o python3 do PATH são interpretadores diferentes.
# Precisa ser `if`, não `[ -x … ] && PY=…`: sob `set -e`, o `&&` falso mata o script.
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else PY=python3; fi

falta=0
command -v claude >/dev/null || { echo "falta: claude (https://claude.com/claude-code)"; falta=1; }
command -v "$PY"  >/dev/null || { echo "falta: python3"; falta=1; }
# Checado sempre, não só na rodada completa: é fronteira de custo. Descobrir a
# dependência ausente depois de gastar 14 chamadas de API é o desperdício que
# estes ~200 ms compram. Redundante com o sys.exit de tests/legibilidade.py de
# propósito — aquele protege quem roda o verify.py direto, este protege a conta.
"$PY" -c 'import textstat' 2>/dev/null || {
  echo "falta: textstat — python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  falta=1; }
[ "$falta" -eq 0 ] || exit 1

# Só na rodada completa. Durante o desenvolvimento de um caso, dist/ ainda não
# precisa estar em dia — regenerar a cada iteração só suja o diff. Na rodada
# que serve de gate, um bundle defasado é uma skill publicada diferente da
# testada, e isso ninguém percebe olhando o verde dos casos.
if [ $# -eq 0 ]; then
  "$PY" tools/build.py --verificar || exit 1
  "$PY" tests/test_runner.py       || exit 1
fi

exec "$PY" tests/verify.py "$@"
