$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

$EnvFile = Join-Path $PSScriptRoot ".env"
if (-not (Test-Path $EnvFile)) {
    throw ".env file not found: $EnvFile"
}

Get-Content $EnvFile | ForEach-Object {
    $Line = $_.Trim()
    if ($Line -ne "" -and -not $Line.StartsWith("#")) {
        $Parts = $Line.Split("=", 2)
        if ($Parts.Count -eq 2) {
            [Environment]::SetEnvironmentVariable($Parts[0].Trim(), $Parts[1].Trim(), "Process")
        }
    }
}

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
