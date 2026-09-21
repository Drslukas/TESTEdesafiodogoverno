"""
Testa se aumentar a resolução espacial (stride 4 -> 3, quase 2x mais pontos
de grade) melhora o modelo. Mesma config de hiperparâmetros já tunada,
mesmo esquema de exclusão dos 4 anos de El Niño forte, avaliado nos dois
mesmos lugares que já usamos:
  - Cenário B "de sempre" (tp fresco, meses de El Niño 1997-98/2015-16)
  - blocos realistas (tp congelado + lag crescente) - o proxy mais fiel que
    temos do comportamento real no Kaggle

Uso:
    .venv/bin/python scripts/train_stride3.py
"""

import numpy as np
import lightgbm as lgb
import pandas as pd

from features import build_training_table, FEATURE_FILES
from features_lagged import build_realistic_validation_block, load_raw_strided
from baseline_climatology import rmse
from train_lightgbm import FEATURES as FEATURES_V1, TARGET

STRIDE = 3
PARAMS = dict(
    objective="regression", metric="rmse", max_bin=127, verbosity=-1, num_threads=8,
    num_leaves=63, learning_rate=0.03, min_data_in_leaf=100,
    feature_fraction=0.7, bagging_fraction=0.7, bagging_freq=1,
)

BLOCK_1 = ("1997-05-01", "1998-04-01")
BLOCK_2 = ("2015-01-01", "2016-05-01")


def main():
    df = build_training_table(stride=STRIDE)
    df = df.dropna(subset=["oni"]).reset_index(drop=True)
    print(f"{len(df):,} linhas após remover NaN de ONI\n")

    excluded_years = {1997, 1998, 2015, 2016}
    is_excluded = df["target_year"].isin(list(excluded_years))
    is_el_nino = df["oni"] >= 0.5
    train_mask = (~is_excluded).values
    val_mask = (is_excluded & is_el_nino).values
    es_mask = train_mask & (df["target_year"] >= 2011).values & (df["target_year"] <= 2014).values
    core_train_mask = train_mask & ~es_mask

    train_set = lgb.Dataset(df.loc[core_train_mask, FEATURES_V1], label=df.loc[core_train_mask, TARGET])
    es_set = lgb.Dataset(df.loc[es_mask, FEATURES_V1], label=df.loc[es_mask, TARGET], reference=train_set)

    model = lgb.train(
        PARAMS, train_set, num_boost_round=6000,
        valid_sets=[es_set],
        callbacks=[lgb.early_stopping(stopping_rounds=80, verbose=False), lgb.log_evaluation(period=0)],
    )
    print(f"best_iteration={model.best_iteration}")
    model.save_model("../outputs/lgb_model_stride3.txt")

    preds_b = np.clip(model.predict(df.loc[val_mask, FEATURES_V1], num_iteration=model.best_iteration), 0, None)
    score_b = rmse(preds_b, df.loc[val_mask, TARGET].values)
    print(f"\nCenário B (tp fresco, El Niño): RMSE={score_b:.4f}  (stride=4 antes: 1.9379)")

    del df
    import gc
    gc.collect()

    arrays, lat_s, lon_s, time_full = load_raw_strided_at(STRIDE)
    for name, (first, last) in (("Bloco 1997-98", BLOCK_1), ("Bloco 2015-16", BLOCK_2)):
        val_df = build_realistic_validation_block(arrays, lat_s, lon_s, time_full, first, last)
        preds = np.clip(model.predict(val_df[FEATURES_V1], num_iteration=model.best_iteration), 0, None)
        score = rmse(preds, val_df[TARGET].values)
        print(f"{name} (tp congelado + lag): RMSE={score:.4f}")


def load_raw_strided_at(stride):
    import features_lagged as fl
    fl.STRIDE = stride
    return fl.load_raw_strided()


if __name__ == "__main__":
    main()
