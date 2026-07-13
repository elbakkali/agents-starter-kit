#!/usr/bin/env bash
# Install the Agents Starter Kit into an existing repository.
#
# Usage:
#   ./scripts/install.sh /path/to/target-repo
#   ./scripts/install.sh .

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET="${1:-.}"
TARGET="$(cd "${TARGET}" && pwd)"

if [[ ! -d "${TARGET}/.git" && ! -f "${TARGET}/.git" ]]; then
  echo "Warning: ${TARGET} does not look like a git repository."
  read -r -p "Continue anyway? [y/N] " reply
  [[ "${reply}" =~ ^[Yy]$ ]] || exit 1
fi

echo "Installing Agents Starter Kit from ${KIT_ROOT} into ${TARGET}"

copy_file() {
  local src="$1"
  local dest="$2"
  if [[ -f "${dest}" ]]; then
    echo "  skip (exists): ${dest}"
  else
    mkdir -p "$(dirname "${dest}")"
    cp "${src}" "${dest}"
    echo "  copied: ${dest}"
  fi
}

copy_dir_merge() {
  local src="$1"
  local dest="$2"
  mkdir -p "${dest}"
  if command -v rsync &>/dev/null; then
    rsync -a "${src}/" "${dest}/"
  else
    cp -r "${src}/." "${dest}/"
  fi
  echo "  merged: ${dest}/"
}

# Core agent files
copy_file "${KIT_ROOT}/AGENTS.md" "${TARGET}/AGENTS.md"
copy_file "${KIT_ROOT}/api/AGENTS.md" "${TARGET}/api/AGENTS.md"
copy_file "${KIT_ROOT}/web/AGENTS.md" "${TARGET}/web/AGENTS.md"
copy_file "${KIT_ROOT}/app/AGENTS.md" "${TARGET}/app/AGENTS.md"

# Cursor rules (source of truth for scoped rules)
copy_dir_merge "${KIT_ROOT}/.cursor/rules" "${TARGET}/.cursor/rules"
copy_dir_merge "${KIT_ROOT}/.cursor/skills" "${TARGET}/.cursor/skills"
copy_file "${KIT_ROOT}/.cursor/hooks.json" "${TARGET}/.cursor/hooks.json"
copy_dir_merge "${KIT_ROOT}/.cursor/hooks" "${TARGET}/.cursor/hooks"
chmod +x "${TARGET}/.cursor/hooks/"*.sh 2>/dev/null || true

# GitHub (workflows, templates, dependabot — merge without overwriting existing)
copy_dir_merge "${KIT_ROOT}/.github/workflows" "${TARGET}/.github/workflows"
copy_dir_merge "${KIT_ROOT}/.github/ISSUE_TEMPLATE" "${TARGET}/.github/ISSUE_TEMPLATE"
copy_file "${KIT_ROOT}/.github/pull_request_template.md" "${TARGET}/.github/pull_request_template.md"
copy_file "${KIT_ROOT}/.github/dependabot.yml" "${TARGET}/.github/dependabot.yml"

# Cross-editor adapters
copy_dir_merge "${KIT_ROOT}/.claude" "${TARGET}/.claude"
copy_dir_merge "${KIT_ROOT}/.github" "${TARGET}/.github"
copy_file "${KIT_ROOT}/.aider.conf.yml" "${TARGET}/.aider.conf.yml"
copy_dir_merge "${KIT_ROOT}/.gemini" "${TARGET}/.gemini"
copy_file "${KIT_ROOT}/.windsurfrules" "${TARGET}/.windsurfrules"

# Docker
copy_file "${KIT_ROOT}/docker-compose.yml" "${TARGET}/docker-compose.yml"
copy_file "${KIT_ROOT}/docker-compose.prod.yml" "${TARGET}/docker-compose.prod.yml"
copy_file "${KIT_ROOT}/.env.docker.example" "${TARGET}/.env.docker.example"
copy_file "${KIT_ROOT}/.dockerignore" "${TARGET}/.dockerignore"
copy_dir_merge "${KIT_ROOT}/docker" "${TARGET}/docker"
copy_file "${KIT_ROOT}/api/Dockerfile" "${TARGET}/api/Dockerfile"
copy_file "${KIT_ROOT}/web/Dockerfile" "${TARGET}/web/Dockerfile"
copy_dir_merge "${KIT_ROOT}/api/docker" "${TARGET}/api/docker"

# Scripts and devkit
copy_dir_merge "${KIT_ROOT}/scripts" "${TARGET}/scripts"
chmod +x "${TARGET}/scripts/install.sh" "${TARGET}/scripts/devkit.py" 2>/dev/null || true

# Documentation
copy_dir_merge "${KIT_ROOT}/docs/templates" "${TARGET}/docs/templates"
copy_dir_merge "${KIT_ROOT}/docs/technical" "${TARGET}/docs/technical"
copy_dir_merge "${KIT_ROOT}/docs/product" "${TARGET}/docs/product"

# Static analysis stubs
copy_file "${KIT_ROOT}/api/phpstan.neon.dist" "${TARGET}/api/phpstan.neon.dist"
copy_file "${KIT_ROOT}/web/tsconfig.strict-notes.md" "${TARGET}/web/tsconfig.strict-notes.md"

# Gitignore entries (append handoff path if .gitignore exists)
if [[ -f "${TARGET}/.gitignore" ]]; then
  grep -q 'docs/technical/HANDOFF.md' "${TARGET}/.gitignore" 2>/dev/null || echo "docs/technical/HANDOFF.md" >> "${TARGET}/.gitignore"
else
  copy_file "${KIT_ROOT}/.gitignore" "${TARGET}/.gitignore"
fi

# CLAUDE.md symlink
if [[ -L "${TARGET}/CLAUDE.md" ]]; then
  echo "  skip (symlink exists): CLAUDE.md"
elif [[ -f "${TARGET}/CLAUDE.md" ]]; then
  echo "  skip (file exists): CLAUDE.md"
else
  ln -s AGENTS.md "${TARGET}/CLAUDE.md"
  echo "  linked: CLAUDE.md -> AGENTS.md"
fi

# Regenerate adapters from .mdc (ensures target matches kit rules)
if command -v python3 &>/dev/null; then
  echo "  syncing cross-editor adapters..."
  (cd "${TARGET}" && python3 -m scripts.tasks.sync_adapters)
else
  echo "  warning: python3 not found — run sync_adapters manually after install"
fi

echo ""
echo "Done. Next steps:"
echo "  1. cp .env.docker.example .env"
echo "  2. Edit docs/product/overview.md and docs/technical/architecture.md"
echo "  3. python3 scripts/devkit.py"
