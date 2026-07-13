"""Run backend and frontend test suites."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, docker_compose, require_docker, run, web_is_kit_stub


def _native() -> None:
    api = ROOT / "api"
    web = ROOT / "web"
    if (api / "artisan").exists():
        run(["php", "artisan", "test"], cwd=api)
    else:
        print("Skip API tests: no Laravel app in api/")
    if web_is_kit_stub():
        print("Skip web tests: package.json is kit stub (run nuxi init).")
    elif (web / "package.json").exists():
        run(["npm", "run", "test"], cwd=web)
    else:
        print("Skip web tests: no package.json in web/")


def _docker() -> None:
    require_docker()
    if (ROOT / "api" / "artisan").exists():
        docker_compose("exec", "-T", "api", "php", "artisan", "test")
    elif (ROOT / "api" / "composer.json").exists():
        print("Skip API tests: artisan not found — scaffold Laravel in api/")
    else:
        print("Skip API tests: no Laravel app in api/")
    if web_is_kit_stub():
        print("Skip web tests: package.json is kit stub (run nuxi init).")
    elif (ROOT / "web" / "package.json").exists():
        docker_compose("exec", "-T", "web", "npm", "run", "test")
    else:
        print("Skip web tests: no package.json in web/")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "docker"
    if mode == "native":
        _native()
    else:
        _docker()


if __name__ == "__main__":
    main()
