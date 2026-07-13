# MCP setup (optional)

Optional Model Context Protocol servers for richer agent context. Not required for the template.

## Laravel Boost (API)

When the Laravel app is scaffolded, [Laravel Boost](https://laravel.com/docs/boost) can expose:

- Route list, config, and schema awareness
- Artisan command execution (sandboxed per your policy)

Setup (after `composer.json` exists):

1. Install per Laravel Boost docs in `api/`.
2. Register the MCP server in Cursor → Settings → MCP.
3. Scope to `api/` paths only in agent prompts.

## Semantic / codebase search

- Cursor built-in codebase indexing covers most monorepos.
- Optional: add a docs MCP server pointing at `docs/technical/` for RAG over architecture.

## Security

- Do not expose production credentials to MCP tools.
- Prefer read-only MCP tools in CI; interactive tools for local dev only.
- Review `.cursor/mcp.json` (if added) before committing — no secrets.

## Template note

This repo ships without MCP config. Add project-specific MCP entries when apps exist.
