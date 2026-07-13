# AGENTS.md — Agents Starter Kit

Cross-tool instructions for AI coding agents in this repository.

## Repository map

| Path | Stack | Purpose |
|------|-------|---------|
| `api/` | Laravel / PHP | Backend API, auth, business logic, database |
| `web/` | Nuxt / Vue | Web frontend — pages, components, composables |
| `app/` | Flutter / Dart (optional) | Cross-platform app — HTTP to `api/` only; not scaffolded by default |
| `docker/` | Config | Nginx, PHP settings for containers |
| `docs/technical/` | Markdown | Engineering docs — setup, architecture, debt |
| `docs/product/` | Markdown | Product docs — features, flows, overview |
| `scripts/` | Python / Bash | Devkit menu and repeatable task scripts |

**New project from this kit:** [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md).

Nested `AGENTS.md` in `api/`, `web/`, and `app/` hold framework-specific commands.
The nearest file wins; chat prompts override everything.

## Docker (primary workflow)

```bash
cp .env.docker.example .env
docker compose up -d --build
python3 scripts/devkit.py          # interactive menu (↑↓←→ + Enter)
```

**First-time setup:** [`docs/technical/bootstrap.md`](docs/technical/bootstrap.md) or `python3 -m scripts.tasks.bootstrap_project`.

| Task | Command |
|------|---------|
| Start stack | `docker compose up -d` or devkit → Docker → Start stack |
| Stop stack | `docker compose down` |
| API tests | `docker compose exec api php artisan test` |
| Web tests | `docker compose exec web npm run test` |
| Post-feature review | `python3 -m scripts.tasks.feature_review` |
| CI (local) | `python3 -m scripts.tasks.docs_check` + `sync_adapters --check` |
| Start feature | `.cursor/skills/start-feature/SKILL.md` — spec before code |

Full guides: [`docs/technical/setup-local.md`](docs/technical/setup-local.md), [`docs/technical/setup-production.md`](docs/technical/setup-production.md). Native lint/test: see `api/AGENTS.md` and `web/AGENTS.md`.

## Feature completion

Every feature is **done** only after lint/tests pass, orphans removed, docs updated, and `python3 -m scripts.tasks.feature_review` (devkit → Quality → Post-feature review). Detail: [`.cursor/rules/feature-completion.mdc`](.cursor/rules/feature-completion.mdc).

## Documentation

| Category | Path | Update when |
|----------|------|-------------|
| **Technical** | `docs/technical/` | Architecture, setup, APIs, infra, or dev workflow changes |
| **Product** | `docs/product/` | User-visible features, flows, or positioning changes |

Key files: `setup-local.md`, `setup-production.md`, `architecture.md`, `features.md`, `user-flows.md`.
Run `python3 -m scripts.tasks.docs_check` to verify structure and links.

## Spec and handoff

Non-trivial features: `python3 -m scripts.tasks.scaffold_feature "Feature name"` — see [`.cursor/skills/start-feature/SKILL.md`](.cursor/skills/start-feature/SKILL.md). End of session: copy [`HANDOFF.md.template`](docs/technical/HANDOFF.md.template) → `docs/technical/HANDOFF.md` (gitignored; **required** after multi-file changes).

## Security

Shipped-code obligations: [`docs/technical/security.md`](docs/technical/security.md). Scoped rule: [`.cursor/rules/security.mdc`](.cursor/rules/security.mdc).

## Multi-editor support

`.cursor/rules/*.mdc` is source of truth — sync with `python3 -m scripts.tasks.sync_adapters`. See [`docs/technical/agent-adapters.md`](docs/technical/agent-adapters.md).

## Boundaries

**Always**

- Docker-first for local dev unless the user asks for native.
- When `api/`, `web/`, or `app/` behavior changes, update at least one doc in `docs/technical/` or `docs/product/` in the same change.
- Update technical **and** product docs when the feature warrants it.
- Remove deprecated code and files in the same PR — never leave orphans.
- Run post-feature review before marking a task complete.
- After editing `.cursor/rules/*.mdc`, run `python3 -m scripts.tasks.sync_adapters`.

**Ask first**

- Adding/removing dependencies, destructive migrations, prod deploy changes.
- Cross-package API contract changes.

**Never**

- Commit secrets, `.env`, or credentials.
- Force-push to `main` / `master`.
- Leave stub files, `.bak`, or unused components "for later".
- Skip tests or docs and promise a follow-up.

## Detailed rules (load on demand)

| Topic | Location |
|-------|----------|
| Core conduct & gates | [`.cursor/rules/core.mdc`](.cursor/rules/core.mdc) |
| Feature completion | [`.cursor/rules/feature-completion.mdc`](.cursor/rules/feature-completion.mdc) |
| Security | [`.cursor/rules/security.mdc`](.cursor/rules/security.mdc), [`docs/technical/security.md`](docs/technical/security.md) |
| Docs / Docker / Testing / Static analysis / API contract | [`.cursor/rules/`](.cursor/rules/) |
| Laravel / Nuxt / App | [`api/AGENTS.md`](api/AGENTS.md), [`web/AGENTS.md`](web/AGENTS.md), [`app/AGENTS.md`](app/AGENTS.md) |
| Multi-editor adapters | [`docs/technical/agent-adapters.md`](docs/technical/agent-adapters.md) |
| Bootstrap (day 0) | [`docs/technical/bootstrap.md`](docs/technical/bootstrap.md) |
| License | [`LICENSE`](LICENSE) |
