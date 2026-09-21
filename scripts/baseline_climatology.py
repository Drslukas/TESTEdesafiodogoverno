"""
Baseline de climatologia para o desafio WORCAP 2026 (precipitação AmSul).

A doc oficial diz: "a régua a bater é a climatologia" — um bom modelo precisa
superar a média histórica por ponto/mês, não apenas reproduzi-la. Este script:

1. `validate`  — mede RMSE do baseline de climatologia (e de persistência,
   pra comparação) usando um corte temporal dentro do treino, nunca split
   aleatório (ver docs/DESAFIO_KAGGLE_OVERVIEW.md, seção 12).
2. `submit`    — gera um CSV pronto para envio ao Kaggle, usando a
   climatologia calculada com TODO o histórico de treino (1940-2022).

Uso:
    .venv/bin/python scripts/baseline_climatology.py validate
    .venv/bin/python scripts/baseline_climatology.py validate --val-start 2018 --val-end 2022
    .venv/bin/python scripts/baseline_climatology.py submit
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "previsao-climatica-de-precipitacao-sobre-a-america-do-sul"
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def build_climatology(tp: xr.DataArray, max_year: int | None) -> dict[int, np.ndarray]:
    """climatology[month] = grade (lat, lon) com a média histórica de tp naquele mês do calendário.

    max_year restringe o histórico usado (ex.: para não vazar anos de validação
    para dentro da própria estatística "histórica" — ver docs seção 12).
    """
    if max_year is not None:
        tp = tp.sel(time=tp["time"].dt.year <= max_year)
    return {m: tp.sel(time=tp["time"].dt.month == m).mean(dim="time").values for m in range(1, 13)}


def rmse(pred: np.ndarray, true: np.ndarray) -> float:
    mask = ~np.isnan(true)
    return float(np.sqrt(np.mean((pred[mask] - true[mask]) ** 2)))


def target_calendar_month(month_m: int) -> int:
    """Mês M -> mês do calendário do alvo M+1 (com virada dez->jan)."""
    return (month_m % 12) + 1


def cmd_validate(val_start: int, val_end: int) -> None:
    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    tp_alvo = xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc")["tp_alvo"]

    # climatologia treinada SÓ com anos estritamente anteriores à janela de
    # validação — senão a "média histórica" incluiria os próprios meses sendo
    # avaliados, vazando informação futura pra dentro de uma estatística que
    # deveria ser puramente histórica (docs seção 12, "como evitar leakage").
    clim = build_climatology(tp, max_year=val_start - 1)

    time_vals = tp["time"].values
    val_mask = (tp["time"].dt.year >= val_start) & (tp["time"].dt.year <= val_end)
    val_idx = np.where(val_mask.values)[0]

    clim_preds, persist_preds, trues = [], [], []
    for idx in val_idx:
        true = tp_alvo.isel(time=idx).values
        if np.isnan(true).all():
            continue  # último mês da série inteira não tem alvo válido
        month_m = pd.Timestamp(time_vals[idx]).month
        clim_preds.append(clim[target_calendar_month(month_m)])
        persist_preds.append(tp.isel(time=idx).values)  # persistência: tp(M) como previsão de M+1
        trues.append(true)

    clim_preds = np.stack(clim_preds)
    persist_preds = np.stack(persist_preds)
    trues = np.stack(trues)
    global_mean_pred = np.full_like(trues, float(np.nanmean(trues)))

    print(f"Validação temporal: {val_start}-{val_end} ({len(trues)} meses com alvo válido)")
    print(f"Climatologia calculada apenas com anos <= {val_start - 1} (sem leakage)")
    print()
    print(f"  RMSE média global (piso de sanity check): {rmse(global_mean_pred, trues):.4f} mm/dia")
    print(f"  RMSE persistência (tp(M) como previsão):  {rmse(persist_preds, trues):.4f} mm/dia")
    print(f"  RMSE climatologia (por ponto/mês):        {rmse(clim_preds, trues):.4f} mm/dia")


def cmd_submit(out_path: Path) -> None:
    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    clim = build_climatology(tp, max_year=None)  # todo o histórico, 1940-2022

    teste = xr.open_dataset(DATA_DIR / "teste_features.nc")
    lat = teste["lat"].values
    lon = teste["lon"].values

    lat_to_idx = {round(float(v), 2): i for i, v in enumerate(lat)}
    lon_to_idx = {round(float(v), 2): j for j, v in enumerate(lon)}

    sample = pd.read_csv(DATA_DIR / "sample_submission.csv")
    # nunca reconstruir o id manualmente (instrução oficial) — só parsear o id
    # já fornecido pra descobrir mês/lat/lon e preencher tp_mm_day na ordem dada.
    parts = sample["id"].str.split("_", expand=True)
    months = parts[1].astype(int)
    lats = parts[2].astype(float).round(2)
    lons = parts[3].astype(float).round(2)

    lat_idx = lats.map(lat_to_idx).to_numpy()
    lon_idx = lons.map(lon_to_idx).to_numpy()
    if np.isnan(lat_idx).any() or np.isnan(lon_idx).any():
        raise ValueError("Falha ao mapear lat/lon do id para a grade — checar precisão/arredondamento.")
    lat_idx = lat_idx.astype(int)
    lon_idx = lon_idx.astype(int)

    preds = np.empty(len(sample), dtype=np.float32)
    for month in range(1, 13):
        mask = (months == month).to_numpy()
        preds[mask] = clim[month][lat_idx[mask], lon_idx[mask]]

    sample["tp_mm_day"] = preds
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(out_path, index=False)
    print(f"Submissão escrita em {out_path} ({len(sample)} linhas)")
    print(f"  tp_mm_day: min={preds.min():.3f} max={preds.max():.3f} mean={preds.mean():.3f}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="mede RMSE via corte temporal dentro do treino")
    p_val.add_argument("--val-start", type=int, default=2016)
    p_val.add_argument("--val-end", type=int, default=2022)

    p_sub = sub.add_parser("submit", help="gera CSV de submissão com climatologia full-history")
    p_sub.add_argument("--out", type=str, default=str(OUT_DIR / "submission_climatology.csv"))

    args = parser.parse_args()
    if args.cmd == "validate":
        cmd_validate(args.val_start, args.val_end)
    elif args.cmd == "submit":
        cmd_submit(Path(args.out))


if __name__ == "__main__":
    main()
