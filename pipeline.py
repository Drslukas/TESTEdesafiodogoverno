"""Pipeline temporal residual ERA5. Datas de treino são origens; teste usa alvos."""
import argparse
from contextlib import ExitStack
import gc
import hashlib
import json
from pathlib import Path
import platform
from functools import lru_cache

import lightgbm as lgb
import numpy as np
import pandas as pd
import xarray as xr

ATMOS = ('t2', 'cloud_cover', 'surface_pressure', 'shum_850',
         'rel_hum_850', 'temperature_850', 'geopotential_850', 'u_850', 'v_850')

def rmse(y, p):
    y, p = np.asarray(y, dtype=np.float64), np.asarray(p, dtype=np.float64)
    if y.size == 0 or not np.isfinite(y).all() or not np.isfinite(p).all():
        raise ValueError('RMSE exige alvo e previsão finitos e não vazios.')
    return float(np.sqrt(np.mean((y - p) ** 2)))

def save_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str), encoding='utf-8')

class Data:
    def __init__(self, root):
        self.stack = ExitStack()
        root = Path(root)
        matches = list(root.rglob('treino_tp_alvo.nc'))
        if len(matches) != 1:
            raise ValueError(f'Esperado um treino_tp_alvo.nc em {root}; encontrados {len(matches)}.')
        self.root = matches[0].parent
        self.indices_series = None
        try:
            self.y = self.open('treino_tp_alvo.nc')['tp_alvo'].transpose('time', 'lat', 'lon')
            self.fields = {n: self.open(f'treino_{n}.nc')[n].transpose('time', 'lat', 'lon') for n in ATMOS}
            self.test = self.open('teste_features.nc')
            self.times = pd.DatetimeIndex(self.y.time.values)
            self.targets = self.times + pd.offsets.MonthBegin(1)
            self.lat, self.lon = self.y.lat.values, self.y.lon.values
            if not self.times.equals(pd.date_range(self.times[0], periods=len(self.times), freq='MS')):
                raise ValueError('Treino deve ser mensal contínuo e ordenado.')
            if self.targets.max() > pd.Timestamp('2023-01-01'):
                raise ValueError('Treino contém datas além do período oficial permitido.')
            for field in self.fields.values():
                for c in ('time', 'lat', 'lon'):
                    if not np.array_equal(field[c].values, self.y[c].values):
                        raise ValueError(f'Coordenada {c} incompatível entre arquivos.')
            for c in ('lat', 'lon'):
                if not np.array_equal(self.test[c].values, self.y[c].values):
                    raise ValueError('Grade de teste incompatível.')
            test_times = pd.DatetimeIndex(self.test.time.values)
            if not test_times.equals(pd.date_range('2023-01-01', '2024-12-01', freq='MS')):
                raise ValueError('Esperados 24 meses de teste, 2023–2024.')
            expected_origin = test_times - pd.offsets.MonthBegin(1)
            if 'time_origem' not in self.test or not np.array_equal(self.test.time_origem.values, expected_origin.values):
                raise ValueError('time_origem deve ser exatamente T-1.')
        except Exception:
            self.close()
            raise

    def open(self, filename):
        return self.stack.enter_context(xr.open_dataset(self.root / filename))

    def close(self):
        self.atmospheric.cache_clear()
        self.stack.close()

    def indices(self, start, end):
        # O último tp_alvo é desconhecido (janeiro/2023): jamais usado.
        return np.flatnonzero((self.targets >= pd.Timestamp(start)) &
                              (self.targets < pd.Timestamp(end)) &
                              (self.targets <= pd.Timestamp('2022-12-01')) &
                              (np.arange(len(self.times)) >= 2))

    def climatology(self, indices, stride):
        fields = []
        for month in range(1, 13):
            selected = indices[self.targets[indices].month == month]
            if not len(selected):
                raise ValueError(f'Sem histórico para mês {month}.')
            field = self.y.isel(time=selected, lat=slice(None, None, stride),
                                lon=slice(None, None, stride)).mean('time').values.astype('float32')
            if not np.isfinite(field).all():
                raise ValueError('Climatologia não finita.')
            fields.append(field)
        return np.stack(fields)

    @lru_cache(maxsize=128)
    def atmospheric(self, name, date, stride):
        # Consulta pelo mês de origem, inclusive na transição dez/2022 -> jan/2023.
        if date in self.times:
            field = self.fields[name].sel(time=date)
        else:
            origins = pd.DatetimeIndex(self.test.time_origem.values)
            location = origins.get_indexer([date])[0]
            if location < 0:
                raise ValueError(f'Origem ausente: {date}, {name}')
            field = self.test[name].isel(time=location).transpose('lat', 'lon')
        return field.isel(lat=slice(None, None, stride), lon=slice(None, None, stride)).values.astype('float32')

    def frame(self, target, climate, stride, history):
        la, lo = np.meshgrid(self.lat[::stride], self.lon[::stride], indexing='ij')
        base = climate[target.month - 1].ravel()
        cols = {'lat': la.ravel(), 'lon': lo.ravel(), 'climatology': base,
                'month_sin': np.full(base.size, np.sin(2 * np.pi * target.month / 12)),
                'month_cos': np.full(base.size, np.cos(2 * np.pi * target.month / 12))}
        for lag in range(1, history + 1):
            date = target - pd.offsets.MonthBegin(lag)
            values = {n: self.atmospheric(n, date, stride).ravel() for n in ATMOS}
            cols.update({f'{n}_lag{lag}': a for n, a in values.items()})
            cols[f'qu_lag{lag}'] = values['shum_850'] * values['u_850']
            cols[f'qv_lag{lag}'] = values['shum_850'] * values['v_850']
            cols[f'wind_lag{lag}'] = np.hypot(values['u_850'], values['v_850'])
        if self.indices_series is not None:
            from climate_indices import causal_values
            cols.update({name: np.full(base.size, value, dtype='float32')
                         for name, value in causal_values(self.indices_series, target).items()})
        result = pd.DataFrame(cols, dtype='float32')
        if not np.isfinite(result.to_numpy()).all():
            raise ValueError(f'Features não finitas no alvo {target}.')
        return result

    def training(self, indices, climate, stride, history):
        frames, residuals = [], []
        for i in indices:
            frame = self.frame(self.targets[i], climate, stride, history)
            y = self.y.isel(time=int(i), lat=slice(None, None, stride),
                            lon=slice(None, None, stride)).values.ravel().astype('float32')
            if not np.isfinite(y).all():
                raise ValueError(f'Alvo ausente em {self.targets[i]}.')
            frames.append(frame)
            residuals.append(y - frame.climatology.to_numpy())
        if not frames:
            raise ValueError('Janela de treino vazia.')
        return pd.concat(frames, ignore_index=True), np.concatenate(residuals)

