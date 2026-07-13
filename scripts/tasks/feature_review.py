"""Post-feature review: lint, test, docs check, orphan scan."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TASKS = [
    ("scripts.tasks.check_orphans", []),
    ("scripts.tasks.lint_all", ["native"]),
    ("scripts.tasks.test_all", ["native"]),
    ("scripts.tasks.static_analysis", ["native"]),
    ("scripts.tasks.security_check", []),
    ("scripts.tasks.docs_check", []),
    ("scripts.tasks.check_doc_updates", []),
    ("scripts.tasks.validate_agents", []),
    ("scripts.tasks.validate_agents_commands", []),
]


def run_task(module: str, *args: str) -> bool:
    print(f"\n{'=' * 60}\n  {module}\n{'=' * 60}")
    result = subprocess.run([sys.executable, "-m", module, *args], cwd=ROOT)
    return result.returncode == 0


def main() -> None:
    failed = []
    for module, args in TASKS:
        if not run_task(module, *args):
            failed.append(module)
    print(f"\n{'=' * 60}")
    if failed:
        print(f"Feature review FAILED: {', '.join(failed)}")
        print("Fix issues, remove dead code, update docs, then re-run.")
        sys.exit(1)
    print("Feature review PASSED.")
    print("Confirm: no unused imports, no orphaned files, docs updated.")


if __name__ == "__main__":
    main()
