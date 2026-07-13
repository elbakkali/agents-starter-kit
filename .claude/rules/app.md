<!-- AUTO-GENERATED from .cursor/rules/app.mdc — edit the .mdc source and run: python3 -m scripts.tasks.sync_adapters -->

---
paths: app/**/*.dart
---

# Flutter / app conventions

## Architecture

- Talk to `api/` over HTTP only — no direct database or backend imports.
- Keep widgets thin; put API and business logic in services or repositories.
- Use typed models for API responses; avoid raw `Map` at UI boundaries.

## Patterns

```dart
// ❌ BAD — hardcoded URL, no error handling
final data = await http.get(Uri.parse('https://api.example.com/users'));

// ✅ GOOD — config-driven base URL, typed repository
final users = await userRepository.fetchUsers();
```

## Testing

- Unit-test repositories and services with mocked HTTP.
- Widget tests for user-visible behavior, not private methods.

## Do not

- Store secrets in the app bundle — use secure storage for tokens when needed.
- Import from `api/` or `web/` paths — HTTP API only.
- Add Flutter to Docker compose without an ADR and setup doc updates.
