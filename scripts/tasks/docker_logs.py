"""Tail Docker compose logs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import docker_compose


def main() -> None:
    service = sys.argv[1] if len(sys.argv) > 1 else ""
    args = ["logs", "-f", "--tail=100"]
    if service:
        args.append(service)
    docker_compose(*args)


if __name__ == "__main__":
    main()
