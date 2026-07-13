"""Open a shell in the web container."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import docker_compose, require_docker


def main() -> None:
    require_docker()
    docker_compose("exec", "web", "sh")


if __name__ == "__main__":
    main()
