<!-- AUTO-GENERATED from .cursor/rules/api-contract.mdc — edit the .mdc source and run: python3 -m scripts.tasks.sync_adapters -->

---
paths: api/**/*
---

# API contract

## OpenAPI / Scramble

- Document all public HTTP endpoints with **dedoc/scramble** (or equivalent).
- Export OpenAPI at `/docs/api` (dev) — never ship undocumented routes.
- Keep `docs/technical/api-contract.md` in sync with breaking changes.

## Endpoint rules

- Version breaking changes (`/api/v2`) or coordinate with web in same PR.
- Request validation in Form Requests; response shapes via API Resources.
- List auth requirements per route in OpenAPI annotations/attributes.

## Cross-package changes

- **Ask first** before changing response shapes consumed by `web/`.
- Update web types/composables and product docs when user-visible.

## Checklist (new endpoint)

1. Route + controller + Form Request + policy
2. Feature test + OpenAPI attributes
3. Entry in `docs/technical/api-contract.md`
4. Web composable/types if consumed by frontend
