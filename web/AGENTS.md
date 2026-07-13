# AGENTS.md — Nuxt Web

Web frontend package. Read root [`AGENTS.md`](../AGENTS.md) for shared rules.

## Stack

- Nuxt 3+ / Vue 3, Composition API, TypeScript preferred for new files.
- Composables for shared state and API calls; pages stay thin.
- Use existing UI library patterns (Nuxt UI, Tailwind) already in the codebase.

## Commands (run from `web/`)

Prefer Docker from project root: `docker compose exec web <command>` or `python3 scripts/devkit.py`.

```bash
npm install
npm run dev                          # native dev only
npm run build
npm run lint
npm run test
npm run test -- path/to/file.spec.ts
```

## Conventions

- `<script setup lang="ts">` for new Vue SFCs.
- Colocate composables in `composables/`; prefix with `use`.
- Fetch data in composables or `useAsyncData` / `useFetch` — not scattered in templates.
- Match existing styling (Tailwind utilities, design tokens) — do not invent new patterns.

## Testing

- Component tests with Vitest + `@vue/test-utils`.
- Test user-visible behavior, not implementation details.
- Mock API calls at the composable or fetch layer.

## Security

- Rule: [`.cursor/rules/security.mdc`](../.cursor/rules/security.mdc); guide: [`docs/technical/security.md`](../docs/technical/security.md).
- No secrets in bundle (`NUXT_PUBLIC_*` only); no unsafe `v-html` with user content.
- Run `npm audit --audit-level=high` and `security_check` in feature review.

## Boundaries

- **Never** call backend DB or secrets from the web app.
- **Ask first** before adding npm dependencies or changing Nuxt modules config.
