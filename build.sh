#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements.txt

mkdir -p models

if [[ ! -f "${YOLO_MODEL_PATH:-models/ppe-helmet-vest-best.pt}" ]]; then
  if [[ -z "${MODEL_DOWNLOAD_URL:-}" ]]; then
    echo "MODEL_DOWNLOAD_URL is required when the model file is not present."
    exit 1
  fi

  curl -L "${MODEL_DOWNLOAD_URL}" -o "${YOLO_MODEL_PATH:-models/ppe-helmet-vest-best.pt}"
fi

