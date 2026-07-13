---
name: start-feature
description: >-
  Spec-before-code workflow: explore, write feature spec, get approval, implement,
  then run feature_review. Use when starting a new feature or user asks to plan before coding.
---

# Start feature (spec before code)

Follow this workflow for **every non-trivial feature**. Do not jump to implementation without an approved spec.

## 1. Explore

- Read nearest `AGENTS.md`, relevant `.cursor/rules/*.mdc`, and `docs/technical/architecture.md`.
- Search codebase for existing patterns (composables, actions, tests).
- Note affected packages: `api/`, `web/`, `app/`, `docs/`.

## 2. Write spec

Create a spec from the template:

```bash
python3 -m scripts.tasks.scaffold_feature "Feature name"
```

Or copy `docs/templates/feature-spec.template.md` to `docs/product/specs/<slug>.md`.

Fill in: problem, goals, non-goals, user stories, acceptance criteria, technical notes, open questions.

Update **product** docs outline if user-visible (`features.md`, `user-flows.md`).

## 3. Get approval

- Present the spec to the user/stakeholder.
- Resolve open questions; check **Approval** boxes in the spec.
- **Do not implement** until explicit approval.

## 4. Implement

- Match existing patterns; smallest correct diff.
- Backend: consider `python3 -m scripts.tasks.scaffold_api_endpoint` after Laravel exists.
- Frontend: consider `python3 -m scripts.tasks.scaffold_web_page` after Nuxt exists.
- Behavior change → add/update tests.
- Update technical **and** product docs in the same change.

## 5. Feature review

```bash
python3 -m scripts.tasks.feature_review
```

Confirm: no orphans, lint/tests/static analysis pass, docs updated.

## Handoff

Copy `docs/technical/HANDOFF.md.template` → `HANDOFF.md` (gitignored) for session notes.
