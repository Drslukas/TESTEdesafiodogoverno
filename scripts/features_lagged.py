"""
Versão 2 da montagem de features: ensina o modelo a lidar com `tp` (chuva do
mês anterior) DESATUALIZADA, porque descobrimos (submissão real: 2.2287 vs
nossa validação interna de 1.94) que o teste real da competição nunca dá
`tp` fresco pra maioria dos 24 meses - só `tp_ultima_obs` (congelado em
dez/2022) + `lag_meses` (1 a 24, quão velho é esse valor).

Duas peças novas:

1. `build_training_table_lagged()` - tabela de treino onde, PRA CADA MÊS
   (não ponto a ponto), sorteamos um lag aleatório entre 1 e o máximo
   disponível, e a feature `tp` passa a ser "a chuva de `lag` meses atrás"
   em vez de sempre "a chuva do mês passado". Isso imita a distribuição real
   do teste (lag_meses uniforme entre 1 e 24) e ensina o modelo a usar
   `lag_meses` como feature explícita pra descontar a confiança em `tp`
   proporcionalmente.

2. `build_realistic_validation_block()` - validação que reproduz o
   mecanismo EXATO do teste real: congela `tp` num mês de corte e cresce
   `lag_meses` de 1 em diante ao longo de um bloco contínuo de meses-alvo
   (os episódios de El Niño 1997-98 e 2015-16), em vez de usar sempre o
   `tp` real e fresco como fizemos antes. Essa validação é o proxy mais
   fiel que temos do que o Kaggle realmente vai pontuar.
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

MAX_LAG = 24


def load_raw_strided():
    """Carrega as 10 variáveis + alvo, já sub-amostradas no stride, e mantém
    em memória (barato: ~200MB no total) pra reusar tanto no treino quanto
    na validação realista, sem reler os .nc duas vezes."""
    tp_ds = xr.open_dataset(DATA_DIR / "treino_tp.nc")
    lat_full = tp_ds["lat"].values
    lon_full = tp_ds["lon"].values
    time_full = pd.to_datetime(tp_ds["time"].values)
    tp_ds.close()

    lat_idx = np.arange(0, len(lat_full), STRIDE)
    lon_idx = np.arange(0, len(lon_full), STRIDE)
    lat_s = lat_full[lat_idx]
    lon_s = lon_full[lon_idx]

    arrays = {}
    for name, fname in FEATURE_FILES.items():
        ds = xr.open_dataset(DATA_DIR / fname)
        var = list(ds.data_vars)[0]
        arrays[name] = ds[var].values[:, lat_idx, :][:, :, lon_idx].astype("float32")
        ds.close()
        print(f"  carregado: {name}")

    alvo_ds = xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc")
    arrays["target"] = alvo_ds["tp_alvo"].values[:, lat_idx, :][:, :, lon_idx].astype("float32")
    alvo_ds.close()
    gc.collect()

    return arrays, lat_s, lon_s, time_full


def build_training_table_lagged(exclude_target_month_ranges=None, seed=0):
    """exclude_target_month_ranges: lista de (pd.Timestamp inicio, pd.Timestamp fim)
    de MESES-ALVO a excluir inteiramente do treino (pra não vazar pros blocos
    de validação realista)."""
    arrays, lat_s, lon_s, time_full = load_raw_strided()
    oni = load_oni_monthly()
    rng = np.random.default_rng(seed)

    n_lat, n_lon = len(lat_s), len(lon_s)
    n_points = n_lat * n_lon
    n_months = len(time_full) - 1  # último mês sem alvo válido

    input_months = time_full[:n_months]
    target_ts = input_months + pd.DateOffset(months=1)
    target_month_num = np.array([target_calendar_month(m.month) for m in input_months])
    target_year = target_ts.year.values

    exclude_target_month_ranges = exclude_target_month_ranges or []
    keep_mask = np.ones(n_months, dtype=bool)
    for start, end in exclude_target_month_ranges:
        in_range = (target_ts >= start) & (target_ts <= end)
        keep_mask &= ~np.asarray(in_range)
    kept_idx = np.where(keep_mask)[0]
    print(f"Meses de treino: {n_months} totais, {len(kept_idx)} após excluir blocos de validação realista")

    # sorteia 1 lag por MÊS (não por ponto) - imita lag_meses ser constante
    # dentro de um mês-alvo, exatamente como no teste_features.nc real
    max_lag_per_t = np.minimum(MAX_LAG, kept_idx + 1)  # não pode olhar antes do início da série
    lag_per_t = rng.integers(1, max_lag_per_t + 1)  # inclusive
    tp_source_idx = kept_idx - (lag_per_t - 1)

    oni_per_month = np.array([
        float(oni.loc[(y, m)]) if (y, m) in oni.index else np.nan
        for y, m in zip(target_year[kept_idx], target_month_num[kept_idx])
    ], dtype="float32")
    month_sin = np.sin(2 * np.pi * target_month_num[kept_idx] / 12).astype("float32")
    month_cos = np.cos(2 * np.pi * target_month_num[kept_idx] / 12).astype("float32")

    lat_grid, lon_grid = np.meshgrid(lat_s, lon_s, indexing="ij")
    lat_flat = lat_grid.reshape(-1).astype("float32")
    lon_flat = lon_grid.reshape(-1).astype("float32")
    n_kept = len(kept_idx)

    columns = {
        "lat": np.tile(lat_flat, n_kept),
        "lon": np.tile(lon_flat, n_kept),
        "month_sin": np.repeat(month_sin, n_points),
        "month_cos": np.repeat(month_cos, n_points),
        "oni": np.repeat(oni_per_month, n_points),
        "lag_meses": np.repeat(lag_per_t.astype("float32"), n_points),
        "tp": arrays["tp"][tp_source_idx].reshape(-1),  # defasado (o que muda vs. v1)
        "target_year": np.repeat(target_year[kept_idx].astype("int32"), n_points),
    }
    for name in FEATURE_FILES:
        if name == "tp":
            continue
        columns[name] = arrays[name][kept_idx].reshape(-1)  # sempre fresco - real no teste também
    columns["target"] = arrays["target"][kept_idx].reshape(-1)

    df = pd.DataFrame(columns)
    print(f"Tabela lagged: {df.shape[0]:,} linhas x {df.shape[1]} colunas ({df.memory_usage(deep=True).sum()/1e6:.0f} MB)")
    return df, arrays, lat_s, lon_s, time_full


def build_realistic_validation_block(arrays, lat_s, lon_s, time_full, first_target: str, last_target: str):
    """Reproduz o mecanismo exato do teste: congela `tp` no mês anterior ao
    início do bloco, e cresce lag_meses = 1, 2, 3... ao longo do bloco."""
    oni = load_oni_monthly()
    first_target = pd.Timestamp(first_target)
    last_target = pd.Timestamp(last_target)
    freeze_month = first_target - pd.DateOffset(months=1)

    time_index = {t: i for i, t in enumerate(time_full)}
    freeze_idx = time_index[freeze_month]
    tp_frozen = arrays["tp"][freeze_idx]  # (n_lat, n_lon) - mesmo valor pro bloco inteiro

    lat_grid, lon_grid = np.meshgrid(lat_s, lon_s, indexing="ij")
    lat_flat = lat_grid.reshape(-1).astype("float32")
    lon_flat = lon_grid.reshape(-1).astype("float32")
    n_points = len(lat_flat)

    rows = []
    cur = first_target
    lag = 1
    while cur <= last_target:
        t_idx = time_index[cur - pd.DateOffset(months=1)]  # índice do mês M (features atmosféricas reais)
        month_num = cur.month
        key = (cur.year, cur.month)
        oni_val = float(oni.loc[key]) if key in oni.index else np.nan

        row = {
            "lat": lat_flat, "lon": lon_flat,
            "month_sin": np.full(n_points, np.sin(2 * np.pi * month_num / 12), dtype="float32"),
            "month_cos": np.full(n_points, np.cos(2 * np.pi * month_num / 12), dtype="float32"),
            "oni": np.full(n_points, oni_val, dtype="float32"),
            "lag_meses": np.full(n_points, float(lag), dtype="float32"),
            "tp": tp_frozen.reshape(-1),
        }
        for name in FEATURE_FILES:
            if name == "tp":
                continue
            row[name] = arrays[name][t_idx].reshape(-1)
        row["target"] = arrays["target"][t_idx].reshape(-1)
        rows.append(pd.DataFrame(row))

        cur = cur + pd.DateOffset(months=1)
        lag += 1

    df = pd.concat(rows, ignore_index=True)
    print(f"Bloco de validação realista {first_target.date()} a {last_target.date()} "
          f"(freeze={freeze_month.date()}): {len(df):,} linhas, lag 1-{lag-1}")
    return df
