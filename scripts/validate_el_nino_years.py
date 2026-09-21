"""
Revalidação do baseline usando os dois episódios de El Niño forte do
histórico (1997-98 e 2015-16) como proxy do regime real de teste (2023-2024,
também dominado por El Niño) — em vez da janela 2016-2022, que era dominada
por La Niña e mede as condições ERRADAS (ver conversa/GRAPH_REPORT).

Metodologia:
- Um mês entra na validação se sua fase ENSO (ONI do mês-alvo M+1) for
  El Niño (ONI >= 0.5) E o ano do mês-alvo estiver em {1997, 1998, 2015, 2016}.
  Isso evita contaminar com meses de La Niña que também caem dentro desses
  anos-calendário (ex.: 1998 vira La Niña forte no 2º semestre; 2016 vira
  neutro/La Niña fraca a partir de junho).
- A climatologia é calculada com TODO o histórico EXCETO esses 4 anos
  (1997, 1998, 2015, 2016) inteiros - não só os meses de El Niño dentro
  deles - pra não vazar nenhum dado desses anos pra dentro da própria
  "média histórica" usada como previsão.

Uso:
    .venv/bin/python scripts/validate_el_nino_years.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from baseline_climatology import DATA_DIR, rmse, target_calendar_month
from enso_bias_analysis import load_oni_monthly, classify
from dipole_regions_timeseries import REGIONS

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

EXCLUDED_YEARS = {1997, 1998, 2015, 2016}  # anos dos dois episódios de El Niño forte

CMAP_SEQ = LinearSegmentedColormap.from_list("seq_blue", [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
])
CMAP_DIV = LinearSegmentedColormap.from_list(
    "div_blue_red", ["#0d366b", "#2a78d6", "#f0efec", "#eb6834", "#e34948"]
)


def main():
    oni = load_oni_monthly()
    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    tp_alvo = xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc")["tp_alvo"]
    lat = tp["lat"].values
    lon = tp["lon"].values

    # climatologia SEM os 4 anos-calendário dos dois episódios - impede leakage
    # NOTA: xr.DataArray.isin() falha silenciosamente (retorna tudo False) se
    # receber um set() do Python em vez de list/array - por isso list() aqui.
    tp_train = tp.sel(time=~tp["time"].dt.year.isin(list(EXCLUDED_YEARS)))
    clim = {m: tp_train.sel(time=tp_train["time"].dt.month == m).mean(dim="time").values for m in range(1, 13)}
    print(f"Climatologia calculada com {tp_train.sizes['time']} meses "
          f"(exclui {sorted(EXCLUDED_YEARS)} por completo, {tp.sizes['time'] - tp_train.sizes['time']} meses fora)")

    time_vals = tp["time"].values
    clim_preds, persist_preds, trues, tags = [], [], [], []
    for idx in range(len(time_vals)):
        true = tp_alvo.isel(time=idx).values
        if np.isnan(true).all():
            continue
        ts = pd.Timestamp(time_vals[idx])
        target_ts = ts + pd.DateOffset(months=1)
        if target_ts.year not in EXCLUDED_YEARS:
            continue
        key = (target_ts.year, target_ts.month)
        if key not in oni.index:
            continue
        if classify(float(oni.loc[key])) != "El Niño":
            continue  # só os meses de El Niño de verdade dentro desses anos

        tmonth = target_calendar_month(ts.month)
        clim_preds.append(clim[tmonth])
        persist_preds.append(tp.isel(time=idx).values)
        trues.append(true)
        tags.append(f"{target_ts.year}-{target_ts.month:02d} (ONI={float(oni.loc[key]):+.2f})")

    clim_preds = np.stack(clim_preds)
    persist_preds = np.stack(persist_preds)
    trues = np.stack(trues)
    global_mean_pred = np.full_like(trues, float(np.nanmean(trues)))

    print(f"\n{len(trues)} meses de El Niño forte usados na validação:")
    for t in tags:
        print(f"  {t}")

    print("\n=== Comparação: validação La Niña-heavy (2016-2022) vs El Niño proxy (1997-98, 2015-16) ===")
    print(f"{'baseline':<28} {'La Niña-heavy (n=83)':>22} {'El Niño proxy (n=' + str(len(trues)) + ')':>22}")
    print(f"{'média global':<28} {3.9146:>22.4f} {rmse(global_mean_pred, trues):>22.4f}")
    print(f"{'persistência':<28} {2.7906:>22.4f} {rmse(persist_preds, trues):>22.4f}")
    print(f"{'climatologia':<28} {1.8666:>22.4f} {rmse(clim_preds, trues):>22.4f}")

    # --- viés espacial neste regime ---
    errors = clim_preds - trues
    bias_map = errors.mean(axis=0)
    rmse_map = np.sqrt((errors ** 2).mean(axis=0))
    print(f"\nRMSE espacial (El Niño proxy): min={rmse_map.min():.3f} max={rmse_map.max():.3f} mean={rmse_map.mean():.3f}")
    print(f"Viés espacial (El Niño proxy): min={bias_map.min():.3f} max={bias_map.max():.3f} mean={bias_map.mean():.3f}")

    # comparação regional Norte vs Centro-Sul (mesmas caixas do dipolo)
    print("\nViés médio por região (El Niño proxy):")
    for name, box in REGIONS.items():
        lat_mask = (lat >= box["lat_min"]) & (lat <= box["lat_max"])
        lon_mask = (lon >= box["lon_min"]) & (lon <= box["lon_max"])
        idx = np.ix_(lat_mask, lon_mask)
        region_bias = bias_map[idx].mean()
        print(f"  {name}: {region_bias:+.3f} mm/dia")

    bias_abs_max = float(np.percentile(np.abs(bias_map), 98))
    fig, ax = plt.subplots(figsize=(7, 7.5))
    norm = TwoSlopeNorm(vcenter=0, vmin=-bias_abs_max, vmax=bias_abs_max)
    mesh = ax.pcolormesh(lon, lat, bias_map, cmap=CMAP_DIV, norm=norm, shading="auto")
    ax.set_title(
        f"Viés do baseline em El Niño forte (1997-98, 2015-16, n={len(trues)})\n"
        "vermelho=superestima, azul=subestima",
        fontsize=12,
    )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal")
    cbar = fig.colorbar(mesh, ax=ax, shrink=0.8)
    cbar.set_label("viés médio (mm/dia)")
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / "vies_el_nino_forte_historico.png", dpi=130)
    print(f"\nsalvo: {OUT_DIR / 'vies_el_nino_forte_historico.png'}")


if __name__ == "__main__":
    main()
