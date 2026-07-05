$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

$env:YOLO_MODEL_PATH = "models\yolo9e.pt"
$env:YOLO_CONFIDENCE = "0.25"
$env:YOLO_CONFIG_DIR = Join-Path $PSScriptRoot ".runtime\ultralytics"
$env:MPLCONFIGDIR = Join-Path $PSScriptRoot ".runtime\matplotlib"

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
