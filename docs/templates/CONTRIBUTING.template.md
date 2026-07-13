# Contributing

> Copy to `docs/CONTRIBUTING.md` and customize for your team.

## Prerequisites

- PHP 8.2+, Composer
- Node.js 20+, npm
- Database (PostgreSQL recommended)

## Local setup

```bash
# Backend
cd api && composer install && cp .env.example .env && php artisan key:generate && php artisan migrate

# Frontend
cd web && npm install && cp .env.example .env
```

## Branching

- Branch from `main`: `feat/short-description`, `fix/issue-slug`, `chore/task`
- One logical change per PR when possible.

## Before opening a PR

```bash
# Backend
cd api && ./vendor/bin/pint && php artisan test

# Frontend
cd web && npm run lint && npm run test
```

## Commit messages

Use Conventional Commits:

- `feat(api): add invoice export endpoint`
- `fix(web): correct login redirect loop`
- `chore: update agent kit rules`

## AI agents

This repo includes an agent kit for Cursor, Claude Code, Copilot, and similar tools.
See root [`AGENTS.md`](../../AGENTS.md) for agent instructions.
