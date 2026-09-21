# Estado do projeto — Desafio WORCAP 2026 (precipitação AmSul)

Contexto completo: `docs/DESAFIO_KAGGLE_OVERVIEW.md` (regras/dados/métrica) e
`docs/palestra 01.md` / `palestra 02.md` (contexto de domínio).

## O que já foi feito

1. **Inspeção dos dados** (`scripts/inspect_data.py`) — confirmou grade
   301x261, 996 meses de treino, unidades reais de cada variável (ver
   `data_inspection_report.txt`).
2. **Baseline de climatologia** (`scripts/baseline_climatology.py`) — RMSE
   ~1.87 (validação 2016-2022) / ~2.12 (validação em anos de El Niño forte,
   proxy melhor do teste real).
3. **Descoberta central: ENSO (El Niño/La Niña) importa muito.** O índice
   ONI (`data/oni.ascii.txt`, baixado da NOAA) mostra que o período de
   avaliação real da competição (2023-2024) foi dominado por **El Niño
   forte** (ONI chegou a +1.99 em dez/2023), enquanto nossa janela de
   validação natural (2016-2022) foi dominada por **La Niña**. Isso muda
   completamente qual baseline é realista - ver `scripts/enso_bias_analysis.py`,
   `scripts/validate_el_nino_years.py` e os mapas em `outputs/figures/`.
4. **Modelo tabular LightGBM** (`scripts/train_lightgbm.py`,
   `scripts/tune_lightgbm.py`) — usa as 10 variáveis atmosféricas + lat/lon +
   sazonalidade + ONI, treinado numa subamostra espacial (`stride=4`, ~5000
   de 78561 pontos de grade) por limitação de RAM desta máquina (~2GB
   livres). Config tunada: `num_leaves=63, learning_rate=0.03,
   min_data_in_leaf=100, feature_fraction=0.7, bagging_fraction=0.7`.
5. **Primeira submissão real no Kaggle: RMSE = 2.22871, 37º lugar.** Líder
   está em 1.48895 - GAP GRANDE ainda a fechar.

## Tentativas de melhoria que NÃO deram resultado claro (importante não repetir sem mudar a abordagem)

- **`lag_meses` como feature + treino com `tp` defasado aleatoriamente**
  (`scripts/features_lagged.py`, `scripts/train_lightgbm_v2.py`) — a
  hipótese era que o `tp` desatualizado no teste real (`tp_ultima_obs`
  travado em dez/2022) explicava boa parte do gap. Testado com validação
  realista (tp congelado + lag crescente, replicando o mecanismo exato do
  teste) nos episódios de El Niño 1997-98 e 2015-16: resultado
  inconclusivo (+0.4% num bloco, -2.7% no outro). Não confirma a hipótese.
- **Aumentar resolução espacial (`stride=4` → `stride=3`)** — PIOROU em
  todas as métricas testadas (`scripts/train_stride3.py`). Hipótese: mais
  densidade de pontos aumenta a capacidade de overfitting espacial sem que
  a validação (cortada só por tempo/ano) detecte isso.

## Conclusão até aqui

O gap real (2.23 no Kaggle vs. ~1.9-1.97 nas nossas melhores validações
internas) provavelmente **não é resolvível só com tuning/features no
LightGBM tabular**. A hipótese mais forte agora: o modelo tabular trata cada
ponto de grade como uma linha solta (lat/lon são só números), sem captar
vizinhança espacial de verdade - e a própria doc do desafio (seção 10.3)
sugere que **CNN espacial** (tratando cada mês como "imagem" multicanal
301x261x10) é estruturalmente mais adequada a este problema.

## Próximo passo (no notebook, RTX 4050 + 16GB RAM)

1. Com mais RAM, treinar o LightGBM na grade completa (sem `stride`) pra
   isolar se a subamostragem espacial (não a resolução em si) era o
   problema.
2. Implementar uma CNN (tipo U-Net simples) que recebe o tensor
   `(301, 261, 10)` do mês M e prevê `(301, 261, 1)` de M+1 - usando a GPU.
   Ver seção 10.3-10.5 do `docs/DESAFIO_KAGGLE_OVERVIEW.md` pra arquiteturas
   sugeridas.
3. Manter a mesma disciplina de validação temporal usada até aqui (nunca
   split aleatório) e, se possível, validar também no proxy de El Niño
   forte (1997-98, 2015-16) com o mecanismo de `tp` congelado.

## Arquivos que NÃO estão no git (ver `.gitignore`)

- `data/` (dados brutos, ~2GB)
- `.venv/` (ambiente Python local)
- `outputs/*.csv`, `outputs/*.parquet`, `outputs/*.txt` (submissões, tabela
  de treino cacheada, modelos LightGBM salvos - grandes demais / fáceis de
  regerar rodando os scripts de novo)
- `graphify-out/` (grafo de conhecimento gerado pelo `/graphify` - também
  regenerável)

Pra recriar o ambiente: `python3 -m venv .venv && .venv/bin/pip install
xarray netCDF4 numpy pandas matplotlib lightgbm scikit-learn pyarrow`
