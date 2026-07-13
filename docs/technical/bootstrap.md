# Bootstrap (day 0)

Complete guide from empty clone to a running Laravel + Nuxt stack with a green feature review.

For daily dev after bootstrap, see [setup-local.md](setup-local.md).

## Prerequisites

| Tool | Required | Check |
|------|----------|-------|
| Git | Yes | `git --version` |
| Docker + Compose v2 | Yes (recommended) | `docker compose version` |
| Python 3.10+ | Yes (devkit) | `python3 --version` |
| Composer | For native scaffold | `composer --version` |
| Node.js 20+ | For native scaffold | `node --version` |
| Flutter | Optional (`app/`) | `flutter --version` |

## Quick bootstrap (automated)

From project root:

```bash
python3 -m scripts.tasks.bootstrap_project
```

Or non-interactive:

```bash
python3 -m scripts.tasks.bootstrap_project --yes
python3 -m scripts.tasks.bootstrap_project --skip-scaffold   # kit only, apps exist
python3 -m scripts.tasks.bootstrap_project --flutter       # include Flutter stub
```

The script checks prerequisites, scaffolds missing apps, copies env templates, and prints next steps.

## Manual bootstrap

### 1. Clone and root env

```bash
git clone git@github.com:elbakkali/agents-starter-kit.git my-app
cd my-app
cp .env.docker.example .env
```

### 2. Scaffold Laravel (`api/`)

Skip if `api/composer.json` already exists.

```bash
composer create-project laravel/laravel api
```

Copy env template and align for Docker:

```bash
cp api/.env.example.template api/.env
# Or after Laravel scaffold: cp api/.env.example api/.env
```

Key values for Docker (see `api/.env.example.template`):

```env
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=app
DB_USERNAME=app
DB_PASSWORD=secret
REDIS_HOST=redis
REDIS_PORT=6379
MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
```

Install dev tooling (recommended after scaffold):

```bash
cd api
composer require --dev larastan/larastan pestphp/pest pestphp/pest-plugin-laravel
php artisan pest:install
cp phpstan.neon.dist phpstan.neon
cp tests/Architecture/ArchTest.php.template tests/Architecture/ArchTest.php
```

OpenAPI docs (recommended):

```bash
composer require dedoc/scramble
# Dev docs at /docs/api — see docs/technical/api-contract.md
```

### 3. Scaffold Nuxt (`web/`)

Skip if `web/package.json` exists (other than the kit stub).

```bash
npx nuxi@latest init web
cd web && npm install
```

Copy env template:

```bash
cp web/.env.example.template web/.env
```

Key value (must match root `.env` / nginx port):

```env
NUXT_PUBLIC_API_BASE=http://localhost:8080/api
```

See [tsconfig.strict-notes.md](../../web/tsconfig.strict-notes.md) for strict TypeScript setup.

E2E (optional, after Nuxt scaffold):

```bash
cd web && npm init playwright@latest
# Or copy templates from web/e2e/ — see docs/technical/e2e.md
```

### 4. Optional Flutter (`app/`)

```bash
flutter create --project-name my_app app
# Or copy app/pubspec.yaml.template and run flutter pub get
```

See [app/AGENTS.md](../../app/AGENTS.md). Dependabot pub job activates when `app/pubspec.yaml` exists.

### 5. Start Docker stack

```bash
docker compose up -d --build
docker compose exec api composer install
docker compose exec api php artisan key:generate
docker compose exec api php artisan migrate
docker compose exec web npm install
```

### 6. Verify

```bash
python3 -m scripts.tasks.feature_review
```

Expected in template mode: lint/test/static analysis skip gracefully; kit checks (docs, orphans, adapters, AGENTS.md) pass.

### 7. Optional tooling

**Pre-commit hooks** (local only):

```bash
pip install pre-commit   # or: brew install pre-commit
pre-commit install
```

**just** (command shortcuts):

```bash
# Install just: https://github.com/casey/just
just --list
```

**Session handoff** — at end of multi-file sessions, copy `docs/technical/HANDOFF.md.template` → `docs/technical/HANDOFF.md` (gitignored).

## Static analysis

| Package | Config | When active |
|---------|--------|-------------|
| API | `api/phpstan.neon.dist` | After Laravel + Larastan install |
| API | `api/tests/Architecture/` | After copying `ArchTest.php.template` |
| Web | `npm run typecheck` | After adding vue-tsc script |

Run via devkit → Development → Static analysis, or `python3 -m scripts.tasks.static_analysis`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `api/` empty after clone | Run bootstrap script or `composer create-project` |
| DB connection refused | `DB_HOST=postgres` in `api/.env`, stack running |
| Web cannot reach API | Align `NUXT_PUBLIC_API_BASE` with `HTTP_PORT` in root `.env` |
| PHPStan missing | `composer require --dev larastan/larastan` in `api/` |
| feature_review fails on docs | Update `docs/technical/` when changing app code |

## Related

- [setup-local.md](setup-local.md) — daily workflow
- [architecture.md](architecture.md) — fill in your product design
- [api-contract.md](api-contract.md) — OpenAPI / Scramble
- [e2e.md](e2e.md) — Playwright smoke tests
