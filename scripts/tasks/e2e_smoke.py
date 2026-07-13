"""Run Playwright E2E smoke tests when installed; skip in template mode."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.runner import ROOT, run, web_is_kit_stub

WEB = ROOT / "web"


def _playwright_ready() -> bool:
    if not (WEB / "package.json").exists() or web_is_kit_stub():
        return False
    config = WEB / "playwright.config.ts"
    template = WEB / "e2e" / "playwright.config.ts.template"
    return config.exists() or template.exists()


def main() -> None:
    if not _playwright_ready():
        print("Skip E2E: no Nuxt app or Playwright config (template mode).")
        return

    config = WEB / "playwright.config.ts"
    cfg_arg = ["--config=playwright.config.ts"] if config.exists() else []

    try:
        run(["npx", "playwright", "test", *cfg_arg], cwd=WEB)
    except subprocess.CalledProcessError:
        print(
            "E2E failed or Playwright not installed. "
            "Run: cd web && npm init playwright@latest",
            file=sys.stderr,
        )
        sys.exit(1)

    print("E2E smoke OK.")


if __name__ == "__main__":
    main()
