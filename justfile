# Common commands — install just: https://github.com/casey/just
# List recipes: just --list

default:
    @just --list

devkit:
    python3 scripts/devkit.py

bootstrap:
    python3 -m scripts.tasks.bootstrap_project --yes

up:
    docker compose up -d --build

down:
    docker compose down

logs:
    docker compose logs -f

review:
    python3 -m scripts.tasks.feature_review

docs:
    python3 -m scripts.tasks.docs_check

sync:
    python3 -m scripts.tasks.sync_adapters

test:
    python3 -m scripts.tasks.test_all native

lint:
    python3 -m scripts.tasks.lint_all native

e2e:
    python3 -m scripts.tasks.e2e_smoke
