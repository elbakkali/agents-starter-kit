"""Validate AGENTS.md command strings against package scripts and artisan."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, web_is_kit_stub

NPM_RUN = re.compile(r"npm run (\S+)")
ARTISAN = re.compile(r"php artisan (\S+)")


def _bash_lines(agents_path: Path) -> list[str]:
    if not agents_path.exists():
        return []
    lines: list[str] = []
    in_block = False
    for line in agents_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                lines.append(stripped)
    return lines


def _load_npm_scripts(package_json: Path) -> set[str]:
    data = json.loads(package_json.read_text(encoding="utf-8"))
    return set(data.get("scripts", {}).keys())


def _artisan_commands(api_dir: Path) -> set[str]:
    result = subprocess.run(
        ["php", "artisan", "list", "--raw"],
        cwd=api_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()
    names: set[str] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        names.add(line.split(":")[0].strip())
        names.add(line.strip())
    return names


def validate_web() -> list[str]:
    errors: list[str] = []
    pkg = ROOT / "web" / "package.json"
    if not pkg.exists():
        print("Skip web commands: no package.json (template mode).")
        return errors
    if web_is_kit_stub():
        print("Skip web commands: package.json is kit stub (run nuxi init).")
        return errors
    scripts = _load_npm_scripts(pkg)
    for line in _bash_lines(ROOT / "web" / "AGENTS.md"):
        for match in NPM_RUN.finditer(line):
            script = match.group(1)
            if script not in scripts:
                errors.append(
                    f"web/AGENTS.md references `npm run {script}` but script missing in package.json"
                )
    return errors


def validate_api() -> list[str]:
    errors: list[str] = []
    api = ROOT / "api"
    if not (api / "composer.json").exists():
        print("Skip API commands: no composer.json (template mode).")
        return errors
    if not (api / "artisan").exists():
        print("Skip API artisan commands: no artisan binary.")
        return errors
    available = _artisan_commands(api)
    if not available:
        print("Skip artisan validation: artisan list unavailable.")
        return errors
    for line in _bash_lines(api / "AGENTS.md"):
        for match in ARTISAN.finditer(line):
            target = match.group(1)
            base = target.split()[0]
            if base not in available and target not in available:
                errors.append(
                    f"api/AGENTS.md references `php artisan {target}` but command not in artisan list"
                )
    return errors


def main() -> None:
    errors = validate_api() + validate_web()
    if errors:
        print("AGENTS.md command validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print("AGENTS.md commands OK (or skipped in template mode).")


if __name__ == "__main__":
    main()
