"""Bootstrap a fresh Agents Starter Kit clone: scaffold apps, env, and verify."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, require_docker, run

API = ROOT / "api"
WEB = ROOT / "web"
APP = ROOT / "app"


def _command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def check_prerequisites(*, need_scaffold: bool) -> list[str]:
    missing: list[str] = []
    if not _command_exists("docker"):
        missing.append("docker")
    if not _command_exists("python3"):
        missing.append("python3")
    if need_scaffold:
        if not (API / "composer.json").exists() and not _command_exists("composer"):
            missing.append("composer (needed to scaffold Laravel)")
        if not (WEB / "package.json").exists() and not _command_exists("npx"):
            missing.append("npx/node (needed to scaffold Nuxt)")
    return missing


def _prompt_yes(message: str, default: bool = True) -> bool:
    suffix = " [Y/n] " if default else " [y/N] "
    answer = input(f"{message}{suffix}").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def scaffold_laravel(*, yes: bool) -> None:
    if (API / "composer.json").exists():
        print("Skip Laravel: api/composer.json exists.")
        return
    if not yes and not _prompt_yes("Scaffold Laravel in api/?"):
        print("Skipped Laravel scaffold.")
        return
    print("\n→ Scaffolding Laravel in api/ …")
    run(["composer", "create-project", "laravel/laravel", str(API)])
    env_template = API / ".env.example.template"
    env_target = API / ".env"
    if env_template.exists() and not env_target.exists():
        shutil.copy(env_template, env_target)
        print(f"Copied {env_template.name} → .env")
    elif (API / ".env.example").exists() and not env_target.exists():
        shutil.copy(API / ".env.example", env_target)
        _patch_api_env(env_target)
    print(
        "\nRecommended after scaffold:\n"
        "  cd api && composer require --dev larastan/larastan pestphp/pest pestphp/pest-plugin-laravel\n"
        "  composer require dedoc/scramble   # OpenAPI — see docs/technical/api-contract.md\n"
        "  cp phpstan.neon.dist phpstan.neon\n"
        "  cp tests/Architecture/ArchTest.php.template tests/Architecture/ArchTest.php"
    )


def _patch_api_env(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    replacements = {
        "DB_CONNECTION=sqlite": "DB_CONNECTION=pgsql",
        "DB_HOST=127.0.0.1": "DB_HOST=postgres",
        "# DB_HOST=127.0.0.1": "DB_HOST=postgres",
        "REDIS_HOST=127.0.0.1": "REDIS_HOST=redis",
        "MAIL_MAILER=log": "MAIL_MAILER=smtp",
        "MAIL_HOST=127.0.0.1": "MAIL_HOST=mailpit",
        "MAIL_PORT=2525": "MAIL_PORT=1025",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print("Patched api/.env for Docker service names.")


def _is_nuxt_stub() -> bool:
    pkg = WEB / "package.json"
    return pkg.exists() and "starter-kit-stub" in pkg.read_text(encoding="utf-8")


def scaffold_nuxt(*, yes: bool) -> None:
    pkg = WEB / "package.json"
    if pkg.exists() and not _is_nuxt_stub():
        print("Skip Nuxt: web/package.json exists (non-stub).")
        return
    if not yes and not _prompt_yes("Scaffold Nuxt in web/?"):
        print("Skipped Nuxt scaffold.")
        return
    if _is_nuxt_stub():
        pkg.unlink()
        shutil.rmtree(WEB / "node_modules", ignore_errors=True)
    print("\n→ Scaffolding Nuxt in web/ …")
    run(["npx", "nuxi@latest", "init", str(WEB), "--force", "--no-install"])
    run(["npm", "install"], cwd=WEB)
    env_template = WEB / ".env.example.template"
    env_target = WEB / ".env"
    if env_template.exists() and not env_target.exists():
        shutil.copy(env_template, env_target)
        print(f"Copied {env_template.name} → .env")


def scaffold_flutter(*, yes: bool) -> None:
    pubspec = APP / "pubspec.yaml"
    if pubspec.exists():
        print("Skip Flutter: app/pubspec.yaml exists.")
        return
    if not _command_exists("flutter"):
        print("Skip Flutter: flutter not installed.")
        return
    if not yes and not _prompt_yes("Scaffold Flutter in app/?"):
        print("Skipped Flutter scaffold.")
        return
    print("\n→ Scaffolding Flutter in app/ …")
    run(["flutter", "create", "--project-name", "my_app", str(APP)])


def setup_root_env(*, yes: bool) -> None:
    root_env = ROOT / ".env"
    example = ROOT / ".env.docker.example"
    if root_env.exists():
        print("Skip root .env: already exists.")
        return
    if not example.exists():
        print("Warning: .env.docker.example missing.", file=sys.stderr)
        return
    if not yes and not _prompt_yes("Copy .env.docker.example → .env?"):
        return
    shutil.copy(example, root_env)
    print("Created .env from .env.docker.example")


def print_env_alignment() -> None:
    print("\n--- Env alignment checklist ---")
    print("Root .env:      HTTP_PORT, WEB_PORT, NUXT_PUBLIC_API_BASE, DB_*")
    print("api/.env:       DB_HOST=postgres, REDIS_HOST=redis, MAIL_HOST=mailpit")
    print("web/.env:       NUXT_PUBLIC_API_BASE=http://localhost:${HTTP_PORT}/api")
    print("See api/.env.example.template and web/.env.example.template")


def docker_bootstrap(*, yes: bool) -> None:
    if not (API / "composer.json").exists():
        print("Skip Docker bootstrap: no Laravel app yet.")
        return
    if not yes and not _prompt_yes("Start Docker stack and run migrations?"):
        return
    require_docker()
    run(["docker", "compose", "up", "-d", "--build"])
    run(["docker", "compose", "exec", "-T", "api", "composer", "install"])
    run(["docker", "compose", "exec", "-T", "api", "php", "artisan", "key:generate"])
    run(["docker", "compose", "exec", "-T", "api", "php", "artisan", "migrate", "--force"])
    if (WEB / "package.json").exists():
        run(["docker", "compose", "exec", "-T", "web", "npm", "install"])


def run_feature_review(*, yes: bool) -> None:
    if not yes and not _prompt_yes("Run feature_review now?"):
        print("Run later: python3 -m scripts.tasks.feature_review")
        return
    result = subprocess.run(
        [sys.executable, "-m", "scripts.tasks.feature_review"],
        cwd=ROOT,
    )
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap Agents Starter Kit project.")
    parser.add_argument("--yes", "-y", action="store_true", help="Non-interactive; accept defaults.")
    parser.add_argument("--skip-scaffold", action="store_true", help="Skip app scaffolding.")
    parser.add_argument("--skip-docker", action="store_true", help="Skip docker compose up.")
    parser.add_argument("--flutter", action="store_true", help="Scaffold optional Flutter app.")
    parser.add_argument("--no-review", action="store_true", help="Skip feature_review at end.")
    args = parser.parse_args()

    need_scaffold = not args.skip_scaffold
    missing = check_prerequisites(need_scaffold=need_scaffold)
    if missing:
        print("Missing prerequisites:", ", ".join(missing), file=sys.stderr)
        sys.exit(1)

    print("Prerequisites OK.")
    setup_root_env(yes=args.yes)

    if need_scaffold:
        scaffold_laravel(yes=args.yes)
        scaffold_nuxt(yes=args.yes)
        if args.flutter:
            scaffold_flutter(yes=args.yes)

    print_env_alignment()

    if not args.skip_docker:
        docker_bootstrap(yes=args.yes)

    if not args.no_review:
        run_feature_review(yes=args.yes)

    print("\nBootstrap complete. See docs/technical/bootstrap.md for details.")


if __name__ == "__main__":
    main()
