#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

source ~/miniforge3/etc/profile.d/conda.sh
conda activate ai

export YOLO_MODEL_PATH="${YOLO_MODEL_PATH:-models/ppe-helmet-vest-best.pt}"
export YOLO_CONFIDENCE="${YOLO_CONFIDENCE:-0.25}"
export AI_SERVER_BASE_URL="${AI_SERVER_BASE_URL:-http://165.246.170.53:8000}"
export BACKEND_CALLBACK_ENABLED="${BACKEND_CALLBACK_ENABLED:-true}"
export BACKEND_BASE_URL="${BACKEND_BASE_URL:-https://logisquare.p-e.kr}"
export BACKEND_REQUEST_TIMEOUT="${BACKEND_REQUEST_TIMEOUT:-15.0}"
export YOLO_CONFIG_DIR="${YOLO_CONFIG_DIR:-.runtime/ultralytics}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-.runtime/matplotlib}"

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
