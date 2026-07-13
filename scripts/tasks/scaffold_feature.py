"""Create a feature spec stub from the template."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "docs" / "templates" / "feature-spec.template.md"
SPECS_DIR = ROOT / "docs" / "product" / "specs"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower())
    return slug.strip("-") or "feature"


def main() -> None:
    if not TEMPLATE.exists():
        print(f"Missing template: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    name = " ".join(sys.argv[1:]).strip()
    if not name:
        name = input("Feature name: ").strip()
    if not name:
        print("Feature name required.", file=sys.stderr)
        sys.exit(1)

    slug = slugify(name)
    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    dest = SPECS_DIR / f"{slug}.md"

    if dest.exists():
        print(f"Spec already exists: {dest}", file=sys.stderr)
        sys.exit(1)

    content = TEMPLATE.read_text(encoding="utf-8")
    content = content.replace("{{FEATURE_NAME}}", name)
    content = content.replace("{{DATE}}", date.today().isoformat())
    content = content.replace("{{SLUG}}", slug)
    dest.write_text(content, encoding="utf-8")
    print(f"Created spec: {dest}")
    print("Next: review with stakeholder, get approval, then implement.")


if __name__ == "__main__":
    main()
