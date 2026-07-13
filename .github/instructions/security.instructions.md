<!-- AUTO-GENERATED from .cursor/rules/security.mdc — edit the .mdc source and run: python3 -m scripts.tasks.sync_adapters -->

---
description: "Security baseline — OWASP, secrets, auth, dependencies, shipped code"
applyTo: "api/**,web/**,app/**,docs/technical/security.md"
---

# Security baseline

## Secrets

- Never commit `.env`, keys, tokens, or credentials.
- Use env vars and secret managers in production.
- CI runs gitleaks/trufflehog (see `.github/workflows/security.yml`).

## Shipped code (application security)

Every PR must leave the codebase safer, not merely secret-free:

- **New/changed endpoints:** authentication, authorization (policies/gates), and input validation (Form Requests / typed schemas) before merge.
- **No user-controlled data** in raw SQL, `DB::raw`, shell commands, or file paths — use parameterized queries and allowlists.
- **Output encoding:** escape user content in HTML; no `v-html` with untrusted input; API Resources for consistent response shapes.
- **Security tests:** feature tests asserting 401/403 on protected routes; regression tests for auth boundaries on new routes.
- **Dependencies:** run `composer audit` (api) and `npm audit --audit-level=high` (web) before shipping; fix or document accepted high/critical findings.

See [`docs/technical/security.md`](../../docs/technical/security.md) for CI vs agent vs human review.

## Laravel (api/)

- CSRF for web routes; Sanctum/Passport for API tokens as appropriate.
- Mass assignment: `$fillable` / `$guarded`; validate all input via Form Requests.
- Authorize with policies/gates; never trust client-sent user IDs for ownership.
- Parameterize queries (Eloquent); no raw SQL with user input.
- Rate-limit auth and sensitive endpoints.

## Nuxt (web/)

- No secrets in client bundle — public env vars only (`NUXT_PUBLIC_*`).
- Sanitize user HTML; avoid `v-html` with untrusted content.
- Call API over HTTPS; store tokens in httpOnly cookies when possible.

## Flutter (app/)

- No API secrets or credentials in the app bundle; use secure storage for tokens.
- Validate and encode user content before display; never trust client-side auth alone.
- Call `api/` over HTTPS only; no direct database access.

## Dependencies

- Dependabot enabled for Composer, npm, and GitHub Actions.
- Review security advisories before merging dependency bumps.

## Reporting

- Document security decisions in `docs/technical/decisions/` (ADRs).
