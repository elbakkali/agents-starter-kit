#!/usr/bin/env bash
# Format PHP files under api/ with Pint when available (graceful skip).
set -euo pipefail

input=$(cat)
file_path=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('file_path',''))" <<<"$input" 2>/dev/null || true)

if [[ -z "$file_path" ]]; then
  exit 0
fi

if [[ "$file_path" != api/* && "$file_path" != */api/* ]]; then
  exit 0
fi

if [[ "$file_path" != *.php ]]; then
  exit 0
fi

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PINT="${ROOT}/api/vendor/bin/pint"

if [[ ! -x "$PINT" ]]; then
  exit 0
fi

"$PINT" "$ROOT/$file_path" 2>/dev/null || true
exit 0
