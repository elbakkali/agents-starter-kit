---
name: update-product-docs
description: >-
  On feature complete: update docs/product/features.md and user-flows.md when
  user-visible behavior changed. Use after implementation or during feature review.
---

# Update product docs

Run when a feature changes **what users see or do**. Skip for internal-only refactors.

## Checklist

1. Read the approved spec (`docs/product/specs/…`) and list user-visible changes.
2. Update [`docs/product/features.md`](../../docs/product/features.md):
   - Add or revise feature bullets
   - Remove deleted features in the same PR
3. Update [`docs/product/user-flows.md`](../../docs/product/user-flows.md) when flows change:
   - New screens, steps, or auth gates
   - Diagrams or numbered steps — keep copy-paste runnable
4. Touch [`docs/product/overview.md`](../../docs/product/overview.md) only if positioning changes.
5. Run `python3 -m scripts.tasks.docs_check` and `python3 -m scripts.tasks.check_doc_updates`.

## When not to update product docs

- Backend-only changes with no UI impact
- Test-only, CI, or agent-kit changes
- Docs/technical-only updates

## Pair with technical docs

| Change | Product | Technical |
|--------|---------|-----------|
| New user-facing screen | features.md, user-flows.md | architecture.md if new module |
| New API consumed by web | user-flows if UX changes | api-contract.md |
| Docker/setup only | — | setup-local.md |

## Gate

Product doc updates belong in the **same PR** as the code. Feature review runs `check_doc_updates` when `api/`, `web/`, or `app/` code changes.
