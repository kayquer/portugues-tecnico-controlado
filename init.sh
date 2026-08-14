#!/usr/bin/env bash
# Verificação da skill PTC. Roda os casos de tests/casos/ contra o SKILL.md
# deste repo. Ver AGENTS.md para o fluxo de desenvolvimento.
#
#   ./init.sh                    todos os casos
#   ./init.sh caso-01            um caso (match por substring)
#   ./init.sh --cobertura        matriz de cobertura (não chama a API)
#   PTC_MODELO=opus ./init.sh    outro modelo (default: sonnet)
#   PTC_TENTATIVAS=1 ./init.sh   sem retry (para medir instabilidade)
#   PTC_MODELO_ESCALA=           não repete em opus quando o caso falha
#   PTC_ADVERSARIAL=1 ./init.sh --cobertura   só conta contra-teste caso-adv-*
set -euo pipefail
cd "$(dirname "$0")"

falta=0
command -v claude  >/dev/null || { echo "falta: claude (https://claude.com/claude-code)"; falta=1; }
command -v python3 >/dev/null || { echo "falta: python3"; falta=1; }
[ "$falta" -eq 0 ] || exit 1

# Só na rodada completa. Durante o desenvolvimento de um caso, dist/ ainda não
# precisa estar em dia — regenerar a cada iteração só suja o diff. Na rodada
# que serve de gate, um bundle defasado é uma skill publicada diferente da
# testada, e isso ninguém percebe olhando o verde dos casos.
if [ $# -eq 0 ]; then
  python3 tools/build.py --verificar || exit 1
  python3 tests/test_runner.py     || exit 1
fi

exec python3 tests/verify.py "$@"
