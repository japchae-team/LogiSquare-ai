#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-models/yolo9e.pt}"
EPOCHS="${EPOCHS:-50}"
IMGSZ="${IMGSZ:-640}"
DEVICE="${DEVICE:-1}"
BATCH="${BATCH:-}"

cd "$(dirname "$0")/.."

ARGS=(
  detect
  train
  "model=${MODEL}"
  "data=training/ppe-helmet-vest-data.server.yaml"
  "epochs=${EPOCHS}"
  "imgsz=${IMGSZ}"
  "device=${DEVICE}"
  "project=runs"
  "name=ppe-helmet-vest"
)

if [[ -n "${BATCH}" ]]; then
  ARGS+=("batch=${BATCH}")
fi

yolo "${ARGS[@]}"
