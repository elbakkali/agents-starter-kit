# Technical documentation

Engineering docs for developers and AI agents. Keep these **up to date** with every feature that changes architecture, setup, or APIs.

## Index

| Document | Purpose | Update when |
|----------|---------|-------------|
| [setup-local.md](setup-local.md) | Run the project locally (Docker + native) | Tooling, env vars, or service topology changes |
| [setup-production.md](setup-production.md) | Deploy from scratch to production | Infra, CI/CD, or runtime config changes |
| [architecture.md](architecture.md) | System design, data flow, modules | Boundaries, auth, or integration changes |
| [api-contract.md](api-contract.md) | HTTP API contract and OpenAPI | New/changed endpoints |
| [security.md](security.md) | Shipped code security — CI, agents, review | Auth, validation, or security workflow changes |
| [agent-adapters.md](agent-adapters.md) | Multi-editor rule sync and token budget | Adapter files, editor compatibility, or sync workflow changes |
| [decisions/](decisions/) | Architecture Decision Records | Significant technical choices |
| [mcp-setup.md](mcp-setup.md) | Optional MCP servers for agents | MCP tooling changes |
| [tech-debt.md](tech-debt.md) | Known debt and cleanup targets | Debt added or resolved |

## Rules for agents

- **Technical** docs describe *how* the system works (code, infra, APIs).
- Update the relevant doc **in the same change** as the code — not in a follow-up.
- Link from root [`AGENTS.md`](../../AGENTS.md); do not duplicate long content there.
- Product (non-technical) docs live in [`../product/`](../product/).
