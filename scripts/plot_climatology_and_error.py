"""
Mapas de climatologia e de erro do baseline, pra ver ONDE no mapa ele
funciona bem e onde erra mais.

Gera 4 imagens em outputs/figures/:
  climatologia_jan.png   - chuva média histórica de janeiro (verão/chuvoso)
  climatologia_jul.png   - chuva média histórica de julho (inverno/seco)
  erro_rmse.png          - RMSE por ponto de grade, validação 2016-2022
  erro_vies.png          - viés por ponto (superestima/subestima), mesma validação

Uso:
    .venv/bin/python scripts/plot_climatology_and_error.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sem display - só salvar PNG
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from baseline_climatology import DATA_DIR, build_climatology, target_calendar_month

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

# Paleta sequencial azul (light->dark), pra grandezas positivas (chuva, erro).
SEQ_BLUE = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]
CMAP_SEQ = LinearSegmentedColormap.from_list("seq_blue", SEQ_BLUE)

# Paleta diverging azul<->vermelho com meio-tom neutro cinza, pra viés
# (positivo = superestima, negativo = subestima).
CMAP_DIV = LinearSegmentedColormap.from_list(
    "div_blue_red", ["#0d366b", "#2a78d6", "#f0efec", "#eb6834", "#e34948"]
)


def plot_grid(values, lat, lon, title, cbar_label, out_path, cmap, norm=None, vmin=None, vmax=None):
    fig, ax = plt.subplots(figsize=(7, 7.5))
    mesh = ax.pcolormesh(lon, lat, values, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, shading="auto")
    ax.set_title(title, fontsize=12, wrap=True)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal")
    cbar = fig.colorbar(mesh, ax=ax, shrink=0.8)
    cbar.set_label(cbar_label)
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  salvo: {out_path}")


def main():
    print("Carregando treino_tp.nc / treino_tp_alvo.nc ...")
    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    tp_alvo = xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc")["tp_alvo"]
    lat = tp["lat"].values
    lon = tp["lon"].values

    # --- 1) mapas de climatologia (full history) para jan (chuvoso) e jul (seco) ---
    print("Climatologia (full history) ...")
    clim_full = build_climatology(tp, max_year=None)
    # Teto no percentil 98 (não no máximo bruto): o Chocó colombiano (litoral
    # Pacífico, ~5N/-77) é uma das regiões mais chuvosas do planeta e, com o
    # máximo bruto como teto, esses poucos pontos extremos esticam a escala e
    # apagam toda a variação no resto do continente (prática padrão em mapas
    # de precipitação: clipar em percentil alto, não no máximo).
    vmax = float(np.percentile(np.stack([clim_full[1], clim_full[7]]), 98))
    plot_grid(
        clim_full[1], lat, lon,
        "Climatologia - Janeiro (média histórica 1940-2022)",
        "precipitação média (mm/dia, clipado no p98)",
        OUT_DIR / "climatologia_jan.png",
        CMAP_SEQ, vmin=0, vmax=vmax,
    )
    plot_grid(
        clim_full[7], lat, lon,
        "Climatologia - Julho (média histórica 1940-2022)",
        "precipitação média (mm/dia, clipado no p98)",
        OUT_DIR / "climatologia_jul.png",
        CMAP_SEQ, vmin=0, vmax=vmax,
    )

    # --- 2) mapas de erro espacial, mesma validação temporal do baseline (2016-2022) ---
    print("Erro espacial do baseline (validação 2016-2022, sem leakage) ...")
    val_start, val_end = 2016, 2022
    clim_val = build_climatology(tp, max_year=val_start - 1)
    time_vals = tp["time"].values
    val_mask = (tp["time"].dt.year >= val_start) & (tp["time"].dt.year <= val_end)
    val_idx = np.where(val_mask.values)[0]

    errors = []
    for idx in val_idx:
        true = tp_alvo.isel(time=idx).values
        if np.isnan(true).all():
            continue
        month_m = pd.Timestamp(time_vals[idx]).month
        pred = clim_val[target_calendar_month(month_m)]
        errors.append(pred - true)
    errors = np.stack(errors)  # (n_meses_validos, lat, lon)

    rmse_map = np.sqrt(np.mean(errors**2, axis=0))
    bias_map = np.mean(errors, axis=0)

    rmse_vmax = float(np.percentile(rmse_map, 98))
    plot_grid(
        rmse_map, lat, lon,
        f"RMSE espacial do baseline de climatologia ({val_start}-{val_end})",
        "RMSE (mm/dia, clipado no p98)",
        OUT_DIR / "erro_rmse.png",
        CMAP_SEQ, vmin=0, vmax=rmse_vmax,
    )

    bias_abs_max = float(np.percentile(np.abs(bias_map), 98))
    plot_grid(
        bias_map, lat, lon,
        f"Viés espacial do baseline ({val_start}-{val_end})\nvermelho=superestima, azul=subestima",
        "viés médio (mm/dia, clipado no p98)",
        OUT_DIR / "erro_vies.png",
        CMAP_DIV, norm=TwoSlopeNorm(vcenter=0, vmin=-bias_abs_max, vmax=bias_abs_max),
    )

    print("\nResumo:")
    print(f"  RMSE espacial: min={rmse_map.min():.3f} max={rmse_map.max():.3f} mean={rmse_map.mean():.3f}")
    print(f"  Viés espacial: min={bias_map.min():.3f} max={bias_map.max():.3f} mean={bias_map.mean():.3f}")


if __name__ == "__main__":
    main()
