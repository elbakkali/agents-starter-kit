"""Scaffold Nuxt page and composable stubs when a Nuxt app exists."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower())
    return slug.strip("-") or "page"


def camel(name: str) -> str:
    parts = re.split(r"[-_\s]+", name.strip())
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def main() -> None:
    if not (WEB / "package.json").exists():
        print("Skip: no Nuxt app in web/ (run nuxi init or scaffold Nuxt first).")
        sys.exit(0)

    page_name = " ".join(sys.argv[1:]).strip()
    if not page_name:
        page_name = input("Page name (e.g. invoices): ").strip()
    if not page_name:
        print("Page name required.", file=sys.stderr)
        sys.exit(1)

    slug = slugify(page_name)
    composable_name = camel(page_name)
    page = WEB / "pages" / slug / "index.vue"
    composable = WEB / "composables" / f"use{composable_name[0].upper()}{composable_name[1:]}.ts"
    test = WEB / "tests" / "pages" / f"{slug}.spec.ts"

    if page.exists():
        print(f"Already exists: {page}", file=sys.stderr)
        sys.exit(1)

    page.parent.mkdir(parents=True, exist_ok=True)
    composable.parent.mkdir(parents=True, exist_ok=True)
    test.parent.mkdir(parents=True, exist_ok=True)

    use_fn = f"use{composable_name[0].upper()}{composable_name[1:]}"

    page.write_text(
        f"""<script setup lang="ts">
const {{ data, pending, error }} = await {use_fn}()
</script>

<template>
  <div>
    <h1>{page_name.title()}</h1>
    <p v-if="pending">Loading…</p>
    <p v-else-if="error">Something went wrong.</p>
    <pre v-else>{{ data }}</pre>
  </div>
</template>
""",
        encoding="utf-8",
    )

    composable.write_text(
        f"""export function {use_fn}() {{
  return useAsyncData('{slug}', () =>
    // TODO: call API composable or $fetch
    Promise.resolve([]),
  )
}}
""",
        encoding="utf-8",
    )

    test.write_text(
        f"""import {{ describe, it, expect }} from 'vitest'
import {{ mountSuspended }} from '@nuxt/test-utils/runtime'
// import Page from '~/pages/{slug}/index.vue'

describe('{slug} page', () => {{
  it('renders', async () => {{
    // TODO: mount page after spec approval
    expect(true).toBe(true)
  }})
}})
""",
        encoding="utf-8",
    )

    print(f"Created: {page.relative_to(ROOT)}")
    print(f"Created: {composable.relative_to(ROOT)}")
    print(f"Created: {test.relative_to(ROOT)}")
    print(f"Route: /{slug}")
    print("Update docs/product/user-flows.md if this is user-visible.")


if __name__ == "__main__":
    main()
