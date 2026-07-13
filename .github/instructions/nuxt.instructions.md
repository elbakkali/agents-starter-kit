<!-- AUTO-GENERATED from .cursor/rules/nuxt.mdc — edit the .mdc source and run: python3 -m scripts.tasks.sync_adapters -->

---
description: "Nuxt and Vue frontend conventions for web/ files"
applyTo: "web/**/*.{vue,ts,js}"
---

# Nuxt / Vue conventions

## Components

- Use `<script setup lang="ts">` for new single-file components.
- Props and emits must be typed with `defineProps` / `defineEmits`.
- Keep templates readable — extract logic to composables when a script block grows.

## Patterns

```vue
<!-- ❌ BAD — fetch in template, no typing -->
<script setup>
const { data } = await useFetch('/api/users')
</script>

<!-- ✅ GOOD — typed composable, clear responsibility -->
<script setup lang="ts">
const { users, pending, error } = useUsers()
</script>
```

## Composables

- Place in `composables/use*.ts`; one concern per composable.
- Return reactive state and methods; do not expose raw fetch internals.
- Handle loading and error states — do not assume success.

## Styling

- Follow existing Tailwind / UI library patterns in the codebase.
- No inline styles unless the project already uses them for a specific case.

## Do not

- Store secrets or API keys in client code.
- Import from backend paths (`api/`) — use HTTP API only.
- Add global state without checking if a composable or Pinia store already exists.
