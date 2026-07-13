# Production setup (from scratch)

Deploy this project to production. Update this file when deployment steps, secrets, or infrastructure change.

## Overview

```
Internet → TLS terminator (nginx / cloud LB) → nginx → api (PHP-FPM) + web (Nuxt SSR)
                                                      ↘ postgres, redis
```

## Prerequisites

- Linux host or container platform (Docker, Kubernetes, Forge, Fly.io, etc.)
- Domain + TLS certificate (Let's Encrypt or provider)
- PostgreSQL 16+ (managed or self-hosted)
- Redis 7+
- Secrets store (never commit production `.env`)

## 1. Build production images

```bash
cp .env.docker.example .env
# Set production values: APP_KEY, DB_*, strong passwords

docker compose -f docker-compose.yml -f docker-compose.prod.yml build
```

## 2. Environment variables

Set these in your host or orchestrator (not in git):

| Variable | Description |
|----------|-------------|
| `APP_KEY` | Laravel app key (`php artisan key:generate --show`) |
| `APP_URL` | Public URL, e.g. `https://app.example.com` |
| `DB_*` | Production database credentials |
| `REDIS_*` | Production Redis |
| `NUXT_PUBLIC_API_BASE` | Public API URL the browser calls |

Copy from `api/.env.example` and `web/.env.example`; map Docker service names to production hosts.

## 3. Database bootstrap

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm api php artisan migrate --force
# Optional: docker compose ... run --rm api php artisan db:seed --force
```

## 4. Start production stack

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

For managed platforms, push images to your registry and reference them in your platform config instead of building on the server.

## 5. TLS and reverse proxy

Terminate TLS at nginx or your cloud load balancer. Example nginx additions (not included in dev config):

- Redirect HTTP → HTTPS
- `proxy_pass` to web and fastcgi to api
- Rate limiting and security headers

Document your provider-specific steps below:

### Provider: _(fill in — e.g. Laravel Forge, AWS ECS, Hetzner)_

1. ...
2. ...

## 6. Post-deploy verification

- [ ] Homepage loads over HTTPS
- [ ] API health endpoint responds
- [ ] Login / auth flow works
- [ ] Queues and scheduled tasks running (if applicable)
- [ ] Backups configured for PostgreSQL
- [ ] Monitoring and log aggregation active

## 7. Rollback

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
# Deploy previous image tag, then:
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
# Roll back migrations only if safe — ask first
```

## CI/CD

Document your pipeline here when added:

| Stage | Command / trigger |
|-------|-------------------|
| Test | `docker compose exec api php artisan test` + web tests |
| Build | `docker compose -f docker-compose.yml -f docker-compose.prod.yml build` |
| Deploy | _(fill in)_ |
