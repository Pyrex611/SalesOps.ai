#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Local environment initialized."
echo "Run backend with: source .venv/bin/activate && uvicorn app.main:app --app-dir backend --reload"
echo "Run frontend with: cd frontend && npm install && npm run dev"
