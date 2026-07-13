"""Stop the Docker development stack."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import docker_compose


def main() -> None:
    docker_compose("down")


if __name__ == "__main__":
    main()
