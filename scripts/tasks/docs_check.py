"""Verify documentation structure and internal markdown links."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT

REQUIRED = [
    "docs/technical/README.md",
    "docs/technical/bootstrap.md",
    "docs/technical/setup-local.md",
    "docs/technical/setup-production.md",
    "docs/technical/architecture.md",
    "docs/product/README.md",
    "docs/product/overview.md",
]

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_required() -> list[str]:
    missing = []
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            missing.append(rel)
    return missing


def check_links() -> list[str]:
    broken: list[str] = []
    for md in ROOT.glob("docs/**/*.md"):
        text = md.read_text(encoding="utf-8")
        for target in LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "#")):
                continue
            path_part = target.split("#")[0]
            if not path_part:
                continue
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                broken.append(f"{md.relative_to(ROOT)}: {target}")
    return broken


def main() -> None:
    errors: list[str] = []
    missing = check_required()
    if missing:
        errors.append("Missing required docs:")
        errors.extend(f"  - {m}" for m in missing)
    broken = check_links()
    if broken:
        errors.append("Broken relative links:")
        errors.extend(f"  - {b}" for b in broken)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print("Documentation structure OK.")


if __name__ == "__main__":
    main()
