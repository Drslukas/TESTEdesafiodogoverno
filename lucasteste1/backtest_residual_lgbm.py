"""Backtest temporal que imita o mecanismo de teste do Kaggle.

Treina somente antes de 2015 e valida janeiro/2015--maio/2016, mantendo a
precipitação de dezembro/2014 congelada em todo o bloco de validação. O RMSE
é calculado sobre todos os pixels do bloco, como no leaderboard.
"""

from pathlib import Path
import sys
import argparse

import lightgbm as lgb
import numpy as np
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA_DIR, rmse
from train_residual_lightgbm import FEATURE_FILES, STRIDE, _clim_context


BLOCKS = {
    "1997": (pd.Timestamp("1997-05-01"), pd.Timestamp("1998-04-01")),
    "2015": (pd.Timestamp("2015-01-01"), pd.Timestamp("2016-05-01")),
}


def load_arrays():
    with xr.open_dataset(DATA_DIR / "treino_tp.nc") as ds:
        lat, lon = ds["lat"].values, ds["lon"].values
        times = pd.to_datetime(ds["time"].values)
    ii, jj = np.arange(0, len(lat), STRIDE), np.arange(0, len(lon), STRIDE)
    arrays = {}
    for name, file in FEATURE_FILES.items():
        print(f"Carregando {name}...", flush=True)
        with xr.open_dataset(DATA_DIR / file) as ds:
            var = list(ds.data_vars)[0]
            arrays[name] = ds[var].values[:-1, ii, :][:, :, jj].astype("float32")
    with xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc") as ds:
        arrays["target"] = ds["tp_alvo"].values[:-1, ii, :][:, :, jj].astype("float32")
    return arrays, lat[ii], lon[jj], times[:-1]


