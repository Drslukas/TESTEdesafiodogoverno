"""Leitor de snapshots NOAA/PSL; somente observações anteriores ao mês alvo."""
from pathlib import Path
import numpy as np
import pandas as pd

NAMES = ('soi', 'nino12', 'nino3', 'nino4')

def read_indices(directory):
    output = {}
    for name in NAMES:
        path = Path(directory) / f'{name}.data'
        if not path.exists():
            raise FileNotFoundError(f'Índice {path} ausente. Rode download_indices.py.')
        values = {}
        for line in path.read_text(encoding='utf-8').splitlines():
            tokens = line.split()
            if len(tokens) != 13 or not tokens[0].isdigit() or len(tokens[0]) != 4:
                continue
            year = int(tokens[0])
            for month, token in enumerate(tokens[1:], 1):
                value = float(token)
                values[pd.Timestamp(year, month, 1)] = value if value > -90 else np.nan
        if not values:
            raise ValueError(f'Índice vazio: {path}')
        output[name] = pd.Series(values, dtype='float32').sort_index()
    return output

def causal_values(series, target, history=3):
    target = pd.Timestamp(target)
    result = {}
    for name, values in series.items():
        for lag in range(1, history + 1):
            month = target - pd.DateOffset(months=lag)
            value = values.get(month, np.nan)
            if not np.isfinite(value):
                raise ValueError(f'Índice {name} ausente em {month:%Y-%m}')
            result[f'{name}_lag{lag}'] = np.float32(value)
    return result
