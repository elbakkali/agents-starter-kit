"""Validate AGENTS.md structure and token budget."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "AGENTS.md"
MAX_LINES = 120

REQUIRED_SECTIONS = [
    "Repository map",
    "Feature completion",
    "Documentation",
    "Boundaries",
    "Detailed rules",
]


def main() -> None:
    if not AGENTS.exists():
        print(f"Missing {AGENTS}", file=sys.stderr)
        sys.exit(1)

    text = AGENTS.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    if len(lines) > MAX_LINES:
        errors.append(f"AGENTS.md exceeds {MAX_LINES} lines ({len(lines)}). Move detail to docs/.")

    for section in REQUIRED_SECTIONS:
        pattern = re.compile(rf"^##\s+{re.escape(section)}", re.MULTILINE)
        if not pattern.search(text):
            errors.append(f"Missing required section: ## {section}")

    if errors:
        print("AGENTS.md validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"AGENTS.md OK ({len(lines)} lines, all required sections present).")


if __name__ == "__main__":
    main()
