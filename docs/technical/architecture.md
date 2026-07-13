# Architecture

> Keep this file current. Move content from `docs/templates/architecture.template.md` here on first setup.

## Overview

Brief description of what this product does and who uses it.

## Repository layout

| Path | Responsibility |
|------|----------------|
| `api/` | Laravel API — auth, business logic, persistence |
| `web/` | Nuxt browser frontend — UI, client-side state, API consumption |
| `app/` | Flutter cross-platform app (optional) — HTTP to `api/` only; not in Docker by default |
| `docker/` | Nginx, PHP config for containerized dev/prod |
| `scripts/` | Devkit and repeatable task scripts |

## Data flow

```
Browser → Nuxt (web/) → HTTP API → Laravel (api/) → PostgreSQL
Flutter app (app/) ──────────────────┘
                              ↘ Redis (cache / queues)
```

## Key modules

- **Auth**: _(fill in paths)_
- **Core domain**: _(fill in paths)_

## External services

| Service | Purpose | Config |
|---------|---------|--------|
| PostgreSQL | Primary DB | `DB_*` in `api/.env` |
| Redis | Cache / queues | `REDIS_*` in `api/.env` |
| Mailpit | Local email (dev only) | SMTP port 1025 |

## Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| | | |

## Related docs

- [Local setup](setup-local.md)
- [Production setup](setup-production.md)
- [Product overview](../product/overview.md)
