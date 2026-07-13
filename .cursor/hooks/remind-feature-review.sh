#!/usr/bin/env bash
# Remind to run feature_review and update HANDOFF when code files changed this session.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  exit 0
fi

changed=$(git diff --name-only HEAD 2>/dev/null || true)
untracked=$(git ls-files --others --exclude-standard 2>/dev/null || true)
all_changes=$(printf '%s\n%s' "$changed" "$untracked" | grep -E '^(api|web|app|scripts)/' || true)

if [[ -z "$all_changes" ]]; then
  exit 0
fi

file_count=$(echo "$all_changes" | grep -c . || true)
handoff_note=""
if [[ "$file_count" -ge 2 ]]; then
  handoff_note=" Update docs/technical/HANDOFF.md from HANDOFF.md.template for session handoff."
fi

export HANDOFF_NOTE="$handoff_note"
python3 - <<'PY'
import json
import os

handoff = os.environ.get("HANDOFF_NOTE", "")
print(json.dumps({
    "followup_message": (
        "Code under api/, web/, app/, or scripts/ changed. Before finishing: "
        "review/refactor, remove orphans, update docs, then run "
        "python3 -m scripts.tasks.feature_review." + handoff
    )
}))
PY
exit 0
