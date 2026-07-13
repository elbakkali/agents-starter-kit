"""Dependency audit and minimal anti-pattern scan for shipped code security."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, run

API = ROOT / "api"
WEB = ROOT / "web"

SKIP_DIRS = {"vendor", "node_modules", ".git", "storage", "bootstrap/cache"}
SCAN_EXTENSIONS = {".php", ".ts", ".vue", ".js", ".jsx", ".tsx"}

# Minimal patterns — low false positives; expand only with care.
ANTIPATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\beval\s*\("), "eval() call"),
    (re.compile(r'password\s*=\s*["\'][^"\']{3,}["\']', re.I), "hardcoded password assignment"),
    (re.compile(r"DB::raw\s*\(\s*\$request"), "DB::raw with request input"),
]


def _has_composer() -> bool:
    return (API / "composer.json").exists()


def _has_npm() -> bool:
    return (WEB / "package.json").exists()


def composer_audit() -> bool:
    if not _has_composer():
        print("Skip composer audit: no composer.json in api/")
        return True
    try:
        run(["composer", "audit", "--no-interaction"], cwd=API)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"composer audit failed: {exc}", file=sys.stderr)
        return False


def npm_audit() -> bool:
    if not _has_npm():
        print("Skip npm audit: no package.json in web/")
        return True
    if not (WEB / "node_modules").exists():
        print("Skip npm audit: no node_modules in web/ (run npm install first)")
        return True
    try:
        run(["npm", "audit", "--audit-level=high"], cwd=WEB)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"npm audit failed: {exc}", file=sys.stderr)
        return False


def _should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_EXTENSIONS:
        return False
    return not any(part in SKIP_DIRS for part in path.parts)


def scan_antipatterns() -> bool:
    findings: list[str] = []
    for pkg in ("api", "web", "app"):
        base = ROOT / pkg
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or not _should_scan(path):
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pattern, desc in ANTIPATTERNS:
                if pattern.search(content):
                    findings.append(f"{path.relative_to(ROOT)}: {desc}")
    if findings:
        print("Anti-pattern scan findings:", file=sys.stderr)
        for item in findings:
            print(f"  - {item}", file=sys.stderr)
        return False
    print("Anti-pattern scan: no obvious issues.")
    return True


def main() -> None:
    failed: list[str] = []
    if not composer_audit():
        failed.append("composer audit")
    if not npm_audit():
        failed.append("npm audit")
    if not scan_antipatterns():
        failed.append("anti-pattern scan")

    if failed:
        print(f"\nSecurity check FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)
    print("\nSecurity check PASSED.")


if __name__ == "__main__":
    main()
