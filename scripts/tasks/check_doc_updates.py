"""Require docs/ updates when application code under api/, web/, or app/ changes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT

APP_PREFIXES = ("api/", "web/", "app/")
CODE_EXTENSIONS = {".php", ".vue", ".ts", ".tsx", ".js", ".jsx", ".dart"}
CODE_PATH_MARKERS = ("/routes/", "/database/migrations/")
AGENTS_PATHS = {"api/AGENTS.md", "web/AGENTS.md", "app/AGENTS.md"}
DOC_HINTS = {
    "setup": "docs/technical/setup-local.md or setup-production.md",
    "architecture": "docs/technical/architecture.md or api-contract.md",
    "product": "docs/product/features.md or user-flows.md",
}


def _run_git(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def get_changed_files() -> set[str]:
    """Collect changed paths from branch diff, recent commit, and working tree."""
    files: set[str] = set()
    for args in (
        ["diff", "--name-only", "origin/main...HEAD"],
        ["diff", "--name-only", "origin/master...HEAD"],
        ["diff", "--name-only", "HEAD~1", "HEAD"],
        ["diff", "--name-only", "HEAD"],
        ["diff", "--name-only", "--cached"],
    ):
        files.update(_run_git(args))
    files.update(_run_git(["ls-files", "--others", "--exclude-standard"]))
    return {f.replace("\\", "/") for f in files}


def is_agents_only(path: str) -> bool:
    return path in AGENTS_PATHS or path.endswith("/AGENTS.md")


def is_app_code_change(path: str) -> bool:
    if not path.startswith(APP_PREFIXES) or is_agents_only(path):
        return False
    posix = PurePosixPath(path)
    if posix.suffix.lower() in CODE_EXTENSIONS:
        return True
    return any(marker in f"/{path}/" for marker in CODE_PATH_MARKERS)


def is_doc_change(path: str) -> bool:
    return path.startswith("docs/") and path.endswith(".md")


def suggest_docs(code_changes: list[str]) -> list[str]:
    hints: list[str] = []
    joined = " ".join(code_changes)
    if any(token in joined for token in ("docker", "Dockerfile", ".env", "compose")):
        hints.append(DOC_HINTS["setup"])
    if any(
        token in joined
        for token in ("routes/", "Controller", "migration", "api/", "openapi", "sanctum")
    ):
        hints.append(DOC_HINTS["architecture"])
    if any(
        token in joined
        for token in ("pages/", "components/", "composables/", "web/", "app/", ".vue", ".dart")
    ):
        hints.append(DOC_HINTS["product"])
    if not hints:
        hints.extend(DOC_HINTS.values())
    seen: set[str] = set()
    ordered: list[str] = []
    for hint in hints:
        if hint not in seen:
            seen.add(hint)
            ordered.append(hint)
    return ordered


def main() -> None:
    changed = sorted(get_changed_files())
    if not changed:
        print("Doc update check skipped: no changed files detected.")
        return

    code_changes = [path for path in changed if is_app_code_change(path)]
    doc_changes = [path for path in changed if is_doc_change(path)]

    if not code_changes:
        print("Doc update check skipped: no application code changes in api/, web/, or app/.")
        return

    if doc_changes:
        print("Doc update check OK:")
        for path in doc_changes:
            print(f"  - {path}")
        return

    print("Doc update check FAILED.", file=sys.stderr)
    print(
        "Application code changed without a matching docs/ update in the same change.",
        file=sys.stderr,
    )
    print("\nChanged application files:", file=sys.stderr)
    for path in code_changes:
        print(f"  - {path}", file=sys.stderr)
    print("\nUpdate at least one relevant doc:", file=sys.stderr)
    for hint in suggest_docs(code_changes):
        print(f"  - {hint}", file=sys.stderr)
    print(
        "\nMap: infra/setup → setup-*.md; architecture/API → architecture.md or api-contract.md; "
        "user-facing → features.md or user-flows.md",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
