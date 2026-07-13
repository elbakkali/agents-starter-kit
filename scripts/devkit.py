#!/usr/bin/env python3
"""
Interactive project devkit — arrow-key navigation.

  ↑/↓   Navigate within the focused column
  ←/→   Switch between Categories and Actions
  Enter Run selected action
  q     Quit

Run from project root: python3 scripts/devkit.py
"""

from __future__ import annotations

import curses
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORIES: dict[str, list[tuple[str, str]]] = {
    "Docker": [
        ("Start stack", "scripts.tasks.docker_up"),
        ("Stop stack", "scripts.tasks.docker_down"),
        ("Rebuild services", "scripts.tasks.docker_rebuild"),
        ("Tail logs (all)", "scripts.tasks.docker_logs"),
        ("Shell: API", "scripts.tasks.docker_shell_api"),
        ("Shell: web", "scripts.tasks.docker_shell_web"),
    ],
    "Development": [
        ("Install dependencies", "scripts.tasks.install_deps"),
        ("Run all tests", "scripts.tasks.test_all"),
        ("Run all linters", "scripts.tasks.lint_all"),
        ("Static analysis", "scripts.tasks.static_analysis"),
        ("Scaffold feature spec", "scripts.tasks.scaffold_feature"),
        ("Scaffold API endpoint", "scripts.tasks.scaffold_api_endpoint"),
        ("Scaffold web page", "scripts.tasks.scaffold_web_page"),
        ("Install deps (native)", "scripts.tasks.install_deps native"),
        ("Tests (native)", "scripts.tasks.test_all native"),
        ("Lint (native)", "scripts.tasks.lint_all native"),
        ("Static analysis (native)", "scripts.tasks.static_analysis native"),
    ],
    "Documentation": [
        ("Check doc structure & links", "scripts.tasks.docs_check"),
        ("Sync editor adapters", "scripts.tasks.sync_adapters"),
        ("Open technical docs index", "__open__:docs/technical/README.md"),
        ("Open product docs index", "__open__:docs/product/README.md"),
    ],
    "Quality": [
        ("Check orphans & junk", "scripts.tasks.check_orphans"),
        ("Security check", "scripts.tasks.security_check"),
        ("Validate AGENTS.md", "scripts.tasks.validate_agents"),
        ("Adapter sync check", "scripts.tasks.sync_adapters --check"),
        ("Post-feature review", "scripts.tasks.feature_review"),
    ],
}

CATEGORY_NAMES = list(CATEGORIES.keys())


def run_action(spec: str) -> tuple[int, str]:
    if spec.startswith("__open__:"):
        target = ROOT / spec.removeprefix("__open__:")
        return 0, f"Open in editor: {target}"

    parts = spec.split()
    module = parts[0]
    args = parts[1:]
    cmd = [sys.executable, "-m", module, *args]
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode, " ".join(cmd)


def draw_menu(
    stdscr: curses.window,
    cat_idx: int,
    act_idx: int,
    focus: str,
    message: str,
) -> None:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    if height < 10 or width < 50:
        stdscr.addstr(0, 0, "Terminal too small. Resize and retry.")
        stdscr.refresh()
        return

    title = " Project Devkit "
    stdscr.addstr(0, 0, title, curses.A_BOLD | curses.A_REVERSE)
    stdscr.addstr(1, 0, "←/→ switch column   ↑/↓ navigate   Enter run   q quit")

    cat_x, act_x = 2, 22
    stdscr.addstr(3, cat_x, "Categories", curses.A_UNDERLINE)
    stdscr.addstr(3, act_x, "Actions", curses.A_UNDERLINE)

    for i, name in enumerate(CATEGORY_NAMES):
        y = 5 + i
        if y >= height - 4:
            break
        attr = curses.A_REVERSE if focus == "cat" and i == cat_idx else curses.A_NORMAL
        stdscr.addstr(y, cat_x, f" {name} ", attr)

    actions = CATEGORIES[CATEGORY_NAMES[cat_idx]]
    for i, (label, _) in enumerate(actions):
        y = 5 + i
        if y >= height - 4:
            break
        attr = curses.A_REVERSE if focus == "act" and i == act_idx else curses.A_NORMAL
        label = label[: width - act_x - 4]
        stdscr.addstr(y, act_x, f" {label} ", attr)

    if message:
        msg_y = height - 3
        for line in message.split("\n")[:2]:
            if msg_y < height:
                stdscr.addstr(msg_y, 0, line[: width - 1])
                msg_y += 1

    stdscr.refresh()


def main_curses(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)

    cat_idx = 0
    act_idx = 0
    focus = "cat"
    message = ""

    while True:
        draw_menu(stdscr, cat_idx, act_idx, focus, message)
        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break

        actions = CATEGORIES[CATEGORY_NAMES[cat_idx]]

        if key == curses.KEY_LEFT:
            focus = "cat"
        elif key == curses.KEY_RIGHT:
            focus = "act"
        elif key == curses.KEY_UP:
            if focus == "cat":
                cat_idx = (cat_idx - 1) % len(CATEGORY_NAMES)
                act_idx = min(act_idx, len(CATEGORIES[CATEGORY_NAMES[cat_idx]]) - 1)
            else:
                act_idx = (act_idx - 1) % len(actions)
        elif key == curses.KEY_DOWN:
            if focus == "cat":
                cat_idx = (cat_idx + 1) % len(CATEGORY_NAMES)
                act_idx = min(act_idx, len(CATEGORIES[CATEGORY_NAMES[cat_idx]]) - 1)
            else:
                act_idx = (act_idx + 1) % len(actions)
        elif key in (curses.KEY_ENTER, 10, 13):
            _, spec = actions[act_idx]
            curses.endwin()
            code, desc = run_action(spec)
            if spec.startswith("__open__:"):
                print(desc)
            elif code == 0:
                print(f"\nDone: {desc}")
            else:
                print(f"\nFailed ({code}): {desc}")
            input("\nPress Enter to return to menu...")
            stdscr = curses.initscr()
            curses.cbreak()
            stdscr.keypad(True)
            curses.noecho()
            message = "Last run finished." if code == 0 else f"Last run failed (exit {code})."


def main() -> None:
    if not (ROOT / "docker-compose.yml").exists():
        print("Run from project root (docker-compose.yml not found).", file=sys.stderr)
        sys.exit(1)
    curses.wrapper(main_curses)


if __name__ == "__main__":
    main()
