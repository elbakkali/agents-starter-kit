"""Run static analysis (PHPStan, vue-tsc, architecture tests) when tools exist."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, docker_compose, require_docker, run


def _has_api() -> bool:
    return (ROOT / "api" / "composer.json").exists()


def _has_web() -> bool:
    return (ROOT / "web" / "package.json").exists()


def _run_phpstan_native() -> bool:
    api = ROOT / "api"
    phpstan = api / "vendor" / "bin" / "phpstan"
    config = api / "phpstan.neon"
    dist = api / "phpstan.neon.dist"
    if not phpstan.exists():
        print("Skip PHPStan: run composer install and require phpstan/larastan in api/")
        return True
    cfg = config if config.exists() else dist
    if not cfg.exists():
        print("Skip PHPStan: no phpstan.neon or phpstan.neon.dist in api/")
        return True
    run([str(phpstan), "analyse", f"--configuration={cfg}"], cwd=api)
    return True


def _run_vue_tsc_native() -> bool:
    web = ROOT / "web"
    if not (web / "package.json").exists():
        print("Skip vue-tsc: no package.json in web/")
        return True
    pkg = (web / "package.json").read_text(encoding="utf-8")
    if '"vue-tsc"' not in pkg and '"typecheck"' not in pkg:
        print("Skip vue-tsc: add vue-tsc or npm run typecheck script in web/")
        return True
    if '"typecheck"' in pkg:
        run(["npm", "run", "typecheck"], cwd=web)
    else:
        run(["npx", "vue-tsc", "--noEmit"], cwd=web)
    return True


def _run_architecture_tests_native() -> bool:
    api = ROOT / "api"
    arch = api / "tests" / "Architecture"
    if not arch.exists():
        print("Skip architecture tests: no api/tests/Architecture/")
        return True
    if not (api / "artisan").exists():
        print("Skip architecture tests: no Laravel app in api/")
        return True
    run(["php", "artisan", "test", "--filter=Architecture"], cwd=api)
    return True


def _native() -> int:
    failed = False
    if _has_api():
        for fn in (_run_phpstan_native, _run_architecture_tests_native):
            try:
                fn()
            except subprocess.CalledProcessError:
                failed = True
    else:
        print("Skip API static analysis: no composer.json in api/")
    if _has_web():
        try:
            _run_vue_tsc_native()
        except subprocess.CalledProcessError:
            failed = True
    else:
        print("Skip web static analysis: no package.json in web/")
    return 1 if failed else 0


def _docker() -> int:
    require_docker()
    if _has_api():
        docker_compose(
            "exec",
            "-T",
            "api",
            "./vendor/bin/phpstan",
            "analyse",
            "--configuration=phpstan.neon.dist",
        )
    else:
        print("Skip API static analysis: no composer.json in api/")
    if _has_web():
        docker_compose("exec", "-T", "web", "npm", "run", "typecheck")
    else:
        print("Skip web static analysis: no package.json in web/")
    return 0


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "native"
    code = _docker() if mode == "docker" else _native()
    sys.exit(code)


if __name__ == "__main__":
    main()
