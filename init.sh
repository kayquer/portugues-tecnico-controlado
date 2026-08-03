#!/usr/bin/env bash
# Verificação da skill PTC. Roda os casos de tests/casos/ contra o SKILL.md
# deste repo. Ver AGENTS.md para o fluxo de desenvolvimento.
#
#   ./init.sh                    todos os casos
#   ./init.sh caso-01            um caso (match por substring)
#   PTC_MODELO=opus ./init.sh    outro modelo (default: sonnet)
set -euo pipefail
cd "$(dirname "$0")"

falta=0
command -v claude  >/dev/null || { echo "falta: claude (https://claude.com/claude-code)"; falta=1; }
command -v python3 >/dev/null || { echo "falta: python3"; falta=1; }
[ "$falta" -eq 0 ] || exit 1

exec python3 tests/verify.py "$@"
