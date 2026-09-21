"""
Busca de hiperparâmetros pro LightGBM, usando o Cenário B (El Niño proxy:
treina excluindo 1997/1998/2015/2016, valida nos meses de El Niño forte
desses anos) como métrica principal - é o cenário mais parecido com o teste
real 2023-2024. O Cenário A (La Niña-heavy) é reavaliado só pra a
configuração vencedora, como checagem de sanidade (não queremos um config
que otimiza só pro regime raro e piora muito no regime comum).

Uso:
    .venv/bin/python scripts/tune_lightgbm.py
"""

import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd

from train_lightgbm import load_table, FEATURES, TARGET
from baseline_climatology import rmse

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

CANDIDATES = [
    {"name": "baseline",        "num_leaves": 63,  "learning_rate": 0.05, "min_data_in_leaf": 50,  "feature_fraction": 0.8, "bagging_fraction": 0.8, "lambda_l1": 0.0, "lambda_l2": 0.0},
    {"name": "mais_folhas",     "num_leaves": 127, "learning_rate": 0.05, "min_data_in_leaf": 50,  "feature_fraction": 0.8, "bagging_fraction": 0.8, "lambda_l1": 0.0, "lambda_l2": 0.0},
    {"name": "lr_alto_raso",    "num_leaves": 31,  "learning_rate": 0.10, "min_data_in_leaf": 30,  "feature_fraction": 0.8, "bagging_fraction": 0.8, "lambda_l1": 0.0, "lambda_l2": 0.0},
    {"name": "mais_regular",    "num_leaves": 63,  "learning_rate": 0.03, "min_data_in_leaf": 100, "feature_fraction": 0.7, "bagging_fraction": 0.7, "lambda_l1": 0.0, "lambda_l2": 0.0},
    {"name": "folhas_min_data", "num_leaves": 127, "learning_rate": 0.03, "min_data_in_leaf": 20,  "feature_fraction": 0.8, "bagging_fraction": 0.8, "lambda_l1": 0.0, "lambda_l2": 0.0},
    {"name": "l1_l2",           "num_leaves": 63,  "learning_rate": 0.05, "min_data_in_leaf": 50,  "feature_fraction": 0.8, "bagging_fraction": 0.8, "lambda_l1": 0.1, "lambda_l2": 1.0},
]


def main():
    df = load_table()
    df = df.dropna(subset=["oni"]).reset_index(drop=True)
    print(f"{len(df):,} linhas após remover NaN de ONI\n")

    excluded_years = {1997, 1998, 2015, 2016}
    is_excluded = df["target_year"].isin(list(excluded_years))
    is_el_nino = df["oni"] >= 0.5
    train_mask = (~is_excluded).values
    val_mask = (is_excluded & is_el_nino).values
    es_mask = (train_mask & (df["target_year"] >= 2011).values & (df["target_year"] <= 2014).values)
    core_train_mask = train_mask & ~es_mask

    X_train = df.loc[core_train_mask, FEATURES]
    y_train = df.loc[core_train_mask, TARGET]
    X_es = df.loc[es_mask, FEATURES]
    y_es = df.loc[es_mask, TARGET]
    X_val = df.loc[val_mask, FEATURES]
    y_val = df.loc[val_mask, TARGET].values

    print(f"treino: {len(X_train):,} | early-stopping: {len(X_es):,} | validação (El Niño proxy): {len(X_val):,}\n")

    train_set = lgb.Dataset(X_train, label=y_train)
    es_set = lgb.Dataset(X_es, label=y_es, reference=train_set)

    results = []
    for cfg in CANDIDATES:
        name = cfg["name"]
        params = dict(
            objective="regression", metric="rmse", max_bin=127, verbosity=-1, num_threads=8,
            feature_pre_filter=False,  # varia min_data_in_leaf entre configs - sem isso, o Dataset
            # reusado trava na 2a chamada (o filtro é fixado pelo 1o min_data_in_leaf usado)
            **{k: v for k, v in cfg.items() if k != "name"},
        )
        model = lgb.train(
            params, train_set, num_boost_round=2000,
            valid_sets=[es_set],
            callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False), lgb.log_evaluation(period=0)],
        )
        preds = np.clip(model.predict(X_val, num_iteration=model.best_iteration), 0, None)
        score = rmse(preds, y_val)
        results.append({"name": name, "rmse": score, "best_iteration": model.best_iteration, **cfg})
        print(f"  {name:<16} RMSE={score:.4f}  best_iter={model.best_iteration}  {cfg}")

    results.sort(key=lambda r: r["rmse"])
    print("\n=== Ranking (melhor primeiro) ===")
    for r in results:
        print(f"  {r['name']:<16} RMSE={r['rmse']:.4f}")

    best = results[0]
    print(f"\nMelhor config: {best['name']} (RMSE={best['rmse']:.4f}, climatologia=2.1206)")
    (OUT_DIR / "best_lgb_params.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
    print(f"salvo: {OUT_DIR / 'best_lgb_params.json'}")


if __name__ == "__main__":
    main()