def fit(data, indices, climate, args):
    X, y = data.training(indices, climate, args.stride, args.history)
    print(f'Treino: {len(indices)} meses, {len(X):,} linhas, {X.shape[1]} features.', flush=True)
    model = lgb.train(dict(objective='regression', metric='rmse',
                          learning_rate=args.lr, num_leaves=args.leaves,
                          min_data_in_leaf=100, feature_fraction=.85,
                          bagging_fraction=.85, bagging_freq=1, max_bin=127,
                          num_threads=args.threads, verbosity=-1, seed=42,
                          deterministic=True, force_col_wise=True),
                      lgb.Dataset(X, label=y), num_boost_round=args.rounds)
    del X, y
    gc.collect()
    return model

def settings(args):
    return {k: getattr(args, k) for k in ('stride', 'history', 'train_years', 'leaves', 'rounds', 'lr', 'ocean')}

def validate(data, args):
    reports = []
    for year in args.folds:
        first = pd.Timestamp(year, 1, 1)
        end = first + pd.DateOffset(years=2)
        train = data.indices(first - pd.DateOffset(years=args.train_years), first)
        valid = data.indices(first, end)
        if len(valid) != 24:
            raise ValueError(f'Fold {year} exige 24 meses observados.')
        climate = data.climatology(train, args.stride)
        model = fit(data, train, climate, args)
        truth, baseline, prediction, dates, monthly = [], [], [], [], []
        for i in valid:
            target = data.targets[i]
            X = data.frame(target, climate, args.stride, args.history)
            y = data.y.isel(time=int(i), lat=slice(None, None, args.stride),
                            lon=slice(None, None, args.stride)).values.ravel()
            base = X.climatology.to_numpy()
            pred = np.maximum(0, base + model.predict(X))
            truth.append(y); baseline.append(base); prediction.append(pred)
            dates.append(str(target.date()))
            monthly.append({'target': str(target.date()), 'climatology_rmse': rmse(y, base), 'model_rmse': rmse(y, pred)})
        y, b, p = map(np.stack, (truth, baseline, prediction))
        result = {'fold': year, 'train_last_target': str(data.targets[train[-1]].date()),
                  'climatology_rmse': rmse(y, b), 'model_rmse': rmse(y, p),
                  'second_year_climatology_rmse': rmse(y[12:], b[12:]),
                  'second_year_model_rmse': rmse(y[12:], p[12:]), 'monthly': monthly}
        # Pesos predefinidos: a tabela é diagnóstico, não validação independente do peso escolhido.
        result['exploratory_blends'] = {str(w): rmse(y, (1-w)*b + w*p) for w in (.5, .75, 1.)}
        np.savez_compressed(Path(args.output) / f'fold_{year}.npz', truth=y, climatology=b,
                            prediction=p, dates=dates, lat=data.lat[::args.stride], lon=data.lon[::args.stride])
        save_json(Path(args.output) / f'fold_{year}.json', result)
        print(json.dumps({k: v for k, v in result.items() if k != 'monthly'}, indent=2), flush=True)
        reports.append(result)
    save_json(Path(args.output) / 'validation.json', {'settings': settings(args), 'folds': reports,
              'note': 'Comparação com climatologia; não reproduz o modelo ocean 1.69874. Grade subamostrada é triagem.'})

