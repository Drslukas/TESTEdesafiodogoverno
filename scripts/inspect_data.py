"""
Inspeciona os arquivos .nc/.csv do desafio WORCAP 2026 (precipitação AmSul).

Para cada arquivo, reporta: variáveis, dimensões, shape, dtype, range de
lat/lon/time, e estatísticas (min/max/mean/std/%NaN) por variável de dados —
porque a documentação (docs/DESAFIO_KAGGLE_OVERVIEW.md, seção 3) avisa
explicitamente que as unidades ERA5 "de fábrica" NÃO estão confirmadas pela
página da competição e devem ser verificadas empiricamente.

Uso:
    .venv/bin/python scripts/inspect_data.py
    .venv/bin/python scripts/inspect_data.py --file treino_tp.nc   # só um arquivo
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "previsao-climatica-de-precipitacao-sobre-a-america-do-sul"

NC_FILES = [
    "treino_tp.nc",
    "treino_tp_alvo.nc",
    "treino_t2.nc",
    "treino_cloud_cover.nc",
    "treino_surface_pressure.nc",
    "treino_shum_850.nc",
    "treino_rel_hum_850.nc",
    "treino_temperature_850.nc",
    "treino_geopotential_850.nc",
    "treino_u_850.nc",
    "treino_v_850.nc",
    "teste_features.nc",
]


def fmt(v, nd=4):
    if v is None:
        return "n/a"
    if isinstance(v, float) and np.isnan(v):
        return "NaN"
    return f"{v:.{nd}g}"


def inspect_coords(ds: xr.Dataset) -> None:
    known = ("lat", "latitude", "lon", "longitude", "time")
    for name in known:
        if name not in ds.coords:
            continue
        c = ds.coords[name]
        vals = c.values
        print(f"  coord `{name}`: shape={vals.shape} dtype={c.dtype}")
        if name in ("lat", "latitude"):
            ascending = bool(np.all(np.diff(vals) > 0))
            print(f"    range=[{vals.min():.3f}, {vals.max():.3f}] ascending={ascending}")
        elif name in ("lon", "longitude"):
            print(f"    range=[{vals.min():.3f}, {vals.max():.3f}]")
        elif name == "time":
            try:
                print(f"    range=[{pd.Timestamp(vals.min())}, {pd.Timestamp(vals.max())}] n={len(vals)}")
            except Exception:
                print(f"    range=[{vals.min()}, {vals.max()}] n={len(vals)}")

    # Auxiliary/non-dimension coords (e.g. teste_features.nc's `lag_meses`,
    # `time_origem`) live in ds.coords but aren't dimension coords, so the
    # loop above misses them — surface them separately or they go unreported.
    extra = [n for n in ds.coords if n not in known]
    for name in extra:
        c = ds.coords[name]
        vals = c.values
        print(f"  coord `{name}` (aux): shape={vals.shape} dtype={c.dtype}")
        if np.issubdtype(c.dtype, np.number):
            print(f"    range=[{vals.min()}, {vals.max()}] unique={len(np.unique(vals))}")
        elif np.issubdtype(c.dtype, np.datetime64):
            print(f"    range=[{pd.Timestamp(vals.min())}, {pd.Timestamp(vals.max())}]")
        else:
            print(f"    values={vals[:5]}{'...' if len(vals) > 5 else ''}")


def inspect_variable(ds: xr.Dataset, var: str) -> None:
    da = ds[var]
    arr = da.values  # loads this variable into memory (single var, ~50-300MB — fine one at a time)
    n_total = arr.size
    nan_mask = np.isnan(arr) if np.issubdtype(arr.dtype, np.floating) else np.zeros_like(arr, dtype=bool)
    n_nan = int(nan_mask.sum())
    valid = arr[~nan_mask] if n_nan else arr

    print(f"  var `{var}`: dims={da.dims} shape={da.shape} dtype={da.dtype}")
    units = da.attrs.get("units")
    long_name = da.attrs.get("long_name")
    if units or long_name:
        print(f"    attrs: units={units!r} long_name={long_name!r}")
    if valid.size:
        print(
            f"    min={fmt(float(valid.min()))} max={fmt(float(valid.max()))} "
            f"mean={fmt(float(valid.mean()))} std={fmt(float(valid.std()))} "
            f"nan={n_nan}/{n_total} ({100*n_nan/n_total:.2f}%)"
        )
    else:
        print("    all-NaN")

    # NaN pattern along time, if there's a time dim — useful to confirm the
    # documented "last month is NaN" behavior on treino_tp_alvo.nc, and
    # "tp_alvo is entirely NaN" on teste_features.nc.
    if "time" in da.dims and n_nan:
        time_axis = da.dims.index("time")
        nan_per_t = nan_mask.sum(axis=tuple(i for i in range(arr.ndim) if i != time_axis))
        full_nan_steps = np.where(nan_per_t == nan_per_t.max())[0] if nan_per_t.max() > 0 else []
        cell_count = arr.size // arr.shape[time_axis]
        fully_nan_t = [int(i) for i in np.where(nan_per_t == cell_count)[0]]
        if fully_nan_t:
            print(f"    time steps fully NaN: {len(fully_nan_t)} (indices: {fully_nan_t[:5]}{'...' if len(fully_nan_t) > 5 else ''})")


def inspect_file(path: Path) -> None:
    print(f"\n{'=' * 70}\n{path.name}  ({path.stat().st_size / 1e6:.1f} MB)\n{'=' * 70}")
    try:
        ds = xr.open_dataset(path)
    except Exception as e:
        print(f"  ERROR opening file: {e}")
        return

    print(f"  data_vars: {list(ds.data_vars)}")
    inspect_coords(ds)
    for var in ds.data_vars:
        inspect_variable(ds, var)
    ds.close()


def inspect_sample_submission(path: Path) -> None:
    print(f"\n{'=' * 70}\n{path.name}  ({path.stat().st_size / 1e6:.1f} MB)\n{'=' * 70}")
    df = pd.read_csv(path)
    print(f"  shape={df.shape} columns={list(df.columns)}")
    print(f"  dtypes:\n{df.dtypes.to_string()}")
    print(f"  head:\n{df.head(3).to_string(index=False)}")
    if "id" in df.columns:
        parts = df["id"].str.split("_", expand=True)
        if parts.shape[1] >= 4:
            years = parts[0].unique()
            months = parts[1].unique()
            print(f"  id years={sorted(years)} months={sorted(months)}")
    if "tp_mm_day" in df.columns:
        print(f"  tp_mm_day: unique values={df['tp_mm_day'].unique()[:5]} (placeholder check)")
    dup = df["id"].duplicated().sum() if "id" in df.columns else None
    print(f"  duplicated ids: {dup}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="inspecionar apenas um arquivo (nome, ex.: treino_tp.nc)")
    parser.add_argument("--data-dir", default=str(DATA_DIR))
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Data dir not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    files = [args.file] if args.file else NC_FILES
    for fname in files:
        fpath = data_dir / fname
        if not fpath.exists():
            print(f"\n[SKIP] {fname} not found at {fpath}")
            continue
        inspect_file(fpath)

    if not args.file:
        sub_path = data_dir / "sample_submission.csv"
        if sub_path.exists():
            inspect_sample_submission(sub_path)


if __name__ == "__main__":
    main()
