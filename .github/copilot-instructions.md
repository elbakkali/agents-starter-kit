# GitHub Copilot instructions

**Primary source:** [AGENTS.md](../AGENTS.md) — read this first for commands, boundaries, and doc rules.

**Scoped rules:** `.github/instructions/*.instructions.md` (auto-synced from `.cursor/rules/*.mdc`).

After editing Cursor rules, regenerate adapters:

```bash
python3 -m scripts.tasks.sync_adapters
```

Do not duplicate long content in this file — keep it as an index.
