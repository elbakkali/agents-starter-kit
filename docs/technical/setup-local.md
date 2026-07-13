# Local setup (from scratch)

Complete guide to run this project on your machine. Update this file when Docker, env vars, or bootstrap steps change.

## Prerequisites

- Docker Desktop or Docker Engine + Compose v2
- Python 3.10+ (for `scripts/devkit.py`)
- Git

Optional (native dev without Docker):

- PHP 8.2+, Composer
- Node.js 20+, npm
- PostgreSQL 16+

## 1. Clone and configure

```bash
git clone <repo-url> my-app && cd my-app
cp .env.docker.example .env
# Edit .env if you need custom ports or credentials
```

## 2. Scaffold applications (first time only)

If `api/` and `web/` are empty stubs, create the Laravel and Nuxt apps first:

```bash
# Laravel in api/
composer create-project laravel/laravel api

# Nuxt in web/
npx nuxi@latest init web
```

Then align `.env` files inside each package with Docker service names (`DB_HOST=postgres`, etc.).

## 3. Start with Docker (recommended)

```bash
docker compose up -d --build
docker compose exec api composer install
docker compose exec api php artisan key:generate
docker compose exec api php artisan migrate
docker compose exec web npm install
```

Or use the interactive toolkit:

```bash
python3 scripts/devkit.py
# Docker → Start stack
```

## 4. Access services

| Service | URL |
|---------|-----|
| App (via nginx) | http://localhost:8080 |
| Nuxt dev (direct) | http://localhost:3000 |
| Mailpit UI | http://localhost:8025 |
| PostgreSQL | localhost:5432 |

## 5. Daily commands

```bash
docker compose up -d          # start
docker compose down           # stop
docker compose logs -f api    # tail API logs
docker compose exec api php artisan test
docker compose exec web npm run test
python3 scripts/devkit.py      # interactive menu for common tasks
```

## 6. Native dev (without Docker)

```bash
# Terminal 1 — database & redis via Docker only
docker compose up -d postgres redis mailpit

# Terminal 2 — API
cd api && composer install && cp .env.example .env
php artisan key:generate && php artisan migrate && php artisan serve

# Terminal 3 — Web
cd web && npm install && cp .env.example .env && npm run dev
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port already in use | Change `HTTP_PORT` / `WEB_PORT` in `.env` |
| API cannot connect to DB | Ensure `DB_HOST=postgres` in `api/.env` when using Docker |
| Web node_modules empty | Run `docker compose exec web npm install` |
| Permission errors on `storage/` | `docker compose exec api chown -R www-data:www-data storage bootstrap/cache` |
