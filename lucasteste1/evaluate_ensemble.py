"""Escolhe um peso fixo somente se ganhar em todos os blocos históricos."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

RESULTS = Path(__file__).resolve().parent / 'results'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'nmme_gate.json'
FOLDS = ('2015full', '2021', '2022')
WEIGHTS = (0.25, 0.5, 0.75, 1.0)

def rmse(y, p):
    return float(np.sqrt(np.mean((y.astype('float64') - p.astype('float64')) ** 2)))

def load(fold, nmme):
    suffix = '_nmme_geoss2s' if nmme else ''
    path = RESULTS / f'E00_fold{fold}_s8_l224_r700_lr0.025_years30_atm_three_ocean{suffix}_predictions.npz'
    with np.load(path) as data:
        return {k: data[k].copy() for k in ('prediction', 'truth', 'time', 'lat', 'lon')}

def main():
    records = {}
    for fold in FOLDS:
        base, nmme = load(fold, False), load(fold, True)
        for name in ('truth', 'time', 'lat', 'lon'):
            if not np.array_equal(base[name], nmme[name]):
                raise ValueError(f'{fold}: {name} incompatível entre modelos.')
        npoints = len(base['lat'])*len(base['lon'])
        dates = pd.DatetimeIndex(base['time'])
        if len(dates)*npoints != len(base['truth']):
            raise ValueError('Formato de previsão inválido.')
        second = np.repeat(dates.year == dates.year.max(), npoints)
        records[fold] = (base, nmme, second)
    choices = []
    for weight in WEIGHTS:
        metrics = {}
        passed = True
        total_sse = total_n = 0
        for fold, (base, nmme, second) in records.items():
            y = base['truth']
            original = base['prediction']
            candidate = np.maximum(0, (1-weight)*original + weight*nmme['prediction'])
            base_score, candidate_score = rmse(y, original), rmse(y, candidate)
            second_base, second_candidate = rmse(y[second], original[second]), rmse(y[second], candidate[second])
            improved = candidate_score < base_score and second_candidate < second_base
            passed &= improved
            metrics[fold] = {'ocean_rmse': base_score, 'blend_rmse': candidate_score,
                             'second_year_ocean_rmse': second_base,
                             'second_year_blend_rmse': second_candidate, 'improved': improved}
            if fold != '2022':
                total_sse += np.sum((candidate.astype('float64')-y)**2)
                total_n += len(y)
        choices.append({'nmme_weight': weight, 'passed': passed,
                        'independent_pooled_rmse': float(np.sqrt(total_sse/total_n)),
                        'folds': metrics})
    eligible = [item for item in choices if item['passed']]
    selected = min(eligible, key=lambda item: item['independent_pooled_rmse']) if eligible else None
    report = {'passed': selected is not None, 'selected_weight': selected['nmme_weight'] if selected else None,
              'choices': choices, 'note': 'Pesos predefinidos; seleção usa validação histórica. 2022 também é subconjunto de 2021–22.'}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'selected_weight': report['selected_weight'],
                      'scores': [{k: v for k, v in item.items() if k != 'folds'} for item in choices]}, indent=2))

if __name__ == '__main__':
    main()
