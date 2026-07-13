"""Find orphaned junk files and common leftovers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT

JUNK_GLOBS = [
    "**/*.bak",
    "**/*.tmp",
    "**/*.swp",
    "**/*~",
    "**/.DS_Store",
]

SKIP_DIRS = {
    ".git",
    "node_modules",
    "vendor",
    ".cursor",
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def find_junk() -> list[Path]:
    found: list[Path] = []
    for pattern in JUNK_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file() and not should_skip(path):
                found.append(path)
    return sorted(found)


def find_empty_dirs() -> list[Path]:
    empty: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_dir() or should_skip(path):
            continue
        try:
            if not any(path.iterdir()):
                empty.append(path)
        except PermissionError:
            continue
    return empty


def main() -> None:
    junk = find_junk()
    empty = find_empty_dirs()
    issues = False
    if junk:
        issues = True
        print("Junk files (delete these):")
        for p in junk:
            print(f"  - {p.relative_to(ROOT)}")
    if empty:
        issues = True
        print("Empty directories (remove if orphaned):")
        for p in empty:
            print(f"  - {p.relative_to(ROOT)}")
    if not issues:
        print("No junk files or empty directories found.")
        return
    print("\nReview docs/technical/tech-debt.md for intentional deprecations.")
    sys.exit(1)


if __name__ == "__main__":
    main()
