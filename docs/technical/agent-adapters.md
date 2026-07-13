# Multi-editor agent adapters

`AGENTS.md` is the cross-tool contract for commands, boundaries, and doc rules. Scoped rules live in [`.cursor/rules/*.mdc`](../../.cursor/rules/) — **edit rules there**, not in generated adapter files.

## Editor compatibility

| Editor | Config | Notes |
|--------|--------|-------|
| **Cursor** | `AGENTS.md` + `.cursor/rules/*.mdc` | Source of truth — edit `.mdc` files here |
| **Claude Code** | `CLAUDE.md` → `AGENTS.md` + [`.claude/rules/`](../../.claude/rules/) | Synced from `.mdc` |
| **GitHub Copilot / VS Code** | [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) + [`.github/instructions/`](../../.github/instructions/) | Synced from `.mdc` |
| **Codex / Windsurf / Jules** | `AGENTS.md` natively | [`.windsurfrules`](../../.windsurfrules) is a pointer |
| **Aider** | [`.aider.conf.yml`](../../.aider.conf.yml) | Reads `AGENTS.md` |
| **Gemini CLI** | [`.gemini/settings.json`](../../.gemini/settings.json) | Reads `AGENTS.md` |
| **OpenClaw** | Copy `AGENTS.md` to workspace | Operating contract |

## Sync workflow

After editing any `.cursor/rules/*.mdc` file:

```bash
python3 -m scripts.tasks.sync_adapters
```

CI verifies adapters are up to date:

```bash
python3 -m scripts.tasks.sync_adapters --check
```

## Generated files (do not hand-edit)

| Source (edit here) | Generated outputs |
|--------------------|-------------------|
| `.cursor/rules/*.mdc` | `.claude/rules/*.md` |
| `.cursor/rules/*.mdc` | `.github/instructions/*.instructions.md` |
| `AGENTS.md` (manual) | `CLAUDE.md` (symlink on install), `.github/copilot-instructions.md` (partial) |

Generated files include an auto-generated banner pointing back to the `.mdc` source. Hand-editing them will be overwritten on the next sync.

## Token budget

Always-loaded context targets ~150 lines:

- Root `AGENTS.md` (~100 lines)
- `.cursor/rules/core.mdc` only (`alwaysApply: true`)

Scoped rules (`security.mdc`, `feature-completion.mdc`, Laravel, Nuxt, Docker, docs) load on demand via globs when editing matching paths.

Long content lives in `docs/` — linked from rules, not inlined.

## Install into another project

The install script copies `AGENTS.md`, nested package `AGENTS.md` files, `.cursor/rules/`, and runs `sync_adapters` to populate adapter directories. See [`scripts/install.sh`](../../scripts/install.sh).
