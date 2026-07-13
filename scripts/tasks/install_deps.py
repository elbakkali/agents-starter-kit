"""Install dependencies in api/ and web/."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, docker_compose, require_docker, run


def _native() -> None:
    api = ROOT / "api"
    web = ROOT / "web"
    if (api / "composer.json").exists():
        run(["composer", "install"], cwd=api)
    if (web / "package.json").exists():
        run(["npm", "install"], cwd=web)


def _docker() -> None:
    require_docker()
    docker_compose("exec", "-T", "api", "composer", "install")
    docker_compose("exec", "-T", "web", "npm", "install")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "docker"
    if mode == "native":
        _native()
    else:
        _docker()


if __name__ == "__main__":
    main()
