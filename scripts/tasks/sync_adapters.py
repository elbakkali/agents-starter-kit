"""Sync cross-editor adapter files from .cursor/rules/*.mdc (source of truth)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURSOR_RULES = ROOT / ".cursor/rules"
CLAUDE_RULES = ROOT / ".claude" / "rules"
COPILOT_INSTRUCTIONS = ROOT / ".github" / "instructions"

GENERATED_BANNER = (
    "<!-- AUTO-GENERATED from .cursor/rules/{source} — "
    "edit the .mdc source and run: python3 -m scripts.tasks.sync_adapters -->\n\n"
)


def parse_mdc(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, frontmatter, body = text.split("---", 2)
    meta: dict[str, str] = {}
    for line in frontmatter.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body.lstrip("\n")


def parse_globs(globs_raw: str) -> list[str]:
    if not globs_raw:
        return []
    patterns: list[str] = []
    for segment in globs_raw.split(","):
        segment = segment.strip()
        patterns.extend(expand_globs(segment))
    return patterns


def expand_globs(pattern: str) -> list[str]:
    match = re.search(r"\{([^}]+)\}", pattern)
    if not match:
        return [pattern]
    prefix = pattern[: match.start()]
    suffix = pattern[match.end() :]
    return [f"{prefix}{part.strip()}{suffix}" for part in match.group(1).split(",")]


def claude_frontmatter(meta: dict[str, str], globs: list[str]) -> str:
    always = meta.get("alwaysApply", "false").lower() == "true"
    if always or not globs:
        return ""  # Global rule — no paths frontmatter
    paths = ", ".join(globs)
    return f"---\npaths: {paths}\n---\n\n"


def copilot_frontmatter(meta: dict[str, str], globs: list[str]) -> str:
    description = meta.get("description", "")
    always = meta.get("alwaysApply", "false").lower() == "true"
    if always or not globs:
        apply_to = '"**"'
    else:
        apply_to = f'"{",".join(globs)}"'
    lines = ["---"]
    if description:
        lines.append(f'description: "{description}"')
    lines.append(f"applyTo: {apply_to}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def write_adapters_for_rule(mdc_path: Path) -> None:
    meta, body = parse_mdc(mdc_path)
    name = mdc_path.stem
    globs_raw = meta.get("globs", "")
    globs = parse_globs(globs_raw)

    banner = GENERATED_BANNER.format(source=mdc_path.name)

    claude_path = CLAUDE_RULES / f"{name}.md"
    claude_path.parent.mkdir(parents=True, exist_ok=True)
    claude_path.write_text(
        banner + claude_frontmatter(meta, globs) + body,
        encoding="utf-8",
    )

    copilot_path = COPILOT_INSTRUCTIONS / f"{name}.instructions.md"
    copilot_path.parent.mkdir(parents=True, exist_ok=True)
    copilot_path.write_text(
        banner + copilot_frontmatter(meta, globs) + body,
        encoding="utf-8",
    )


def write_copilot_index() -> None:
    path = ROOT / ".github" / "copilot-instructions.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """# GitHub Copilot instructions

**Primary source:** [AGENTS.md](../AGENTS.md) — read this first for commands, boundaries, and doc rules.

**Scoped rules:** `.github/instructions/*.instructions.md` (auto-synced from `.cursor/rules/*.mdc`).

After editing Cursor rules, regenerate adapters:

```bash
python3 -m scripts.tasks.sync_adapters
```

Do not duplicate long content in this file — keep it as an index.
""",
        encoding="utf-8",
    )


def write_aider_config() -> None:
    path = ROOT / ".aider.conf.yml"
    path.write_text(
        """# Aider — read cross-tool agent instructions
read:
  - AGENTS.md
""",
        encoding="utf-8",
    )


def write_gemini_config() -> None:
    path = ROOT / ".gemini" / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """{
  "context": {
    "fileName": "AGENTS.md"
  }
}
""",
        encoding="utf-8",
    )


def write_windsurf_pointer() -> None:
    path = ROOT / ".windsurfrules"
    path.write_text(
        """# Windsurf — pointer to cross-tool instructions
# Primary: AGENTS.md (also read by Windsurf natively)
# Scoped rules: .github/instructions/ or .claude/rules/ (synced from .cursor/rules/)
""",
        encoding="utf-8",
    )


def write_instructions_readme() -> None:
    path = COPILOT_INSTRUCTIONS / "README.md"
    path.write_text(
        """# Copilot / VS Code instruction files

Auto-generated from [`.cursor/rules/`](../../.cursor/rules/) by:

```bash
python3 -m scripts.tasks.sync_adapters
```

| Editor | Reads |
|--------|-------|
| GitHub Copilot | `.github/copilot-instructions.md` + this folder |
| VS Code Copilot Chat | Same as Copilot |
| Claude Code | [`.claude/rules/`](../.claude/rules/) (synced in parallel) |
| Cursor | [`.cursor/rules/*.mdc`](../../.cursor/rules/) — **source of truth** |

Edit `.mdc` files in Cursor, then re-run sync. Do not hand-edit generated files.
""",
        encoding="utf-8",
    )


def write_claude_readme() -> None:
    path = ROOT / ".claude" / "rules" / "README.md"
    path.write_text(
        """# Claude Code rules

Auto-generated from [`.cursor/rules/`](../../.cursor/rules/):

```bash
python3 -m scripts.tasks.sync_adapters
```

Global project instructions: [`CLAUDE.md`](../../CLAUDE.md) → [`AGENTS.md`](../../AGENTS.md).

