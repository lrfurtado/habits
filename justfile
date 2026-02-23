set shell := ["bash", "-cu"]

export PYTHONPATH := "src"

default:
    @just --list

install:
    python -m pip install -r requirements.txt

dev-install:
    python -m pip install -r requirements-dev.txt

validate-config:
    python -m habits.main --no-prompt

test:
    pytest -q

run:
    python -m habits --config ui-config.example.yaml --schema ui-config.schema.yaml

notification-server:
    python -m habits.rpc.notification_server

export-daily:
    python -m habits.main --no-prompt --export daily

export-weekly:
    python -m habits.main --no-prompt --export weekly

format-check:
    python -m compileall src
