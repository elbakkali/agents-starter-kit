<!-- AUTO-GENERATED from .cursor/rules/core.mdc — edit the .mdc source and run: python3 -m scripts.tasks.sync_adapters -->

---
description: "Core agent conduct, feature gates, security baseline, and safety boundaries"
applyTo: "**"
---

# Core agent conduct

## Scope

- Implement only what was requested. No drive-by refactors unless completing feature review cleanup.
- Prefer the smallest correct diff. Reuse existing functions and components.
- Read surrounding code before writing — match naming, imports, and patterns.

## Workflow

1. Identify affected packages (`api/`, `web/`, `app/`, `docker/`, `docs/`).
2. Read the nearest `AGENTS.md` and relevant scoped rules.
3. Implement with tests when behavior changes.
4. **Feature completion** — review, refactor, remove orphans, update docs, run feature review.
5. **Session handoff** — after multi-file changes, copy [`HANDOFF.md.template`](../docs/technical/HANDOFF.md.template) → `docs/technical/HANDOFF.md` (gitignored).

## No orphaned code

- Delete files replaced by your change — do not leave old versions alongside new ones.
- Remove unused imports, exports, routes, components, and dead feature flags.
- Remove empty directories left after deletions.
- Never add `.bak`, `.tmp`, or "deprecated" copies — delete or migrate in the same PR.
- Run `python3 -m scripts.tasks.check_orphans` before finishing.

## Feature gate

A feature is **not done** until:

- Lint and tests pass for touched packages; orphans removed; docs updated in same PR.
- New/changed endpoints: auth, authorization, input validation; no secrets or user input in raw queries/shell/paths.
- Run `python3 -m scripts.tasks.feature_review` (or devkit → Quality → Post-feature review).

Deep checklist: [`.cursor/rules/feature-completion.mdc`](feature-completion.mdc). Security detail: [`.cursor/rules/security.mdc`](security.mdc), [`docs/technical/security.md`](../docs/technical/security.md).

## Security essentials

- Never commit `.env`, keys, tokens, or credentials.
- New/changed endpoints: authentication, authorization, validation before merge.
- No user-controlled data in raw SQL, shell, or file paths; escape output; security tests (401/403) on protected routes.

## Documentation

- **Technical** (`docs/technical/`) — how the system works; update with infra/API/architecture changes.
- **Product** (`docs/product/`) — what users see; update with user-facing feature changes.
- Same PR as the code change — never defer doc updates.
- When changing `api/`, `web/`, or `app/` behavior, touch at least one relevant doc in the same change.
- Map: infra/setup → `setup-*.md`; architecture/API → `architecture.md` or `api-contract.md`; user-facing → `features.md` or `user-flows.md`.
- End of session with multi-file changes: update local `docs/technical/HANDOFF.md` from [`HANDOFF.md.template`](../docs/technical/HANDOFF.md.template).

## Git safety

- Never commit `.env`, credentials, or API keys.
- Never force-push to `main` / `master`.
- Do not skip hooks unless the user explicitly requests it.

## Output

- State what changed, which docs were updated, and which commands you ran.
- Focus on non-obvious decisions only.
