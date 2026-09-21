"""
Série temporal de anomalia de precipitação (proxy data-driven pra ENSO).

Não usa nenhum índice externo (ONI) — só os próprios dados de treino. Pra cada
mês, calcula: chuva real - climatologia daquele mês do calendário (média
histórica 1940-2022), depois tira a média espacial (todo o domínio) e anual.

Isso NÃO é o índice ONI oficial, é um proxy: mostra quais anos tiveram chuva
mais anômala na própria grade do desafio, sem depender de nenhuma fonte
externa. Serve pra ver, com dados, se 2016-2022 realmente se destaca — e
depois cruzar isso com o índice ONI de verdade quando ele estiver disponível
(ver scripts/join_oni.py).

Uso:
    .venv/bin/python scripts/anomaly_timeseries.py
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


def main():
    tp = xr.open_dataset(DATA_DIR / "treino_tp.nc")["tp"]
    clim = build_climatology(tp, max_year=None)  # climatologia com TODO o histórico

    time_vals = pd.to_datetime(tp["time"].values)
    anomalies = np.empty(len(time_vals))
    for i, t in enumerate(time_vals):
        anomalies[i] = float(np.mean(tp.isel(time=i).values - clim[t.month]))

    df = pd.DataFrame({"date": time_vals, "anomaly": anomalies})
    df["year"] = df["date"].dt.year
    annual = df.groupby("year")["anomaly"].mean()

    # ranking: anos mais anômalos (positivo=mais chuva que a média histórica,
    # negativo=menos) em todo o período 1940-2022
    ranked = annual.abs().sort_values(ascending=False)
    print("Top 15 anos mais anômalos (1940-2022), |anomalia| espacial média:")
    for year in ranked.index[:15]:
        marker = "  <-- janela de validação (2016-2022)" if 2016 <= year <= 2022 else ""
        print(f"  {year}: {annual[year]:+.3f} mm/dia{marker}")

    print(f"\nMédia da anomalia anual em 2016-2022: {annual.loc[2016:2022].mean():+.3f} mm/dia")
    print(f"Média da anomalia anual em 1940-2015: {annual.loc[1940:2015].mean():+.3f} mm/dia")
    print(f"Desvio padrão da anomalia anual (todo o histórico): {annual.std():.3f} mm/dia")

    fig, ax = plt.subplots(figsize=(11, 4.5))
    colors = ["#eb6834" if 2016 <= y <= 2022 else "#2a78d6" for y in annual.index]
    ax.bar(annual.index, annual.values, color=colors, width=0.8)
    ax.axhline(0, color="#898781", linewidth=1)
    ax.set_title("Anomalia anual de precipitação (média espacial, vs. climatologia 1940-2022)")
    ax.set_xlabel("Ano")
    ax.set_ylabel("anomalia (mm/dia)")
    ax.text(0.99, 0.02, "laranja = janela de validação 2016-2022", transform=ax.transAxes,
            ha="right", fontsize=9, color="#52514e")
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / "anomalia_anual.png", dpi=130)
    print(f"\nsalvo: {OUT_DIR / 'anomalia_anual.png'}")


if __name__ == "__main__":
    main()
