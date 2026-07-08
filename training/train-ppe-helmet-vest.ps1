param(
    [string]$Model = "models\yolo9e.pt",
    [int]$Epochs = 50,
    [int]$ImageSize = 640,
    [int]$Batch = -1,
    [string]$Device = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

$env:YOLO_CONFIG_DIR = Join-Path $ProjectRoot ".runtime\ultralytics"
$env:MPLCONFIGDIR = Join-Path $ProjectRoot ".runtime\matplotlib"

$DataYaml = Join-Path $PSScriptRoot "ppe-helmet-vest-data.yaml"
$YoloExe = Join-Path $ProjectRoot ".venv\Scripts\yolo.exe"

$TrainArgs = @(
    "detect",
    "train",
    "model=$Model",
    "data=$DataYaml",
    "epochs=$Epochs",
    "imgsz=$ImageSize",
    "project=runs",
    "name=ppe-helmet-vest"
)

if ($Batch -gt 0) {
    $TrainArgs += "batch=$Batch"
}

if ($Device -ne "") {
    $TrainArgs += "device=$Device"
}

& $YoloExe @TrainArgs
