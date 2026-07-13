# MCP setup (optional)

Model Context Protocol servers extend what agents can see and do. **Not required** for the starter kit — add when apps are scaffolded.

## Quick start (Cursor)

1. Open **Cursor → Settings → MCP**
2. Add servers below (project or user scope)
3. Restart Cursor after config changes
4. Never commit secrets in MCP config — use env vars

Example project config (create if needed): `.cursor/mcp.json` (gitignore if it holds local paths only).

## Laravel Boost (API)

When Laravel exists in `api/`, [Laravel Boost](https://laravel.com/docs/boost) provides:

| Capability | Use |
|------------|-----|
| Route list | Avoid hallucinated endpoints |
| Schema / models | Accurate migrations and queries |
| Artisan (sandboxed) | One-off tasks with policy |

Setup:

```bash
cd api
# Follow Laravel Boost install docs for your Laravel version
```

Register in Cursor MCP. Scope agent prompts to `api/` for backend work.

## Documentation MCP (optional)

Point a read-only docs server at:

- `docs/technical/` — architecture, API contract, setup
- `docs/product/` — features and user flows

Useful for planners; built-in codebase indexing often suffices.

## Database / API exploration

| Tool | When | Caution |
|------|------|---------|
| Postgres MCP | Local dev only | Read-only user; never production credentials |
| OpenAPI / Scramble | After `dedoc/scramble` install | `/docs/api` — see [api-contract.md](api-contract.md) |
| HTTP client MCP | Integration testing | No prod URLs with real tokens |

## Security checklist

- [ ] MCP tools are read-only in CI; write/exec tools local dev only
- [ ] No production DB URLs or API keys in committed MCP config
- [ ] Review `.cursor/mcp.json` before push
- [ ] Team policy for which MCP servers are approved

## Multi-editor note

MCP config is editor-specific. Document approved servers in this file when the team adopts them.

## Template state

This repo ships **without** committed MCP config. Update this guide when you add project-specific servers.
