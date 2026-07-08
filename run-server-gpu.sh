#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

source ~/.bashrc
conda activate ai

export YOLO_MODEL_PATH="${YOLO_MODEL_PATH:-models/ppe-helmet-vest-best.pt}"
export YOLO_CONFIDENCE="${YOLO_CONFIDENCE:-0.25}"
export YOLO_CONFIG_DIR="${YOLO_CONFIG_DIR:-.runtime/ultralytics}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-.runtime/matplotlib}"

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
