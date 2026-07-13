# Flutter app (optional)

This directory is a stub until you scaffold a Flutter app.

## Scaffold

```bash
# Automated (from project root)
python3 -m scripts.tasks.bootstrap_project --flutter

# Manual
flutter create --project-name my_app app
```

Or copy the template and customize:

```bash
cp pubspec.yaml.template pubspec.yaml
flutter pub get
```

## Configuration

- API base URL from `--dart-define` or env — never hardcode production URLs.
- HTTP to `api/` only; see [`docs/technical/api-contract.md`](../docs/technical/api-contract.md).
- Not included in Docker Compose by default; run on device/emulator with native Flutter SDK.

## Dependabot

When `pubspec.yaml` exists, uncomment the `pub` entry in [`.github/dependabot.yml`](../.github/dependabot.yml).

## Commands

See [`app/AGENTS.md`](AGENTS.md).
