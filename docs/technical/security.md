# Security

What we enforce for **shipped code** (application security), not only secrets and dependency bots.

## Layers

| Layer | What it covers | Where |
|-------|----------------|-------|
| **CI (automated)** | Secret scan (gitleaks, TruffleHog), dependency review on PRs, `composer audit` / `npm audit`, anti-pattern grep | `.github/workflows/security.yml`, `.github/workflows/ci.yml` |
| **Agent rules** | Auth, validation, output encoding, security tests on new endpoints | `.cursor/rules/security.mdc`, package `AGENTS.md` |
| **Human review** | IDOR, mass assignment, CSRF, business-logic auth, threat modeling | PR template, `.cursor/skills/reviewer/SKILL.md` |

## Before merge (developers and agents)

1. New/changed routes: authentication + authorization + validated input.
2. No user input in raw SQL, shell, or filesystem paths.
3. Escape or sanitize user content in HTML; avoid unsafe `v-html`.
4. Feature tests for 401/403 on protected endpoints.
5. Run `python3 -m scripts.tasks.security_check` (included in `feature_review`).
6. No secrets or credentials in the diff.

## Local commands

```bash
python3 -m scripts.tasks.security_check          # audits + anti-pattern scan
docker compose exec api composer audit           # when api/ exists
docker compose exec web npm audit --audit-level=high
python3 -m scripts.tasks.feature_review          # full post-feature gate
```

## Template mode

When `api/composer.json` or `web/package.json` are absent, dependency audits skip gracefully. Anti-pattern scan still runs on existing source trees.

## Decisions

Significant security choices → ADR in [`decisions/`](decisions/).
