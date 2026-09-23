"""Parse NOAA files; monthly lags use observation month, not release vintage."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from climate_indices import read_indices as read_psl_snapshot

FILES = {'soi': 'soi.txt', 'nino12': 'nina1.anom.data.txt',
         'nino3': 'nina3.anom.data.txt', 'nino4': 'nina4.anom.data.txt'}

def read_indices():
    return read_psl_snapshot(Path(__file__).resolve().parents[1] / 'data' / 'indices')

def add_indices(frame, dates, npoints, series):
    for name, data in series.items():
        for lag in (1, 2, 3):
            source = dates - pd.DateOffset(months=lag)
            assert (source < dates).all()
            values = data.reindex(source).to_numpy(dtype='float32')
            if not np.isfinite(values).all():
                raise ValueError(f'Missing historical values: {name} lag {lag}')
            frame[f'{name}_lag{lag}'] = np.repeat(values, npoints)
    return frame
