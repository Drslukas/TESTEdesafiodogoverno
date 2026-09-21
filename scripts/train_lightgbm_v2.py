"""
LightGBM v2: modelo ciente de `lag_meses`, treinado com `tp` defasado
aleatoriamente (1-24 meses) pra imitar a degradação real do teste, e
validado nos dois episódios de El Niño (1997-98, 2015-16) reproduzindo o
mecanismo exato do teste (tp congelado + lag crescente) - não mais o `tp`
sempre fresco que usamos na v1 e que gerou uma validação otimista demais
(1.94 interno vs 2.2287 real no Kaggle).

Compara TRÊS números pra cada bloco de validação:
  - climatologia (sempre foi o "chute ingênuo", sem mudança)
  - LightGBM v1 (o que já submetemos - tp sempre fresco, sem lag_meses)
  - LightGBM v2 (novo - consciente de lag)

Uso:
    .venv/bin/python scripts/train_lightgbm_v2.py
"""

import numpy as np
import lightgbm as lgb
import pandas as pd

from features_lagged import build_training_table_lagged, build_realistic_validation_block, load_raw_strided
from baseline_climatology import rmse, build_climatology, target_calendar_month
from train_lightgbm import FEATURES as FEATURES_V1

FEATURES_V2 = FEATURES_V1 + ["lag_meses"]
TARGET = "target"

PARAMS = dict(
    objective="regression", metric="rmse", max_bin=127, verbosity=-1, num_threads=8,
    num_leaves=63, learning_rate=0.03, min_data_in_leaf=100,
    feature_fraction=0.7, bagging_fraction=0.7, bagging_freq=1,
)

BLOCK_1 = ("1997-05-01", "1998-04-01")
BLOCK_2 = ("2015-01-01", "2016-05-01")


def climatology_baseline_for_block(arrays, lat_s, lon_s, time_full, first_target, last_target, exclude_years):
    """climatologia (média histórica por ponto/mês), excluindo os anos do
    próprio bloco, pra comparar como antes."""
    time_index = {t: i for i, t in enumerate(time_full)}
    years = np.array([t.year for t in time_full[:-1]])
    months = np.array([t.month for t in time_full[:-1]])
    mask = ~np.isin(years, list(exclude_years))
    clim = {}
    for m in range(1, 13):
        sel = mask & (months == m)
        clim[m] = arrays["tp"][:-1][sel].mean(axis=0)

    cur = pd.Timestamp(first_target)
    last = pd.Timestamp(last_target)
    preds, trues = [], []
    while cur <= last:
        t_idx = time_index[cur - pd.DateOffset(months=1)]
        tmonth = cur.month
        preds.append(clim[tmonth])
        trues.append(arrays["target"][t_idx])
        cur += pd.DateOffset(months=1)
    return np.stack(preds), np.stack(trues)


def main():
    exclude_ranges = [(pd.Timestamp(s), pd.Timestamp(e)) for s, e in (BLOCK_1, BLOCK_2)]

    df, arrays, lat_s, lon_s, time_full = build_training_table_lagged(exclude_target_month_ranges=exclude_ranges, seed=0)
    df = df.dropna(subset=["oni"]).reset_index(drop=True)
    print(f"{len(df):,} linhas de treino após remover NaN de ONI\n")

    # separa um pedaço cronológico pra early stopping (últimos anos do treino que sobraram)
    es_mask = (df["target_year"] >= 2011) & (df["target_year"] <= 2014)
    core_mask = ~es_mask

    train_set = lgb.Dataset(df.loc[core_mask, FEATURES_V2], label=df.loc[core_mask, TARGET])
    es_set = lgb.Dataset(df.loc[es_mask, FEATURES_V2], label=df.loc[es_mask, TARGET], reference=train_set)

    model_v2 = lgb.train(
        PARAMS, train_set, num_boost_round=6000,
        valid_sets=[es_set],
        callbacks=[lgb.early_stopping(stopping_rounds=80, verbose=False), lgb.log_evaluation(period=0)],
    )
    print(f"\nModelo v2 treinado - best_iteration={model_v2.best_iteration}\n")
    model_v2.save_model("../outputs/lgb_model_v2.txt")

    print("=== Validação realista (tp congelado + lag crescente, igual ao teste de verdade) ===\n")
    for name, (first, last) in (("Bloco 1997-98", BLOCK_1), ("Bloco 2015-16", BLOCK_2)):
        val_df = build_realistic_validation_block(arrays, lat_s, lon_s, time_full, first, last)

        preds_v2 = np.clip(model_v2.predict(val_df[FEATURES_V2], num_iteration=model_v2.best_iteration), 0, None)
        score_v2 = rmse(preds_v2, val_df[TARGET].values)

        clim_preds, clim_trues = climatology_baseline_for_block(
            arrays, lat_s, lon_s, time_full, first, last, exclude_years={1997, 1998, 2015, 2016})
        score_clim = rmse(clim_preds, clim_trues)

        print(f"{name}:")
        print(f"  climatologia (sem lag, sempre foi assim): {score_clim:.4f}")
        print(f"  LightGBM v2 (lag-aware, validação realista): {score_v2:.4f}")
        print()


if __name__ == "__main__":
    main()
