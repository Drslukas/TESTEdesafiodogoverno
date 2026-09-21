"""
Mostra por que a anomalia MÉDIA do continente inteiro fica "normal" em
2016-2022 mesmo com El Niño/La Niña atuando forte: compara a anomalia de
duas sub-regiões (Norte, que ficou azul/subestimada nos mapas de viés, e
Centro-Sul, que ficou vermelha/superestimada) contra a média de todo o
domínio. A ideia: se elas andam em direções opostas, a média do continente
some o sinal - mesmo com cada região individualmente "gritando".

Uso:
    .venv/bin/python scripts/dipole_regions_timeseries.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from baseline_climatology import DATA_DIR, build_climatology

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

# caixas aproximadas, lidas visualmente dos mapas de viés (erro_vies.png /
# vies_el_nino.png / vies_la_nina.png)
REGIONS = {
    "Norte (0-10N, 75-50O)": dict(lat_min=0, lat_max=10, lon_min=-75, lon_max=-50),
    "Centro-Sul (30-15S, 65-45O)": dict(lat_min=-30, lat_max=-15, lon_min=-65, lon_max=-45),
}


def main():
    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    clim = build_climatology(tp, max_year=None)
    lat = tp["lat"].values
    lon = tp["lon"].values
    time_vals = pd.to_datetime(tp["time"].values)

    region_masks = {}
    for name, box in REGIONS.items():
        lat_mask = (lat >= box["lat_min"]) & (lat <= box["lat_max"])
        lon_mask = (lon >= box["lon_min"]) & (lon <= box["lon_max"])
        region_masks[name] = np.ix_(lat_mask, lon_mask)

    domain_anom = np.empty(len(time_vals))
    region_anom = {name: np.empty(len(time_vals)) for name in REGIONS}

    for i, t in enumerate(time_vals):
        full_anom = tp.isel(time=i).values - clim[t.month]
        domain_anom[i] = float(np.mean(full_anom))
        for name, idx in region_masks.items():
            region_anom[name][i] = float(np.mean(full_anom[idx]))

    df = pd.DataFrame({"date": time_vals, "domínio inteiro": domain_anom, **region_anom})
    df["year"] = df["date"].dt.year
    annual = df.groupby("year").mean(numeric_only=True)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(annual.index, annual["domínio inteiro"], color="#898781", linewidth=2, label="Média de TODO o domínio", zorder=3)
    ax.plot(annual.index, annual["Norte (0-10N, 75-50O)"], color="#2a78d6", linewidth=1.6, label="Só região Norte")
    ax.plot(annual.index, annual["Centro-Sul (30-15S, 65-45O)"], color="#e34948", linewidth=1.6, label="Só região Centro-Sul")
    ax.axhline(0, color="#c3c2b7", linewidth=1)
    ax.axvspan(2016, 2022, color="#eb6834", alpha=0.08, label="janela 2016-2022")
    ax.set_title("Por que a média do continente esconde o que acontece região por região")
    ax.set_xlabel("Ano")
    ax.set_ylabel("anomalia de precipitação (mm/dia)")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / "dipolo_regioes.png", dpi=130)
    print(f"salvo: {OUT_DIR / 'dipolo_regioes.png'}")

    print("\nMédia 2016-2022:")
    print(annual.loc[2016:2022].mean().round(3))
    print("\nDesvio padrão 2016-2022 (quanto cada série varia ano a ano):")
    print(annual.loc[2016:2022].std().round(3))
    print("\nDesvio padrão 1940-2015 (comparação histórica):")
    print(annual.loc[1940:2015].std().round(3))


if __name__ == "__main__":
    main()