def predict(data, args):
    validation = json.loads(Path(args.validation).read_text(encoding='utf-8'))
    if validation['settings'] != settings(args):
        raise ValueError('Configuração deve ser idêntica à validação informada.')
    folds = validation['folds']
    if len(folds) < 3 or len({f['fold'] for f in folds}) != len(folds):
        raise ValueError('Exigidos pelo menos três folds distintos.')
    if any(f['model_rmse'] >= f['climatology_rmse'] or
           f['second_year_model_rmse'] >= f['second_year_climatology_rmse'] for f in folds):
        raise ValueError('Candidato não superou climatologia em todos os blocos e segundos anos.')
    indices = data.indices(pd.Timestamp('2023-01-01') - pd.DateOffset(years=args.train_years), '2023-01-01')
    climate = data.climatology(indices, args.stride)
    model = fit(data, indices, climate, args)
    model.save_model(str(Path(args.output) / 'model.txt'))
    # Climatologia na grade completa, sem interpolar chuva nem usar alvo oculto.
    full_climate = data.climatology(indices, 1)
    np.save(Path(args.output) / 'climatology.npy', full_climate)
    sample = pd.read_csv(data.root / 'sample_submission.csv', dtype={'id': str})
    if list(sample.columns) != ['id', 'tp_mm_day'] or sample.id.duplicated().any():
        raise ValueError('sample_submission inválido.')
    predictions = []
    lat, lon = np.meshgrid(data.lat, data.lon, indexing='ij')
    for target in pd.DatetimeIndex(data.test.time.values):
        X = data.frame(target, full_climate, 1, args.history)
        pred = np.maximum(0, X.climatology.to_numpy() + model.predict(X))
        ids = [f'{target.year}_{target.month:02d}_{a:.2f}_{b:.2f}' for a, b in zip(lat.ravel(), lon.ravel())]
        predictions.append(pd.Series(pred, index=ids))
    predictions = pd.concat(predictions)
    if not predictions.index.is_unique or set(sample.id) != set(predictions.index):
        raise ValueError('IDs previstos não coincidem exatamente com sample_submission.')
    sample['tp_mm_day'] = predictions.loc[sample.id].to_numpy()
    if not np.isfinite(sample.tp_mm_day).all():
        raise ValueError('Previsão inválida.')
    output = Path(args.output) / 'submission_candidate.csv'
    sample.to_csv(output, index=False)
    from audit_submission import audit
    save_json(Path(args.output) / 'submission_audit.json', audit(output, args.reference))
    save_json(Path(args.output) / 'manifest.json', {
        'settings': settings(args), 'validation': validation,
        'python': platform.python_version(), 'lightgbm': lgb.__version__,
        'train_last_target': str(data.targets[indices[-1]].date()),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'indices_snapshot': json.loads((Path(args.indices_dir) / 'manifest.json').read_text(encoding='utf-8')) if args.ocean else None,
        'csv_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'warning': 'Candidato novo; ganho contra submissão ocean não demonstrado. Sem envio automático.'})
    print('Candidato gerado:', output)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'predict'])
    parser.add_argument('--data', default='data')
    parser.add_argument('--output', default='outputs/candidate')
    parser.add_argument('--stride', type=int, default=8)
    parser.add_argument('--history', type=int, choices=[1, 3], default=3)
    parser.add_argument('--train-years', type=int, default=30)
    parser.add_argument('--leaves', type=int, default=224)
    parser.add_argument('--rounds', type=int, default=700)
    parser.add_argument('--lr', type=float, default=.025)
    parser.add_argument('--threads', type=int, default=4)
    parser.add_argument('--folds', type=int, nargs='+', default=[2015, 2019, 2021])
    parser.add_argument('--validation', default='outputs/candidate/validation.json')
    parser.add_argument('--ocean', action='store_true', help='Inclui SOI e Niño 1+2/3/4 com lags de 1–3 meses')
    parser.add_argument('--indices-dir', default='data/indices')
    parser.add_argument('--reference')
    args = parser.parse_args()
    if min(args.stride, args.train_years, args.rounds, args.threads) < 1 or args.leaves < 2 or args.lr <= 0:
        parser.error('Parâmetros numéricos inválidos.')
    Path(args.output).mkdir(parents=True, exist_ok=True)
    data = Data(args.data)
    try:
        if args.ocean:
            from climate_indices import read_indices
            data.indices_series = read_indices(args.indices_dir)
        (validate if args.command == 'validate' else predict)(data, args)
    finally:
        data.close()

if __name__ == '__main__':
    main()
