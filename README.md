# Previsão mensal de precipitação — América do Sul

Projeto preparado para Windows e VS Code. O CSV de referência do usuário tem pontuação pública informada de **1,69874**. A branch `lucasteste-1` contém uma versão oceânica do modelo; seus scripts foram recuperados em `lucasteste1/`. O pipeline principal gera um candidato independente com opção de índices oceânicos. A integração GEOSS2S em `lucasteste1/` foi reconstruída a partir da fonte pública da Columbia.

**Candidato gerado nesta máquina:** [outputs/submission_candidate_2023_2024.csv](outputs/submission_candidate_2023_2024.csv). A validação histórica escolheu 50% do modelo oceânico e 50% da variante GEOSS2S. O arquivo passou na auditoria de formato e contém 1.885.464 previsões para 2023–2024. Veja [STATUS.md](STATUS.md) e [outputs/nmme_gate.json](outputs/nmme_gate.json) para métricas. A pontuação Kaggle de 2024 ainda é desconhecida.

## Abrir e executar

Abra esta pasta no VS Code e selecione `.venv/Scripts/python.exe` em **Python: Select Interpreter**. No terminal PowerShell, a partir desta pasta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe download_data.py --login
```

O download exige acesso à competição Kaggle e aceite das regras. Com `--login`, o token é solicitado no terminal e usado para baixar no mesmo processo. A versão instalada do `kagglehub` não persiste `login()` entre processos; executar `kagglehub.login()` sozinho não autentica o comando posterior. Não coloque tokens no código nem envie credenciais no chat. Alternativamente, extraia os arquivos oficiais em `data/`. O programa localiza também uma subpasta que contenha `treino_tp_alvo.nc`.

Arquivos necessários: `treino_tp_alvo.nc`, nove `treino_<variavel>.nc`, `teste_features.nc` e `sample_submission.csv`. As nove variáveis estão em `ATMOS` no `pipeline.py`. `treino_tp.nc` não é necessário neste candidato.

## Validar antes de gerar

```powershell
.\.venv\Scripts\python.exe -m unittest test_pipeline -v
.\.venv\Scripts\python.exe inspect_data.py
.\.venv\Scripts\python.exe pipeline.py validate
```

Para avaliar a variante com índices oceânicos, baixe primeiro o snapshot NOAA e rode uma validação separada:

```powershell
.\.venv\Scripts\python.exe download_indices.py
.\.venv\Scripts\python.exe pipeline.py validate --ocean --output outputs/ocean
```

SOI e Niño 1+2, Niño 3 e Niño 4 entram apenas com defasagens de 1, 2 e 3 meses. As séries são baixadas de URLs oficiais NOAA/PSL e o snapshot fica em `data/indices/` com hash em `manifest.json`. São observações mensais retrospectivas; a data de publicação de cada valor não foi verificada. Use esta variante só se a regra de disponibilidade temporal da competição permitir essas observações. Para gerar o respectivo CSV, use `pipeline.py predict --ocean --output outputs/ocean --validation outputs/ocean/validation.json` e acrescente `--reference` apontando ao CSV anterior.

São três blocos sem sobreposição: **2015–2016, 2019–2020 e 2021–2022**. Cada treino utiliza até 30 anos anteriores ao bloco. A climatologia é calculada exclusivamente com alvos do treino. O último alvo desconhecido de janeiro/2023 é excluído. O relatório mostra RMSE global, mensal e do segundo ano — útil para avaliar comportamento semelhante ao horizonte de 2024. Isso não mede diretamente a acurácia de 2024.

A grade `--stride 8` serve para triagem e economiza RAM. Para avaliar uma grade mais densa, repita com `--stride 4 --output outputs/stride4`. Não compare métricas calculadas em grades diferentes como se fossem equivalentes. Defaults: 224 folhas, 700 árvores, taxa 0,025 e quatro threads. Número de árvores fixo evita escolher iterações olhando o bloco externo de validação.

O modelo aprende **alvo − climatologia**, com latitude/longitude, sazonalidade, campos atmosféricos de T−1, T−2 e T−3 e produtos umidade × vento. Soma-se a climatologia na previsão e limita-se o resultado a zero. Não usa precipitação congelada como se fosse observação mensal atualizada. Não usa alvos 2023–2024 nem dados externos.

## Gerar candidato

Somente após validação, usando os mesmos parâmetros:

```powershell
.\.venv\Scripts\python.exe pipeline.py predict --reference "C:\Users\Acer\Downloads\submission_ocean_2023_2024.csv"
```

O programa exige ganho sobre climatologia em todos os três blocos e em seus segundos anos. Isso é uma condição mínima, **não comprova ganho sobre o modelo ocean nem sobre o placar Kaggle**. Se falhar, o fluxo interrompe a geração. Não há envio automático ao Kaggle.

Resultados em `outputs/candidate/`:

- `fold_*.json` e `fold_*.npz`: métricas e previsões de validação;
- `validation.json`: configuração e resultados;
- `model.txt` e `climatology.npy`: modelo final e climatologia na grade completa;
- `submission_candidate.csv`: previsões ordenadas exatamente como o sample;
- `submission_audit.json`: IDs, finitude, não negatividade e diferenças para a referência;
- `manifest.json`: parâmetros, versões, hashes e limite temporal do treino.

Diferença entre dois CSVs não é erro contra a verdade. Os pesos de blend do relatório são exploratórios; selecionar o melhor peso nesses mesmos folds não fornece uma avaliação independente. O candidato publicado pelo comando usa apenas o modelo residual, sem ajuste arbitrário específico para 2024.

## Conferir a submissão anterior

```powershell
.\.venv\Scripts\python.exe audit_submission.py "C:\Users\Acer\Downloads\submission_ocean_2023_2024.csv" --output outputs/reference_audit.json
```

SHA-256 esperado: `2B5084B0BB00131948E1CBA3720B7E96774B0F5B10D96119646C0508FDD8782B`.

## O que falta para evoluir o melhor modelo existente

Os arquivos `run_temporal_experiments.py`, `ocean_indices.py`, `generate_ocean_submission.py` e resultados históricos foram encontrados na branch `lucasteste-1` (commit `45831cc03adf882cef0a1c4f8c118623787ba441`) e copiados para `lucasteste1/`. O parser de índices foi adaptado para o snapshot NOAA/PSL baixado neste computador; os arquivos originais usados na submissão de 1,69874 não estão disponíveis. Portanto, um novo CSV desse script pode diferir do anterior. `reference_github/` conserva a versão da `main`.

Para reproduzir essa versão oceânica depois de obter os dados oficiais:

```powershell
.\run_ocean_repro.ps1 -Mode validate
.\run_ocean_repro.ps1 -Mode predict
```

O primeiro comando executa os folds 2015–2016 completos, 2021–2022 e 2022 em grade `stride=8`. O fold completo de 2016 ajuda a testar o ano posterior a um El Niño forte, mais relevante para 2024. O segundo reajusta o modelo em `stride=4`, gera `outputs/submission_ocean_2023_2024.csv` e compara as previsões ao CSV vencedor preservado em Downloads. Faça a comparação antes de considerar uma submissão, pois os índices atuais podem divergir do snapshot antigo.

Para testar GEOSS2S sem o computador anterior, crie o cache da fonte [Columbia NMME](https://forecast.ccsr.columbia.edu/data/NMME/NASA-GMAO/GEOSS2S/) e compare os mesmos folds com os do modelo oceânico:

```powershell
.\.venv\Scripts\python.exe lucasteste1/download_geoss2s.py
.\run_ocean_repro.ps1 -Mode validate -NMME
.\run_ocean_repro.ps1 -Mode predict -NMME
```

O cache seleciona somente a América do Sul a 2°, média dos membros GEOSS2S, lead 1. Para cada alvo T, a inicialização é T−1 e a variável `target` fornecida pelo servidor é conferida contra T. `pr` está em mm/dia e `tos` em °C; nenhuma precipitação observada do alvo é consultada. Na grade completa, as previsões de 2° são interpoladas; bordas seguem o valor da célula válida mais próxima. Para pixels sem SST oceânica, `tos_local` recebe o marcador `-999`, e a média de SST do Pacífico equatorial oriental é incluída separadamente. O cache e os metadados ficam em `data/external/`. Resultados precisam ser comparados em mais de um bloco antes de usar o CSV.

O comando de validação NMME roda também a versão oceânica sem NMME nos mesmos folds e grava `outputs/nmme_gate.json`. São avaliados quatro pesos predefinidos para NMME (25%, 50%, 75% e 100%); somente um peso que reduza o RMSE em todos os folds e em seus segundos anos pode gerar `outputs/submission_candidate_2023_2024.csv`. O peso elegível com menor RMSE agrupado nos blocos independentes 2015–2016 e 2021–2022 é escolhido. Essa escolha usa os próprios folds históricos e não garante ganho no placar privado.

Segundo o histórico fornecido, GEOSS2S e TSM prevista são as melhorias locais mais promissoras já testadas. A implementação nova verifica inicialização T−1, mês válido T, unidades, grade, disponibilidade histórica e ausência de precipitação observada do alvo. A validação com os dados oficiais foi concluída em 22/09/2026; veja `outputs/nmme_gate.json`. Não foi presumido que o cache novo reproduz exatamente o cache do computador anterior.

O script antigo `train_residual_lightgbm.py` calcula climatologia antes de dividir sua validação interna; isso contamina essa avaliação. O backtest separado usa climatologia do treino. Essa observação sobre o código público **não permite concluir que o RMSE 1,8162 informado para a versão mais recente esteja contaminado**.

## Fontes

- [Repositório fornecido](https://github.com/Drslukas/TESTEdesafiodogoverno)
- [Competição](https://www.kaggle.com/competitions/previsao-climatica-de-precipitacao-sobre-a-america-do-sul)
- [Download oficial com kagglehub](https://github.com/Kaggle/kagglehub)
- Handoff e CSV fornecidos pelo usuário, preservados como contexto; a validação nova está em `outputs/nmme_gate.json`.
