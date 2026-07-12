#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

source ~/miniforge3/etc/profile.d/conda.sh
conda activate ai

if [[ ! -f .env ]]; then
  echo ".env file not found: $(pwd)/.env"
  exit 1
fi

set -a
source .env
set +a

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
