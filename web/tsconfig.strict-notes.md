When `web/package.json` exists, enable strict checking in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true
  }
}
```

Run typecheck via `python3 -m scripts.tasks.static_analysis` or `npm run typecheck`.
