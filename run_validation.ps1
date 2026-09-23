param([string]$DataDir = "data")
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$TaskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $TaskPython)) { throw 'Crie o ambiente virtual conforme README.md.' }
& $TaskPython inspect_data.py --data $DataDir
if ($LASTEXITCODE -ne 0) { throw 'Inspeção dos dados falhou.' }
& $TaskPython pipeline.py validate --data $DataDir
if ($LASTEXITCODE -ne 0) { throw 'Validação falhou; consulte o erro acima.' }
Write-Host 'Validação concluída. Consulte outputs/candidate/validation.json antes de gerar o CSV.'
