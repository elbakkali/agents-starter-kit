# AGENTS.md — Laravel API

Backend package. Read root [`AGENTS.md`](../AGENTS.md) for shared rules.

## Stack

- Laravel (PHP 8.2+), Pest for tests, Laravel Pint for formatting.
- Business logic in Actions/Services; controllers stay thin.
- Validation in Form Request classes, not inline in controllers.

## Commands (run from `api/`)

Prefer Docker from project root: `docker compose exec api <command>` or `python3 scripts/devkit.py`.

```bash
composer install
php artisan serve                    # native dev only
php artisan test                     # full suite
php artisan test --filter=UserTest   # single test/class
./vendor/bin/pint                    # format PHP
php artisan migrate                  # local only
```

## API contract

- Document endpoints with Scramble/OpenAPI — see [`docs/technical/api-contract.md`](../docs/technical/api-contract.md).
- Rule: [`.cursor/rules/api-contract.mdc`](../.cursor/rules/api-contract.mdc).

## Static analysis

- PHPStan: `api/phpstan.neon.dist` — run via `python3 -m scripts.tasks.static_analysis`.
- Architecture tests: `tests/Architecture/` when introduced.

## Conventions

- Eloquent relationships over raw queries; eager-load to avoid N+1.
- Use route model binding and policy authorization for resource access.
- Queue long-running work; do not block HTTP requests.
- Config and env via `config/` — never call `env()` outside config files.

## Testing

- Feature tests for HTTP endpoints; unit tests for isolated logic.
- Use factories and `RefreshDatabase` for database tests.
- Mock external HTTP/API calls; hit the real DB for integration paths.

## Security

- Rule: [`.cursor/rules/security.mdc`](../.cursor/rules/security.mdc); guide: [`docs/technical/security.md`](../docs/technical/security.md).
- New/changed routes: auth middleware, policy authorization, Form Request validation.
- Feature tests for 401/403; run `composer audit` and `security_check` in feature review.

## Boundaries

- **Never** run destructive migrations (`migrate:fresh`, `db:wipe`) without explicit approval.
- **Ask first** before changing `composer.json`, service providers, or middleware stack.
