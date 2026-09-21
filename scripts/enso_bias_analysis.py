"""
Junta o índice ONI (El Niño/La Niña) com os dados de precipitação e testa se
o viés espacial do baseline de climatologia (visto em erro_vies.png) muda de
sinal dependendo da fase ENSO do mês-alvo.

Classificação (simplificada - sem a regra de persistência de 5 estações
consecutivas da NOAA, só o valor do ONI naquele mês):
  El Niño: ONI >= +0.5
  La Niña: ONI <= -0.5
  Neutro:  entre os dois

Uso:
    .venv/bin/python scripts/enso_bias_analysis.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from baseline_climatology import DATA_DIR, build_climatology, target_calendar_month

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"
ONI_PATH = Path(__file__).resolve().parent.parent / "data" / "oni.ascii.txt"

# mês "central" de cada estação móvel de 3 meses do ONI (convenção NOAA: o
# ano listado na linha é o ano do mês central, exceto DJF que usa dez do ano
# anterior + jan/fev do próprio ano listado — jan já é o ano listado).
SEASON_CENTER_MONTH = {
    "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6,
    "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12,
}

CMAP_DIV = LinearSegmentedColormap.from_list(
    "div_blue_red", ["#0d366b", "#2a78d6", "#f0efec", "#eb6834", "#e34948"]
)


def load_oni_monthly() -> pd.Series:
    """Retorna uma Series indexada por (year, month) -> valor ONI."""
    df = pd.read_csv(ONI_PATH, sep=r"\s+")
    df["month"] = df["SEAS"].map(SEASON_CENTER_MONTH)
    df = df.set_index(["YR", "month"])["ANOM"]
    return df


def classify(oni_value: float) -> str:
    if oni_value >= 0.5:
        return "El Niño"
    if oni_value <= -0.5:
        return "La Niña"
    return "Neutro"


def main():
    oni = load_oni_monthly()

    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    tp_alvo = xr.open_dataset(DATA_DIR / "treino_tp_alvo.nc")["tp_alvo"]
    lat = tp["lat"].values
    lon = tp["lon"].values

    val_start, val_end = 2016, 2022
    clim_val = build_climatology(tp, max_year=val_start - 1)

    time_vals = tp["time"].values
    val_mask = (tp["time"].dt.year >= val_start) & (tp["time"].dt.year <= val_end)
    val_idx = np.where(val_mask.values)[0]

    print(f"Classificação ENSO dos {len(val_idx)} meses-alvo em {val_start}-{val_end}:")
    phases, errors = [], []
    for idx in val_idx:
        true = tp_alvo.isel(time=idx).values
        if np.isnan(true).all():
            continue
        month_m_ts = pd.Timestamp(time_vals[idx])
        # alvo é o mês M+1 - a fase ENSO relevante é a do mês sendo previsto, não a do mês de entrada
        target_ts = month_m_ts + pd.DateOffset(months=1)
        tmonth = target_calendar_month(month_m_ts.month)
        assert tmonth == target_ts.month

        key = (target_ts.year, target_ts.month)
        if key not in oni.index:
            continue  # sem ONI pra esse mês (não deve acontecer em 2016-2022)
        phase = classify(float(oni.loc[key]))
        pred = clim_val[tmonth]
        phases.append(phase)
        errors.append(pred - true)
        print(f"  {target_ts.year}-{target_ts.month:02d}: ONI={float(oni.loc[key]):+.2f} -> {phase}")

    phases = np.array(phases)
    errors = np.stack(errors)

    print("\nContagem de meses por fase:")
    for phase in ("El Niño", "La Niña", "Neutro"):
        print(f"  {phase}: {int((phases == phase).sum())} meses")

    # --- mapas de viés por fase ---
    bias_all_max = float(np.percentile(np.abs(np.mean(errors, axis=0)), 98))
    for phase in ("El Niño", "La Niña"):
        mask = phases == phase
        n = int(mask.sum())
        if n < 3:
            print(f"  [aviso] poucos meses de {phase} ({n}) - pulando mapa")
            continue
        bias_phase = np.mean(errors[mask], axis=0)

        fig, ax = plt.subplots(figsize=(7, 7.5))
        norm = TwoSlopeNorm(vcenter=0, vmin=-bias_all_max, vmax=bias_all_max)
        mesh = ax.pcolormesh(lon, lat, bias_phase, cmap=CMAP_DIV, norm=norm, shading="auto")
        ax.set_title(
            f"Viés do baseline em meses de {phase} ({val_start}-{val_end}, n={n})\n"
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
        fname = OUT_DIR / f"vies_{'el_nino' if phase == 'El Niño' else 'la_nina'}.png"
        fig.savefig(fname, dpi=130)
        plt.close(fig)
        print(f"  salvo: {fname}")


if __name__ == "__main__":
    main()
