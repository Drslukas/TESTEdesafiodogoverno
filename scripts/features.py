"""
Monta a matriz tabular (ponto de grade, mês) -> features/target, usada pelo
LightGBM. Roda com um SUBAMOSTRAGEM espacial (stride) porque a máquina tem
pouca RAM livre (~2GB) e a grade completa (301x261x996 meses) não cabe
confortavelmente em memória com todas as 10 variáveis simultâneas.

Trade-off explícito: com stride=4, treinamos vendo 1 em cada 16 pontos de
grade (301x261 -> ~76x66 -> ~5000 pontos). O modelo generaliza pros pontos
não vistos via lat/lon como features numéricas (LightGBM interpola via
splits de árvore), mas pode perder detalhe fino em áreas de relevo abrupto
(ex.: Chocó colombiano, Andes) onde a chuva muda muito em poucos km.
"""

import gc
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from baseline_climatology import DATA_DIR, target_calendar_month
from enso_bias_analysis import load_oni_monthly

STRIDE = 4

FEATURE_FILES = {
    "tp": "treino_tp.nc",
    "t2": "treino_t2.nc",
    "cloud_cover": "treino_cloud_cover.nc",
    "surface_pressure": "treino_surface_pressure.nc",
    "shum_850": "treino_shum_850.nc",
    "rel_hum_850": "treino_rel_hum_850.nc",
    "temperature_850": "treino_temperature_850.nc",
    "geopotential_850": "treino_geopotential_850.nc",
    "u_850": "treino_u_850.nc",
    "v_850": "treino_v_850.nc",
}


def build_training_table(stride: int = STRIDE) -> pd.DataFrame:
    oni = load_oni_monthly()

    tp_ds = xr.open_dataset(DATA_DIR / "treino_tp.nc")
    lat_full = tp_ds["lat"].values
    lon_full = tp_ds["lon"].values
    time_full = pd.to_datetime(tp_ds["time"].values)
    tp_ds.close()

    lat_idx = np.arange(0, len(lat_full), stride)
    lon_idx = np.arange(0, len(lon_full), stride)
    lat_s = lat_full[lat_idx]
    lon_s = lon_full[lon_idx]
    n_lat, n_lon = len(lat_s), len(lon_s)
    n_points = n_lat * n_lon

    n_months = len(time_full) - 1  # descarta o último mês (target NaN)
    print(f"Grade completa 301x261 -> stride={stride} -> {n_lat}x{n_lon} = {n_points} pontos")
    print(f"{n_months} meses válidos -> {n_months * n_points:,} linhas na tabela")

    # --- colunas que dependem só do tempo (repetidas por todos os pontos daquele mês) ---
    input_months = time_full[:n_months]
    target_ts = input_months + pd.DateOffset(months=1)
    target_month_num = np.array([target_calendar_month(m.month) for m in input_months])
    target_year = target_ts.year.values

    oni_per_month = np.array([
        float(oni.loc[(y, m)]) if (y, m) in oni.index else np.nan
        for y, m in zip(target_year, target_month_num)
    ], dtype="float32")

    month_sin = np.sin(2 * np.pi * target_month_num / 12).astype("float32")
    month_cos = np.cos(2 * np.pi * target_month_num / 12).astype("float32")

    # --- colunas espaciais (repetidas em bloco por mês) ---
    lat_grid, lon_grid = np.meshgrid(lat_s, lon_s, indexing="ij")
    lat_flat = lat_grid.reshape(-1).astype("float32")
    lon_flat = lon_grid.reshape(-1).astype("float32")

    columns = {
        "lat": np.tile(lat_flat, n_months),
        "lon": np.tile(lon_flat, n_months),
        "month_sin": np.repeat(month_sin, n_points),
        "month_cos": np.repeat(month_cos, n_points),
        "oni": np.repeat(oni_per_month, n_points),
        "input_year": np.repeat(input_months.year.values.astype("int32"), n_points),
        "target_year": np.repeat(target_year.astype("int32"), n_points),
    }

    # --- as 10 variáveis atmosféricas do mês M (features) ---
    for name, fname in FEATURE_FILES.items():
        ds = xr.open_dataset(DATA_DIR / fname)
        var = list(ds.data_vars)[0]
        arr = ds[var].values[:n_months, :, :][:, lat_idx, :][:, :, lon_idx].astype("float32")
        columns[name] = arr.reshape(-1)
        ds.close()
        del arr
        gc.collect()
        print(f"  carregado: {name}")

    # --- target: tp do mês M+1 (tp_alvo) ---
    alvo_ds = xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc")
    alvo_arr = alvo_ds["tp_alvo"].values[:n_months, :, :][:, lat_idx, :][:, :, lon_idx].astype("float32")
    columns["target"] = alvo_arr.reshape(-1)
    alvo_ds.close()
    del alvo_arr
    gc.collect()
    print("  carregado: target (tp_alvo)")

    df = pd.DataFrame(columns)
    print(f"Tabela final: {df.shape[0]:,} linhas x {df.shape[1]} colunas ({df.memory_usage(deep=True).sum()/1e6:.0f} MB)")
    return df


if __name__ == "__main__":
    df = build_training_table()
    print(df.head())
    print(df.describe().T)
