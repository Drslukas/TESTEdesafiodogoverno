"""
Reavalia a config vencedora do tuning (mais_regular) com mais rounds de
boosting (ela bateu quase no teto de 2000 antes), e confere que ela não
piora o Cenário A (La Niña-heavy) como efeito colateral.

Uso:
    .venv/bin/python scripts/finalize_best_config.py
"""

import numpy as np
import lightgbm as lgb

from train_lightgbm import load_table, FEATURES, TARGET
from baseline_climatology import rmse

BEST_PARAMS = dict(
    objective="regression", metric="rmse", max_bin=127, verbosity=-1, num_threads=8,
    feature_pre_filter=False,
    num_leaves=63, learning_rate=0.03, min_data_in_leaf=100,
    feature_fraction=0.7, bagging_fraction=0.7, bagging_freq=1,
)


def main():
    df = load_table()
    df = df.dropna(subset=["oni"]).reset_index(drop=True)

    excluded_years = {1997, 1998, 2015, 2016}
    is_excluded = df["target_year"].isin(list(excluded_years))
    is_el_nino = df["oni"] >= 0.5

    # --- Cenário B com mais rounds ---
    train_mask = (~is_excluded).values
    val_mask = (is_excluded & is_el_nino).values
    es_mask = train_mask & (df["target_year"] >= 2011).values & (df["target_year"] <= 2014).values
    core_train_mask = train_mask & ~es_mask

    train_set = lgb.Dataset(df.loc[core_train_mask, FEATURES], label=df.loc[core_train_mask, TARGET])
    es_set = lgb.Dataset(df.loc[es_mask, FEATURES], label=df.loc[es_mask, TARGET], reference=train_set)

    model_b = lgb.train(
        BEST_PARAMS, train_set, num_boost_round=6000,
        valid_sets=[es_set],
        callbacks=[lgb.early_stopping(stopping_rounds=80, verbose=False), lgb.log_evaluation(period=0)],
    )
    preds_b = np.clip(model_b.predict(df.loc[val_mask, FEATURES], num_iteration=model_b.best_iteration), 0, None)
    score_b = rmse(preds_b, df.loc[val_mask, TARGET].values)
    print(f"Cenário B (El Niño proxy): RMSE={score_b:.4f}  best_iter={model_b.best_iteration}/6000  "
          f"(climatologia=2.1206, tuning anterior=1.9405)")

    # --- checagem: mesma config no Cenário A, não regrediu? ---
    train_a_mask = (df["target_year"] <= 2015).values
    val_a_mask = ((df["target_year"] >= 2016) & (df["target_year"] <= 2022)).values
    es_a_mask = train_a_mask & (df["target_year"] >= 2011).values & (df["target_year"] <= 2015).values
    core_train_a_mask = train_a_mask & ~es_a_mask

    train_set_a = lgb.Dataset(df.loc[core_train_a_mask, FEATURES], label=df.loc[core_train_a_mask, TARGET])
    es_set_a = lgb.Dataset(df.loc[es_a_mask, FEATURES], label=df.loc[es_a_mask, TARGET], reference=train_set_a)

    model_a = lgb.train(
        BEST_PARAMS, train_set_a, num_boost_round=6000,
        valid_sets=[es_set_a],
        callbacks=[lgb.early_stopping(stopping_rounds=80, verbose=False), lgb.log_evaluation(period=0)],
    )
    preds_a = np.clip(model_a.predict(df.loc[val_a_mask, FEATURES], num_iteration=model_a.best_iteration), 0, None)
    score_a = rmse(preds_a, df.loc[val_a_mask, TARGET].values)
    print(f"Cenário A (La Niña-heavy): RMSE={score_a:.4f}  best_iter={model_a.best_iteration}/6000  "
          f"(climatologia=1.8666, LightGBM baseline anterior=1.8835)")


if __name__ == "__main__":
    main()
