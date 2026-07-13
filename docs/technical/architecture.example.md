# Architecture example — Acme Billing

Fictional reference product showing how to fill in [`architecture.md`](architecture.md). **Do not treat this as live project docs.**

## Overview

Acme Billing is a B2B SaaS for small agencies to create invoices, collect payments, and export reports. Users: agency admins and staff. No public marketplace.

## Repository layout

| Path | Responsibility |
|------|----------------|
| `api/` | Laravel — auth, invoices, payments, PDF generation, webhooks |
| `web/` | Nuxt — dashboard, invoice editor, settings |
| `app/` | Flutter (optional) — mobile invoice approval only |
| `docker/` | Nginx, PHP-FPM, local mail capture |
| `scripts/` | Devkit, feature_review, bootstrap |

## Data flow

```
Browser → Nuxt (web/) → REST /api/v1 → Laravel (api/) → PostgreSQL
Stripe webhooks ──────────────────────→ api/routes/webhooks.php
Mobile (app/) ─────────────────────────→ same REST API
                              ↘ Redis (queues: SendInvoiceEmail, GeneratePdf)
```

## Key modules

| Module | API paths | Web routes | Notes |
|--------|-----------|------------|-------|
| Auth | `/api/v1/auth/*` | `/login`, `/register` | Sanctum SPA + API tokens |
| Invoices | `/api/v1/invoices` | `/invoices/*` | Policy: `InvoicePolicy` |
| Payments | `/api/v1/payments` | `/settings/billing` | Stripe Checkout |
| Reports | `/api/v1/reports` | `/reports` | Queued CSV export |

## External services

| Service | Purpose | Config |
|---------|---------|--------|
| PostgreSQL | Primary DB | `DB_*` |
| Redis | Queues + cache | `REDIS_*` |
| Stripe | Payments | `STRIPE_*` in `api/.env` |
| Mailpit (dev) | Email | SMTP 1025 |

## Security boundaries

- All invoice routes require auth + `InvoicePolicy`.
- Webhooks verified with Stripe signature middleware.
- No `env()` outside `config/` — enforced by architecture tests.

## Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01 | Sanctum for SPA | Same-origin Nuxt + API behind nginx |
| 2026-02 | Queue PDF generation | Avoid HTTP timeout on large invoices |

## Related (fictional)

- Product: `docs/product/features.md` would list invoice CRUD, Stripe billing
- API: `docs/technical/api-contract.md` would document `/api/v1/invoices`

Copy structure from this file into your real `architecture.md` after bootstrap.
