# API contract

Living document for public HTTP APIs. Update **in the same PR** as endpoint changes.

## Base URL

| Environment | URL |
|-------------|-----|
| Local (Docker) | `http://localhost/api` |
| Production | _TBD_ |

## Authentication

_Describe Sanctum/session/JWT approach after auth is implemented._

## OpenAPI

- Generate with [Scramble](https://scramble.dedoc.co/) when Laravel is scaffolded.
- Dev docs: `/docs/api`
- Export: commit or CI artifact as team policy dictates.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| _TBD_ | | | |

## Versioning

- Breaking changes require version bump or coordinated web release.
- Document deprecations here with sunset dates.

## Error format

Standard Laravel JSON errors / RFC 7807 — define once apps exist.

## Changelog

| Date | Change | PR |
|------|--------|-----|
| | Initial template | |
