## Summary

<!-- What changed and why -->

## Spec

- [ ] Linked spec: `docs/product/specs/…` (or N/A for kit/docs-only)
- [ ] Acceptance criteria met

## Feature completion checklist

- [ ] Lint passes (`python3 -m scripts.tasks.lint_all native` or Docker)
- [ ] Tests pass (`python3 -m scripts.tasks.test_all native` or Docker)
- [ ] Static analysis pass or skip documented (`python3 -m scripts.tasks.static_analysis`)
- [ ] No orphaned files (`python3 -m scripts.tasks.check_orphans`)
- [ ] Docs updated (technical and/or product as applicable)
- [ ] `python3 -m scripts.tasks.feature_review` passes locally
- [ ] Cross-editor adapters synced if `.mdc` rules changed (`python3 -m scripts.tasks.sync_adapters`)

## Security (shipped code)

- [ ] New/changed endpoints have auth + authorization + input validation
- [ ] No secrets, tokens, or credentials in the diff
- [ ] No user-controlled data in raw SQL, shell commands, or file paths
- [ ] User content escaped / no unsafe `v-html`
- [ ] Feature tests cover 401/403 on protected routes (when applicable)
- [ ] `python3 -m scripts.tasks.security_check` passes (or skips in template mode)

## Test plan

- [ ] …

## Notes

<!-- Non-obvious decisions, ADR links, follow-ups -->
