# Inicia a validação depois que os downloads estiverem completos.
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
New-Item -ItemType Directory -Path outputs -Force | Out-Null
Start-Transcript -Path outputs\automatic_run.log -Append | Out-Null
try {
    $required = @('treino_tp.nc', 'treino_tp_alvo.nc', 'treino_t2.nc',
                  'treino_cloud_cover.nc', 'treino_surface_pressure.nc',
                  'treino_shum_850.nc', 'treino_rel_hum_850.nc',
                  'treino_temperature_850.nc', 'treino_geopotential_850.nc',
                  'treino_u_850.nc', 'treino_v_850.nc',
                  'teste_features.nc', 'sample_submission.csv')
    $ready = $false
    for ($attempt = 0; $attempt -lt 180; $attempt++) {
        $target = Get-ChildItem -LiteralPath data -Filter 'treino_tp_alvo.nc' -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -ne $target) {
            $folder = $target.DirectoryName
            $missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $folder $_)) })
            $nmme = Get-Item -LiteralPath data\external\geoss2s_lead1_sa.npz -ErrorAction SilentlyContinue
            if ($missing.Count -eq 0 -and $null -ne $nmme -and $nmme.Length -gt 500000) {
                # Exige arquivos estáveis por um intervalo antes de abrir NetCDF.
                $sizes = @($required | ForEach-Object { (Get-Item -LiteralPath (Join-Path $folder $_)).Length })
                Start-Sleep -Seconds 60
                $sizesAgain = @($required | ForEach-Object { (Get-Item -LiteralPath (Join-Path $folder $_)).Length })
                $ready = (Compare-Object $sizes $sizesAgain).Count -eq 0
                if ($ready) { break }
            }
        }
        Start-Sleep -Seconds 60
    }
    if (-not $ready) { throw 'Dados completos não apareceram em três horas.' }
    $python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    & $python inspect_data.py
    if ($LASTEXITCODE -ne 0) { throw 'Inspeção oficial falhou.' }
    & (Join-Path $PSScriptRoot 'run_ocean_repro.ps1') -Mode validate -NMME
    if ($LASTEXITCODE -ne 0) { throw 'Validação oceânica falhou.' }
    $gate = Get-Content -LiteralPath outputs\nmme_gate.json -Raw | ConvertFrom-Json
    if ($gate.passed) {
        & (Join-Path $PSScriptRoot 'run_ocean_repro.ps1') -Mode predict -NMME
        if ($LASTEXITCODE -ne 0) { throw 'Geração NMME falhou.' }
        'candidate_ready' | Set-Content -LiteralPath outputs\automatic_run_state.txt
    } else {
        'nmme_not_improved' | Set-Content -LiteralPath outputs\automatic_run_state.txt
    }
} catch {
    ('failed: ' + $_.Exception.Message) | Set-Content -LiteralPath outputs\automatic_run_state.txt
    Write-Error $_
} finally {
    Stop-Transcript | Out-Null
}
