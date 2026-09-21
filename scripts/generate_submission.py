"""
Gera a submissão de teste com o LightGBM tunado, treinado em 100% do
histórico disponível (sem reservar validação - já validamos os
hiperparâmetros nos cenários A/B antes disso).

AVISO IMPORTANTE (leia antes de confiar no resultado):
A feature mais importante do modelo, de longe, é `tp` (chuva do mês
imediatamente anterior ao alvo). No treino, isso sempre foi o valor REAL de
`tp` daquele mês. Mas o `teste_features.nc` da competição não tem `tp` real
do mês anterior pra a maioria dos 24 meses - só tem `tp_ultima_obs`, que é a
chuva de DEZEMBRO/2022 CONGELADA, repetida pra todos os 24 meses (ver
`lag_meses`, que vai de 1 a 24). Ou seja: pra o mês alvo jan/2023 (lag=1),
`tp_ultima_obs` É o mês anterior de verdade. Mas pra dez/2024 (lag=24),
`tp_ultima_obs` é uma chuva de 2 ANOS atrás - a feature mais importante do
modelo fica cada vez mais desatualizada conforme os meses avançam. Isso é
uma limitação conhecida, não um bug: é a natureza do problema (ver docs,
seção 5). Não tem como "consertar" isso sem re-treinar o modelo pra aprender
a usar `lag_meses` e descontar a confiança em `tp` proporcionalmente - isso
fica pra próxima iteração.

Uso:
    .venv/bin/python scripts/generate_submission.py
"""

from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import xarray as xr

from train_lightgbm import load_table, FEATURES, TARGET
from baseline_climatology import DATA_DIR
from enso_bias_analysis import load_oni_monthly

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

FINAL_PARAMS = dict(
    objective="regression", metric="rmse", max_bin=127, verbosity=-1, num_threads=8,
    num_leaves=63, learning_rate=0.03, min_data_in_leaf=100,
    feature_fraction=0.7, bagging_fraction=0.7, bagging_freq=1,
)
NUM_BOOST_ROUND = 3793  # best_iteration encontrado no tuning (Cenário B)


def train_final_model() -> lgb.Booster:
    df = load_table()
    df = df.dropna(subset=["oni"]).reset_index(drop=True)
    print(f"Treinando modelo final com {len(df):,} linhas (100% do histórico com ONI disponível, sem held-out)")

    train_set = lgb.Dataset(df[FEATURES], label=df[TARGET])
    model = lgb.train(FINAL_PARAMS, train_set, num_boost_round=NUM_BOOST_ROUND)
    model.save_model(str(OUT_DIR / "lgb_model_final.txt"))
    print(f"Modelo final salvo em {OUT_DIR / 'lgb_model_final.txt'}")
    return model


def build_test_features() -> pd.DataFrame:
    oni = load_oni_monthly()
    teste = xr.open_dataset(DATA_DIR / "teste_features.nc")
    lat = teste["lat"].values
    lon = teste["lon"].values
    times = pd.to_datetime(teste["time"].values)
    n_lat, n_lon = len(lat), len(lon)
    n_points = n_lat * n_lon

    lat_grid, lon_grid = np.meshgrid(lat, lon, indexing="ij")
    lat_flat = lat_grid.reshape(-1).astype("float32")
    lon_flat = lon_grid.reshape(-1).astype("float32")

    month_num = times.month.values
    month_sin = np.sin(2 * np.pi * month_num / 12).astype("float32")
    month_cos = np.cos(2 * np.pi * month_num / 12).astype("float32")
    oni_per_month = np.array([float(oni.loc[(y, m)]) for y, m in zip(times.year, times.month)], dtype="float32")

    columns = {
        "lat": np.tile(lat_flat, len(times)),
        "lon": np.tile(lon_flat, len(times)),
        "month_sin": np.repeat(month_sin, n_points),
        "month_cos": np.repeat(month_cos, n_points),
        "oni": np.repeat(oni_per_month, n_points),
        # tp: sem chuva real do mês anterior disponível no teste (ver aviso no topo) -
        # único substituto possível é tp_ultima_obs (congelado em dez/2022)
        "tp": teste["tp_ultima_obs"].values.reshape(-1).astype("float32"),
    }
    var_map = {
        "t2": "t2", "cloud_cover": "cloud_cover", "surface_pressure": "surface_pressure",
        "shum_850": "shum_850", "rel_hum_850": "rel_hum_850", "temperature_850": "temperature_850",
        "geopotential_850": "geopotential_850", "u_850": "u_850", "v_850": "v_850",
    }
    for feat_name, nc_var in var_map.items():
        columns[feat_name] = teste[nc_var].values.reshape(-1).astype("float32")

    df = pd.DataFrame(columns)
    df["year"] = np.repeat(times.year.values.astype("int32"), n_points)
    df["month"] = np.repeat(times.month.values.astype("int32"), n_points)
    df["lat_r"] = df["lat"].round(2)
    df["lon_r"] = df["lon"].round(2)
    teste.close()
    return df


def main():
    model = train_final_model()
    test_df = build_test_features()
    print(f"Tabela de teste: {len(test_df):,} linhas (deve bater com 1.885.464 = 24 meses x 78.561 pontos)")

    preds = np.clip(model.predict(test_df[FEATURES], num_iteration=NUM_BOOST_ROUND), 0, None)
    test_df["pred"] = preds

    sample = pd.read_csv(DATA_DIR / "sample_submission.csv")
    parts = sample["id"].str.split("_", expand=True)
    lookup_year = parts[0].astype(int)
    lookup_month = parts[1].astype(int)
    lookup_lat = parts[2].astype(float).round(2)
    lookup_lon = parts[3].astype(float).round(2)

    key_test = test_df.set_index(["year", "month", "lat_r", "lon_r"])["pred"]
    lookup_keys = pd.MultiIndex.from_arrays([lookup_year, lookup_month, lookup_lat, lookup_lon])
    mapped = key_test.reindex(lookup_keys)
    if mapped.isna().any():
        raise ValueError(f"{mapped.isna().sum()} ids não encontrados na tabela de teste - checar alinhamento de lat/lon/mês.")

    sample["tp_mm_day"] = mapped.values
    out_path = OUT_DIR / "submission_lightgbm.csv"
    sample.to_csv(out_path, index=False)
    print(f"\nSubmissão escrita em {out_path} ({len(sample)} linhas)")
    print(f"  tp_mm_day: min={sample['tp_mm_day'].min():.3f} max={sample['tp_mm_day'].max():.3f} mean={sample['tp_mm_day'].mean():.3f}")


if __name__ == "__main__":
    main()