Edit `.cursor/rules/*.mdc`, then re-run sync.
""",
        encoding="utf-8",
    )


def expected_adapter_content(mdc_path: Path) -> tuple[Path, str, Path, str]:
    """Return (claude_path, claude_text, copilot_path, copilot_text) for one rule."""
    meta, body = parse_mdc(mdc_path)
    name = mdc_path.stem
    globs_raw = meta.get("globs", "")
    globs = parse_globs(globs_raw)
    banner = GENERATED_BANNER.format(source=mdc_path.name)
    claude_text = banner + claude_frontmatter(meta, globs) + body
    copilot_text = banner + copilot_frontmatter(meta, globs) + body
    return (
        CLAUDE_RULES / f"{name}.md",
        claude_text,
        COPILOT_INSTRUCTIONS / f"{name}.instructions.md",
        copilot_text,
    )


def expected_index_files() -> list[tuple[Path, str]]:
    """Paths and expected content for non-rule adapter files."""
    return [
        (
            ROOT / ".github" / "copilot-instructions.md",
            """# GitHub Copilot instructions

**Primary source:** [AGENTS.md](../AGENTS.md) — read this first for commands, boundaries, and doc rules.

**Scoped rules:** `.github/instructions/*.instructions.md` (auto-synced from `.cursor/rules/*.mdc`).

After editing Cursor rules, regenerate adapters:

```bash
python3 -m scripts.tasks.sync_adapters
```

Do not duplicate long content in this file — keep it as an index.
""",
        ),
        (
            ROOT / ".aider.conf.yml",
            """# Aider — read cross-tool agent instructions
read:
  - AGENTS.md
""",
        ),
        (
            ROOT / ".gemini" / "settings.json",
            """{
  "context": {
    "fileName": "AGENTS.md"
  }
}
""",
        ),
        (
            ROOT / ".windsurfrules",
            """# Windsurf — pointer to cross-tool instructions
# Primary: AGENTS.md (also read by Windsurf natively)
# Scoped rules: .github/instructions/ or .claude/rules/ (synced from .cursor/rules/)
""",
        ),
        (
            COPILOT_INSTRUCTIONS / "README.md",
            """# Copilot / VS Code instruction files

Auto-generated from [`.cursor/rules/`](../../.cursor/rules/) by:

```bash
python3 -m scripts.tasks.sync_adapters
```

| Editor | Reads |
|--------|-------|
| GitHub Copilot | `.github/copilot-instructions.md` + this folder |
| VS Code Copilot Chat | Same as Copilot |
| Claude Code | [`.claude/rules/`](../.claude/rules/) (synced in parallel) |
| Cursor | [`.cursor/rules/*.mdc`](../../.cursor/rules/) — **source of truth** |

Edit `.mdc` files in Cursor, then re-run sync. Do not hand-edit generated files.
""",
        ),
        (
            ROOT / ".claude" / "rules" / "README.md",
            """# Claude Code rules

Auto-generated from [`.cursor/rules/`](../../.cursor/rules/):

```bash
python3 -m scripts.tasks.sync_adapters
```

Global project instructions: [`CLAUDE.md`](../../CLAUDE.md) → [`AGENTS.md`](../../AGENTS.md).

Edit `.cursor/rules/*.mdc`, then re-run sync.
""",
        ),
    ]


def check_drift() -> int:
    if not CURSOR_RULES.exists():
        print(f"Missing {CURSOR_RULES}", file=sys.stderr)
        return 1

    mdc_files = sorted(CURSOR_RULES.glob("*.mdc"))
    if not mdc_files:
        print("No .mdc rule files found.", file=sys.stderr)
        return 1

    drift: list[str] = []
    for mdc in mdc_files:
        claude_path, claude_text, copilot_path, copilot_text = expected_adapter_content(mdc)
        for path, expected in ((claude_path, claude_text), (copilot_path, copilot_text)):
            if not path.exists():
                drift.append(f"missing: {path.relative_to(ROOT)}")
            elif path.read_text(encoding="utf-8") != expected:
                drift.append(f"drift: {path.relative_to(ROOT)} (run sync_adapters)")

    for path, expected in expected_index_files():
        if not path.exists():
            drift.append(f"missing: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            drift.append(f"drift: {path.relative_to(ROOT)} (run sync_adapters)")

    if drift:
        print("Adapter files out of sync with .cursor/rules/*.mdc:", file=sys.stderr)
        for item in drift:
            print(f"  - {item}", file=sys.stderr)
        print("\nFix: python3 -m scripts.tasks.sync_adapters", file=sys.stderr)
        return 1

    print("Adapter sync check OK (no drift).")
    return 0


def sync_all() -> int:
    if not CURSOR_RULES.exists():
        print(f"Missing {CURSOR_RULES}", file=sys.stderr)
        return 1

    mdc_files = sorted(CURSOR_RULES.glob("*.mdc"))
    if not mdc_files:
        print("No .mdc rule files found.", file=sys.stderr)
        return 1

    for mdc in mdc_files:
        write_adapters_for_rule(mdc)
        print(f"  synced: {mdc.name}")

    write_copilot_index()
    write_aider_config()
    write_gemini_config()
    write_windsurf_pointer()
    write_instructions_readme()
    write_claude_readme()
    print("Adapter sync complete.")
    return 0


def main() -> None:
    check_mode = "--check" in sys.argv
    sys.exit(check_drift() if check_mode else sync_all())


if __name__ == "__main__":
    main()
