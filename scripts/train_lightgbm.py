"""
Treina um LightGBM tabular pra prever tp_alvo (mês M+1) a partir das 10
variáveis atmosféricas do mês M + lat/lon + sazonalidade + ONI.

Roda DOIS cenários de validação, os mesmos que usamos pra medir o baseline
de climatologia, pra comparação direta e honesta:

  Cenário A - "La Niña-heavy": treina em <=2015, valida em 2016-2022.
              Comparável ao RMSE da climatologia = 1.8666.
  Cenário B - "El Niño proxy": treina excluindo 1997,1998,2015,2016 por
              completo, valida SÓ nos meses de El Niño forte desses anos.
              Comparável ao RMSE da climatologia = 2.1206 (o número mais
              honesto pra esperar no teste real 2023-2024, que também foi
              dominado por El Niño).

Uso:
    .venv/bin/python scripts/train_lightgbm.py
"""

import gc
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd

from features import build_training_table
from baseline_climatology import rmse

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
CACHE_PATH = OUT_DIR / "training_table.parquet"

FEATURES = [
    "lat", "lon", "month_sin", "month_cos", "oni",
    "tp", "t2", "cloud_cover", "surface_pressure", "shum_850",
    "rel_hum_850", "temperature_850", "geopotential_850", "u_850", "v_850",
]
TARGET = "target"

LGB_PARAMS = dict(
    objective="regression",
    metric="rmse",
    learning_rate=0.05,
    num_leaves=63,
    max_bin=127,
    min_data_in_leaf=50,
    feature_fraction=0.8,
    bagging_fraction=0.8,
    bagging_freq=1,
    verbosity=-1,
    num_threads=8,
)


def load_table() -> pd.DataFrame:
    if CACHE_PATH.exists():
        print(f"Lendo tabela cacheada: {CACHE_PATH}")
        return pd.read_parquet(CACHE_PATH)
    df = build_training_table()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CACHE_PATH, index=False)
    print(f"Tabela salva em cache: {CACHE_PATH}")
    return df


def train_and_eval(df: pd.DataFrame, train_mask: np.ndarray, val_mask: np.ndarray,
                    internal_eval_mask: np.ndarray, label: str, baseline_rmse: float) -> lgb.Booster:
    core_train_mask = train_mask & ~internal_eval_mask
    X_train = df.loc[core_train_mask, FEATURES]
    y_train = df.loc[core_train_mask, TARGET]
    X_es = df.loc[internal_eval_mask, FEATURES]
    y_es = df.loc[internal_eval_mask, TARGET]
    X_val = df.loc[val_mask, FEATURES]
    y_val = df.loc[val_mask, TARGET]

    print(f"\n=== Cenário {label} ===")
    print(f"  treino: {len(X_train):,} linhas | early-stopping interno: {len(X_es):,} | validação final: {len(X_val):,}")

    train_set = lgb.Dataset(X_train, label=y_train)
    es_set = lgb.Dataset(X_es, label=y_es, reference=train_set)

    model = lgb.train(
        LGB_PARAMS,
        train_set,
        num_boost_round=2000,
        valid_sets=[es_set],
        callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False), lgb.log_evaluation(period=0)],
    )

    preds = np.clip(model.predict(X_val, num_iteration=model.best_iteration), 0, None)
    score = rmse(preds, y_val.values)
    print(f"  best_iteration={model.best_iteration}")
    print(f"  RMSE LightGBM: {score:.4f}  |  RMSE climatologia (mesma validação): {baseline_rmse:.4f}  |  "
          f"{'MELHOROU' if score < baseline_rmse else 'PIOROU'} {abs(score-baseline_rmse)/baseline_rmse*100:.1f}%")

    importance = pd.Series(model.feature_importance(importance_type="gain"), index=FEATURES).sort_values(ascending=False)
    print("  importância das features (gain):")
    for feat, val in importance.items():
        print(f"    {feat:<20} {val:>12.0f}")

    return model


def main():
    df = load_table()
    df = df.dropna(subset=["oni"]).reset_index(drop=True)
    print(f"Após remover linhas sem ONI (1940-49, sem dado histórico): {len(df):,} linhas")

    # --- Cenário A: La Niña-heavy ---
    train_a = df["target_year"] <= 2015
    val_a = (df["target_year"] >= 2016) & (df["target_year"] <= 2022)
    es_a = (df["target_year"] >= 2011) & (df["target_year"] <= 2015)  # últimos 5 anos do treino, cronológico
    model_a = train_and_eval(df, train_a.values, val_a.values, es_a.values, "A (La Niña-heavy)", 1.8666)

    del train_a, val_a, es_a
    gc.collect()

    # --- Cenário B: El Niño proxy ---
    excluded_years = {1997, 1998, 2015, 2016}
    is_excluded = df["target_year"].isin(list(excluded_years))
    is_el_nino = df["oni"] >= 0.5
    train_b = ~is_excluded
    val_b = is_excluded & is_el_nino
    es_b = train_b & (df["target_year"] >= 2011) & (df["target_year"] <= 2014)
    model_b = train_and_eval(df, train_b.values, val_b.values, es_b.values, "B (El Niño proxy)", 2.1206)

    model_a.save_model(str(OUT_DIR / "lgb_model_a.txt"))
    model_b.save_model(str(OUT_DIR / "lgb_model_b.txt"))
    print(f"\nModelos salvos em {OUT_DIR}/lgb_model_a.txt e lgb_model_b.txt")


if __name__ == "__main__":
    main()