def make_frame(arrays, lat, lon, times, idx, clim, frozen_tp_idx=None, lag_values=None,
               circulation: bool = False, temporal: bool = False, multi_lag: bool = False,
               regional: bool = False,
               atmospheric_shift: int = 0, atmosphere_history: str = 'none'):
    if atmospheric_shift != 0:
        raise ValueError('Leakage: time_origem confirma que os campos devem ser anteriores ao alvo.')
    target_dates = times[idx] + pd.DateOffset(months=1)
    months = target_dates.month.to_numpy().astype("int16")
    n_points = len(lat) * len(lon)
    lat_grid, lon_grid = np.meshgrid(lat, lon, indexing="ij")
    la, lo = lat_grid.ravel().astype("float32"), lon_grid.ravel().astype("float32")
    clim_stack = np.stack([clim[int(m)] for m in months])
    if lag_values is None:
        lag_values = np.ones(len(idx), dtype="float32")
    lag_values = np.asarray(lag_values, dtype="float32")
    context = _clim_context(np.stack([clim[m] for m in range(1, 13)]))
    out = {
        "lat": np.tile(la, len(idx)), "lon": np.tile(lo, len(idx)),
        "month_sin": np.repeat(np.sin(2 * np.pi * months / 12).astype("float32"), n_points),
        "month_cos": np.repeat(np.cos(2 * np.pi * months / 12).astype("float32"), n_points),
        "climatology": clim_stack.ravel(),
        "lat2": np.tile((la / 30) ** 2, len(idx)),
        "lon2": np.tile((lo / 60) ** 2, len(idx)),
        "latlon": np.tile((la / 30) * (lo / 60), len(idx)),
        "lag_meses": np.repeat(lag_values, n_points),
    }
    for key, val in context.items():
        out[key] = np.concatenate([val[int(m) - 1].ravel() for m in months])
    for name, arr in arrays.items():
        if name == "target":
            continue
        if name == "tp" and frozen_tp_idx is not None:
            values = np.repeat(arr[frozen_tp_idx][None, ...], len(idx), axis=0)
        elif name == "tp":
            source_idx = idx - (lag_values.astype("int16") - 1)
            values = arr[source_idx]
        else:
            values = arr[idx + atmospheric_shift]
        out[name] = values.ravel()
        if name != 'tp' and atmosphere_history != 'none':
            history = []
            for offset in (1, 2):
                source = idx - offset
                previous = arr[np.maximum(source, 0)].copy()
                previous[source < 0] = np.nan
                out[f'{name}_lag{offset + 1}'] = previous.ravel()
                history.append(previous)
            if atmosphere_history == 'trajectory':
                out[f'{name}_delta_recent'] = (values - history[0]).ravel()
                out[f'{name}_delta_previous'] = (history[0] - history[1]).ravel()
        if regional and name != "tp":
            # Estado regional do campo atmosférico: calculado separadamente
            # para cada mês e usado como contexto de teleconexão.
            out[f"{name}_regional_mean"] = np.repeat(values.mean(axis=(1, 2)), n_points)
            out[f"{name}_regional_std"] = np.repeat(values.std(axis=(1, 2)), n_points)
        if name == "tp" and multi_lag:
            for lag in (1, 2, 3, 6, 12):
                if frozen_tp_idx is not None:
                    lag_values_arr = np.repeat(arr[frozen_tp_idx][None, ...], len(idx), axis=0)
                else:
                    lag_values_arr = arr[np.maximum(0, idx - (lag - 1))]
                out[f"tp_lag{lag}"] = lag_values_arr.ravel()
        if temporal and name in {"t2", "surface_pressure", "shum_850", "u_850", "v_850"}:
            # Média causal de três meses: usa somente o mês de entrada e seus
            # predecessores, portanto não acessa o mês-alvo da previsão.
            starts = np.maximum(0, idx - 2)
            cumulative = np.concatenate([np.zeros_like(arr[:1]), np.cumsum(arr, axis=0)], axis=0)
            means = (cumulative[idx + 1] - cumulative[starts]) / (idx - starts + 1)[:, None, None]
            out[f"{name}_mean_3m"] = means.ravel()
    if circulation:
        # Transporte de umidade em 850 hPa e intensidade do vento resumem a
        # circulação de baixo nível indicada na literatura para o Sul/Sudeste.
        out["moisture_flux_u"] = out["u_850"] * out["shum_850"]
        out["moisture_flux_v"] = out["v_850"] * out["shum_850"]
        out["wind_speed_850"] = np.hypot(out["u_850"], out["v_850"])
    out["target"] = (arrays["target"][idx] - clim_stack).ravel()
    return pd.DataFrame(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lag-aware", action="store_true", help="Treina com tp artificialmente defasada")
    parser.add_argument("--circulation", action="store_true", help="Adiciona fluxos de umidade e vento em 850 hPa")
    parser.add_argument("--temporal", action="store_true", help="Adiciona médias causais de três meses")
    parser.add_argument("--block", choices=sorted(BLOCKS), default="2015", help="Bloco temporal oculto")
    parser.add_argument("--atmospheric-shift", type=int, choices=[0, 1], default=0,
                        help="Alinha campos atmosféricos ao mês de entrada (0) ou ao mês-alvo (1)")
    args = parser.parse_args()
    first_target, last_target = BLOCKS[args.block]
    arrays, lat, lon, times = load_arrays()
    target_dates = times + pd.DateOffset(months=1)
    train_idx = np.where((target_dates < first_target) &
                         (np.arange(len(times)) + args.atmospheric_shift < len(times)))[0]
    val_idx = np.where((target_dates >= first_target) & (target_dates <= last_target) &
                       (np.arange(len(times)) + args.atmospheric_shift < len(times)))[0]
    month_train = target_dates[train_idx].month.to_numpy()
    clim = {m: arrays["target"][train_idx][month_train == m].mean(axis=0) for m in range(1, 13)}
    print(f"Treino até {target_dates[train_idx][-1].date()} ({len(train_idx)} meses); validação {first_target.date()}--{last_target.date()} ({len(val_idx)} meses)", flush=True)
    rng = np.random.default_rng(2026)
    train_lags = rng.integers(1, np.minimum(24, train_idx + 1) + 1).astype("float32")
    train = make_frame(arrays, lat, lon, times, train_idx, clim,
                       lag_values=train_lags if args.lag_aware else np.ones(len(train_idx), dtype="float32"),
                       circulation=args.circulation, temporal=args.temporal,
                       atmospheric_shift=args.atmospheric_shift)
    features = [c for c in train.columns if c != "target"]
    model = lgb.train(
        dict(objective="regression", metric="rmse", learning_rate=0.03, num_leaves=63,
             min_data_in_leaf=100, feature_fraction=0.8, bagging_fraction=0.8,
             bagging_freq=1, max_bin=127, verbosity=-1, num_threads=8),
        lgb.Dataset(train[features], label=train["target"]), num_boost_round=560,
    )
    frozen_tp_idx = val_idx[0]
    val = make_frame(arrays, lat, lon, times, val_idx, clim, frozen_tp_idx=frozen_tp_idx,
                     lag_values=np.arange(1, len(val_idx) + 1, dtype="float32"),
                     circulation=args.circulation, temporal=args.temporal,
                     atmospheric_shift=args.atmospheric_shift)
    raw_pred = val["climatology"].to_numpy() + model.predict(val[features])
    truth = arrays["target"][val_idx].ravel()
    baseline = np.stack([clim[int(m)] for m in target_dates[val_idx].month]).ravel()
    pred = np.clip(raw_pred, 0, None)
    weights = np.linspace(0.0, 1.0, 101)
    scores = np.array([
        rmse(np.clip(baseline + weight * (raw_pred - baseline), 0, None), truth)
        for weight in weights
    ])
    best = int(scores.argmin())
    print(f"RMSE climatologia: {rmse(baseline, truth):.4f}")
    label = "residual LGBM lag-aware" if args.lag_aware else "residual LGBM"
    print(f"RMSE {label} (tp congelada): {rmse(pred, truth):.4f}")
    print(f"Melhor blend: {weights[best]:.2f} modelo + {1 - weights[best]:.2f} climatologia; RMSE={scores[best]:.4f}")


if __name__ == "__main__":
    main()
