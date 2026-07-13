# Architecture

> Copy to `docs/technical/architecture.md` on first setup. See also `docs/technical/` and `docs/product/`.

## Overview

Brief description of what this product does and who uses it.

## Repository layout

| Path | Responsibility |
|------|----------------|
| `api/` | Laravel API — auth, business logic, persistence |
| `web/` | Nuxt web frontend — UI, browser-side state, API consumption |
| `app/` | Flutter cross-platform app (optional) — HTTP to `api/` only |

## Data flow

```
Browser → Nuxt (web/) → HTTP API → Laravel (api/) → Database
Flutter app (app/) ──────────────────┘
```

Describe auth flow (session, Sanctum, JWT, etc.) and any queues or webhooks.

## Key modules

List major domains and where they live:

- **Auth**: `api/app/Http/Controllers/Auth/`, `web/composables/useAuth.ts`
- **Billing**: (fill in paths)
- **Core domain**: (fill in paths)

## External services

| Service | Purpose | Config location |
|---------|---------|-----------------|
| PostgreSQL | Primary DB | `api/.env` `DB_*` |
| Redis | Cache / queues | `api/.env` `REDIS_*` |
| (add rows) | | |

## API contract

- Base URL: `/api/v1` (adjust)
- Auth header: `Authorization: Bearer {token}` (adjust)
- Link to OpenAPI / Scramble docs if available.

## Decisions log

Record non-obvious architectural choices so agents do not reverse them:

| Date | Decision | Rationale |
|------|----------|-----------|
| YYYY-MM-DD | Example: Actions over Services | Team preference, easier testing |

## Tech debt

Track known debt agents should not worsen:

- [ ] Example: Legacy endpoint `/api/old-users` — migrate to v1 before extending
