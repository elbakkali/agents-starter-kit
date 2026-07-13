# Agents Starter Kit

Token-efficient instructions for AI coding agents (Cursor, Claude Code, Copilot, Codex, OpenClaw). Drop into any Laravel + Nuxt monorepo — or adapt for other stacks.

## What you get

| Component | Purpose |
|-----------|---------|
| [`AGENTS.md`](AGENTS.md) | Cross-tool source of truth |
| [`.cursor/rules/`](.cursor/rules/) | Scoped rules — **source of truth** (edit here) |
| [`.claude/rules/`](.claude/rules/) | Claude Code rules (auto-synced) |
| [`.github/instructions/`](.github/instructions/) | Copilot / VS Code rules (auto-synced) |
| [`docker-compose.yml`](docker-compose.yml) | Full local stack (API, web, Postgres, Redis, nginx, Mailpit) |
| [`docs/technical/`](docs/technical/) | Setup local/prod, architecture, tech debt |
| [`docs/product/`](docs/product/) | Product overview, features, user flows |
| [`scripts/devkit.py`](scripts/devkit.py) | Interactive menu (↑↓←→) for repeatable tasks |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | PR/push validation (docs, orphans, adapters, lint/test) |
| [`.cursor/skills/`](.cursor/skills/) | Spec-before-code and multi-agent workflows |
| [`.cursor/hooks.json`](.cursor/hooks.json) | Format PHP on edit, feature_review reminder on stop |

## Quick start

**New project (day 0):** follow [bootstrap guide](docs/technical/bootstrap.md) or run:

```bash
python3 -m scripts.tasks.bootstrap_project
```

**Existing scaffold:**

```bash
cp .env.docker.example .env
docker compose up -d --build
python3 scripts/devkit.py
```

## Devkit menu

Single entry point for repeated tasks:

```bash
python3 scripts/devkit.py
```

| Key | Action |
|-----|--------|
| ↑ / ↓ | Navigate within column |
| ← / → | Switch Categories ↔ Actions |
| Enter | Run selected action |
| q | Quit |

Categories: **Docker**, **Development**, **Documentation**, **Quality**.

Scaffold tasks (after apps exist): feature spec, API endpoint, web page.

## CI

GitHub Actions runs on PR/push:

- `docs_check`, `check_orphans`, `sync_adapters --check`, `validate_agents`
- Template-aware lint, test, static analysis (skips when no `composer.json` / `package.json`)
- Docker job when app manifests exist

Security workflow: secret scan (gitleaks/trufflehog), dependency review. Dependabot weekly.

## Spec before code

```bash
python3 -m scripts.tasks.scaffold_feature "My feature"
```

Approve spec, then implement. Skills: `.cursor/skills/start-feature/`, `planner/`, `implementer/`, `reviewer/`.

## Documentation (two categories)

| Category | Path | Update when |
|----------|------|-------------|
| **Technical** | `docs/technical/` | Architecture, setup, APIs, infra |
| **Product** | `docs/product/` | User-facing features and flows |

Agents must keep both up to date in the same PR as code changes.

Verify docs: `python3 -m scripts.tasks.docs_check`

## Feature completion

Before marking any feature done:

```bash
python3 -m scripts.tasks.feature_review
```

This runs orphan check, lint, tests, static analysis, doc validation, and AGENTS.md checks.

## Install into an existing project

```bash
chmod +x scripts/install.sh
./scripts/install.sh /path/to/your-project
```

## Key guides

- [Bootstrap (day 0)](docs/technical/bootstrap.md)
- [Local setup from scratch](docs/technical/setup-local.md)
- [Production setup from scratch](docs/technical/setup-production.md)
- [Technical docs index](docs/technical/README.md)
- [Product docs index](docs/product/README.md)

## Tool compatibility

Multi-editor setup, sync workflow, and generated files: [`docs/technical/agent-adapters.md`](docs/technical/agent-adapters.md).

## Token budget

- Root `AGENTS.md` + `core.mdc` load always (~150 lines).
- Security, feature-completion, Laravel, Nuxt, Docker, and docs rules load on demand via globs.
- Long content lives in `docs/` — linked, not inlined.

## License

[MIT](LICENSE) — Agents Starter Kit contributors. Customize freely.
