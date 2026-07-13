"""Run backend and frontend linters."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, docker_compose, require_docker, run, web_is_kit_stub


def _native() -> None:
    api = ROOT / "api"
    web = ROOT / "web"
    if (api / "vendor" / "bin" / "pint").exists():
        run(["./vendor/bin/pint"], cwd=api)
    elif (api / "composer.json").exists():
        print("Skip API lint: run composer install first")
    if (web / "package.json").exists():
        if web_is_kit_stub():
            print("Skip web lint: package.json is kit stub (run nuxi init).")
        else:
            run(["npm", "run", "lint"], cwd=web)
    else:
        print("Skip web lint: no package.json in web/")


def _docker() -> None:
    require_docker()
    if (ROOT / "api" / "composer.json").exists():
        docker_compose("exec", "-T", "api", "./vendor/bin/pint")
    else:
        print("Skip API lint: no composer.json in api/")
    if (ROOT / "web" / "package.json").exists():
        if web_is_kit_stub():
            print("Skip web lint: package.json is kit stub (run nuxi init).")
        else:
            docker_compose("exec", "-T", "web", "npm", "run", "lint")
    else:
        print("Skip web lint: no package.json in web/")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "docker"
    if mode == "native":
        _native()
    else:
        _docker()


if __name__ == "__main__":
    main()
