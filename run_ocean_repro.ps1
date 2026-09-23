param([ValidateSet('validate','predict')][string]$Mode = 'validate', [switch]$NMME)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$TaskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $TaskPython)) { throw 'Ambiente virtual ausente.' }
if (-not (Test-Path -LiteralPath 'data\indices\manifest.json')) { throw 'Baixe os índices: python download_indices.py' }
if ($Mode -eq 'validate') {
    $variants = if ($NMME) { @('base','nmme') } else { @('base') }
    foreach ($Variant in $variants) {
        foreach ($Fold in @('2015full','2021','2022')) {
            $arguments = @('lucasteste1\run_temporal_experiments.py', '--fold', $Fold, '--experiments', 'E00', '--stride', '8', '--leaves', '224', '--rounds', '700', '--lr', '0.025', '--atmosphere-history', 'three', '--train-years', '30', '--ocean-indices')
            if ($Variant -eq 'nmme') { $arguments += '--nmme-geoss2s' }
            & $TaskPython @arguments
            if ($LASTEXITCODE -ne 0) { throw "Fold $Fold ($Variant) falhou." }
        }
    }
    if ($NMME) {
        & $TaskPython 'lucasteste1\evaluate_ensemble.py'
        if ($LASTEXITCODE -ne 0) { throw 'Comparação de modelos falhou.' }
        $gate = Get-Content -LiteralPath outputs\nmme_gate.json -Raw | ConvertFrom-Json
        if (-not $gate.passed) { Write-Warning 'GEOSS2S não melhorou todos os folds; não gerar candidato NMME ainda.' }
    }
    Write-Host 'Resultados em lucasteste1/results/. Compare com os números históricos antes de gerar.'
} else {
    if ($NMME) {
        if (-not (Test-Path -LiteralPath outputs\nmme_gate.json)) { throw 'Valide NMME antes de gerar: .\run_ocean_repro.ps1 -Mode validate -NMME' }
        $gate = Get-Content -LiteralPath outputs\nmme_gate.json -Raw | ConvertFrom-Json
        if (-not $gate.passed) { throw 'NMME não superou o modelo oceânico nos três folds.' }
    }
    if ($NMME -and $gate.selected_weight -lt 1) {
        & $TaskPython 'lucasteste1\generate_ocean_submission.py'
        if ($LASTEXITCODE -ne 0) { throw 'Geração oceânica falhou.' }
    }
    if ($NMME) {
        & $TaskPython 'lucasteste1\generate_ocean_submission.py' --nmme-geoss2s
        if ($LASTEXITCODE -ne 0) { throw 'Geração NMME falhou.' }
        & $TaskPython blend_submissions.py
        if ($LASTEXITCODE -ne 0) { throw 'Blend/auditoria falhou.' }
    } else {
        & $TaskPython 'lucasteste1\generate_ocean_submission.py'
        if ($LASTEXITCODE -ne 0) { throw 'Geração oceânica falhou.' }
        & $TaskPython audit_submission.py 'outputs\submission_ocean_2023_2024.csv' --reference 'C:\Users\Acer\Downloads\submission_ocean_2023_2024.csv' --output 'outputs\ocean_repro_audit.json'
        if ($LASTEXITCODE -ne 0) { throw 'Auditoria do CSV falhou.' }
    }
}
