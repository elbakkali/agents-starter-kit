# Playwright E2E (template)

Minimal Playwright setup for smoke tests after Nuxt is scaffolded.

## Install

From `web/` after `nuxi init`:

```bash
npm init playwright@latest
# Or: npm install -D @playwright/test && npx playwright install
```

Copy or merge configs from this directory (`web/e2e/`).

## Run

```bash
cd web && npx playwright test
# Or from project root:
python3 -m scripts.tasks.e2e_smoke
```

## CI

E2E is optional in template mode. Enable in CI when `web/playwright.config.ts` exists and browsers are installed.

## Related

- [bootstrap.md](bootstrap.md) — initial setup
- Devkit → Development (when wired)
