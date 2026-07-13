# AGENTS.md — Flutter App (optional)

Optional cross-platform app package. Read root [`AGENTS.md`](../AGENTS.md) for shared rules.

This directory is a stub until you scaffold a Flutter app. The agent kit does not include Flutter in Docker by default.

## Stack

- Flutter / Dart (when scaffolded).
- HTTP client only — talk to `api/` over REST; no direct database access.
- State management: match patterns already in the codebase (Riverpod, Bloc, etc.).

## Commands (run from `app/`)

Native Flutter toolchain required (not in Docker compose):

```bash
flutter pub get
flutter run
flutter test
flutter analyze
dart format .
```

## Conventions

- API base URL from environment / build flavors — never hardcode production URLs.
- Keep platform channels thin; business logic in Dart services.
- Match API contract in [`docs/technical/api-contract.md`](../docs/technical/api-contract.md).

## Testing

- Widget and integration tests with `flutter test`.
- Mock HTTP at the repository/service layer.

## Security

- Rule: [`.cursor/rules/security.mdc`](../.cursor/rules/security.mdc); guide: [`docs/technical/security.md`](../docs/technical/security.md).
- No API secrets in bundle; use secure storage for tokens; validate output before display.
- Run `security_check` in feature review.

## Boundaries

- **Never** embed API secrets or backend credentials in the app bundle.
- **Never** access the database directly — use `api/` only.
- **Ask first** before adding pub dependencies or changing minimum SDK versions.
