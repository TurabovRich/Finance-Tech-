#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/backend"

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp -n .env.example .env 2>/dev/null || true

echo "Backend ready. Run: docker compose up -d db && alembic upgrade head && uvicorn app.main:app --reload"
