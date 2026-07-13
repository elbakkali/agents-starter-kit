"""Shared helpers for devkit task scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a command from project root (or given cwd) and stream output."""
    workdir = cwd or ROOT
    print(f"\n→ {' '.join(cmd)}  (cwd: {workdir})\n", flush=True)
    return subprocess.run(cmd, cwd=workdir, check=check)


def docker_compose(*args: str, prod: bool = False) -> None:
    cmd = ["docker", "compose"]
    if prod:
        cmd.extend(["-f", "docker-compose.yml", "-f", "docker-compose.prod.yml"])
    cmd.extend(args)
    run(cmd)


def require_docker() -> None:
    try:
        run(["docker", "info"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker is not running or not installed.", file=sys.stderr)
        sys.exit(1)


def web_is_kit_stub() -> bool:
    """True when web/package.json is the pre-scaffold starter kit stub."""
    pkg = ROOT / "web" / "package.json"
    if not pkg.exists():
        return False
    return "starter-kit-stub" in pkg.read_text(encoding="utf-8")
