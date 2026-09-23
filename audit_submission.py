"""Verifica integridade e resume previsões; não calcula RMSE sem alvo."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

EXPECTED_HASH = '2b5084b0bb00131948e1cba3720b7e96774b0f5b10d96119646c0508fdd8782b'

def audit(path, reference=None, official=True):
    path = Path(path)
    frame = pd.read_csv(path, dtype={'id': str})
    if list(frame.columns) != ['id', 'tp_mm_day']:
        raise ValueError('Colunas devem ser id,tp_mm_day, nessa ordem.')
    if frame.id.isna().any() or frame.id.duplicated().any():
        raise ValueError('IDs ausentes ou duplicados.')
    parts = frame.id.str.extract(r'^(\d{4})_(\d{2})_(-?\d+\.\d{2})_(-?\d+\.\d{2})$')
    if parts.isna().any().any():
        raise ValueError('Formato de ID inválido.')
    values = frame.tp_mm_day.to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError('Previsões negativas ou não finitas.')
    if official:
        expected = pd.Index([
            f'{year}_{month:02d}_{la / 4:.2f}_{lo / 4:.2f}'
            for year in (2023, 2024) for month in range(1, 13)
            for la in range(-240, 61) for lo in range(-360, -99)
        ])
        if len(frame) != len(expected) or not expected.isin(frame.id).all():
            raise ValueError('IDs não cobrem exatamente a grade oficial 2023–2024.')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    report = {'file': str(path.resolve()), 'sha256': digest,
              'matches_previous_winner': digest == EXPECTED_HASH,
              'rows': len(frame), 'min': float(values.min()), 'max': float(values.max()),
              'mean': float(values.mean()), 'zero_fraction': float((values == 0).mean())}
    frame['month'] = frame.id.str.slice(0, 7)
    report['monthly'] = frame.groupby('month').tp_mm_day.agg(['count', 'mean', 'std', 'min', 'max']).to_dict('index')
    if reference:
        ref = pd.read_csv(reference, dtype={'id': str}).set_index('id')
        if not ref.index.is_unique or set(ref.index) != set(frame.id):
            raise ValueError('Referência tem IDs diferentes ou duplicados.')
        delta = values - ref.loc[frame.id, 'tp_mm_day'].to_numpy()
        if not np.isfinite(delta).all():
            raise ValueError('Referência contém valores não finitos.')
        report['prediction_difference_rmse_NOT_accuracy'] = float(np.sqrt(np.mean(delta ** 2)))
        report['mean_difference'] = float(delta.mean())
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv')
    parser.add_argument('--reference')
    parser.add_argument('--output', default='outputs/audit.json')
    args = parser.parse_args()
    result = audit(args.csv, args.reference)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'monthly'}, indent=2))
