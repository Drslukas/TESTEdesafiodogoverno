"""Testes sintéticos: verificam o código, não a qualidade meteorológica."""
import tempfile
import unittest
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
import xarray as xr
from pipeline import ATMOS, Data, fit, rmse
from audit_submission import audit
from climate_indices import read_indices, causal_values
from lucasteste1.nmme_features import add_features

class TemporalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        times = pd.date_range('2010-01-01', '2022-12-01', freq='MS')
        coords = dict(time=times, lat=[-1., 0., 1.], lon=[-50., -49.])
        self.values = np.broadcast_to(np.arange(len(times), dtype='float32')[:, None, None], (len(times), 3, 2)).copy()
        for name in ATMOS:
            xr.Dataset({name: (('time', 'lat', 'lon'), self.values)}, coords=coords).to_netcdf(self.root / f'treino_{name}.nc')
        target = self.values / 100 + 2
        target[-1] = np.nan
        xr.Dataset({'tp_alvo': (('time', 'lat', 'lon'), target)}, coords=coords).to_netcdf(self.root / 'treino_tp_alvo.nc')
        dates = pd.date_range('2023-01-01', '2024-12-01', freq='MS')
        fields = {n: (('time', 'lat', 'lon'), np.broadcast_to(np.arange(155, 179, dtype='float32')[:, None, None], (24, 3, 2))) for n in ATMOS}
        xr.Dataset(fields, coords=dict(time=dates, lat=coords['lat'], lon=coords['lon'],
                    time_origem=('time', dates - pd.offsets.MonthBegin(1)))).to_netcdf(self.root / 'teste_features.nc')
        self.data = Data(self.root)

    def tearDown(self):
        self.data.close()
        self.tmp.cleanup()

    def test_climate_uses_only_training_targets(self):
        train = self.data.indices('2010-01-01', '2015-01-01')
        climate = self.data.climatology(train, 1)
        for month in range(1, 13):
            chosen = train[self.data.targets[train].month == month]
            np.testing.assert_allclose(climate[month-1], (self.values[chosen]/100+2).mean(axis=0))
        self.assertLess(self.data.targets[train[-1]], pd.Timestamp('2015-01-01'))
        self.assertNotIn(len(self.data.times)-1, self.data.indices('2010-01-01', '2024-01-01'))

    def test_lags_cross_train_test_boundary(self):
        climate = np.ones((12, 3, 2), dtype='float32')
        jan = self.data.frame(pd.Timestamp('2023-01-01'), climate, 1, 3)
        feb = self.data.frame(pd.Timestamp('2023-02-01'), climate, 1, 3)
        self.assertEqual(jan.t2_lag1.iloc[0], 155)
        self.assertEqual(jan.t2_lag3.iloc[0], 153)
        self.assertEqual(feb.t2_lag1.iloc[0], 156)
        self.assertEqual(feb.t2_lag2.iloc[0], 155)
        self.assertNotIn('tp_alvo', jan.columns)

    def test_ocean_indices_have_only_prior_months(self):
        indices = read_indices('data/indices')
        values = causal_values(indices, pd.Timestamp('2024-01-01'))
        self.assertEqual(len(values), 12)
        self.assertAlmostEqual(values['nino3_lag1'], indices['nino3'][pd.Timestamp('2023-12-01')])
        self.data.indices_series = indices
        jan = self.data.frame(pd.Timestamp('2023-01-01'), np.ones((12, 3, 2), dtype='float32'), 1, 3)
        self.assertAlmostEqual(jan['nino3_lag1'].iloc[0], indices['nino3'][pd.Timestamp('2022-12-01')])

    def test_nmme_uses_exact_target_month_and_grid(self):
        dates = pd.date_range('2023-01-01', periods=2, freq='MS')
        lat = np.array([-60., -58.])
        lon = np.array([-90., -88.])
        cache = {'dates': dates.values, 'lat': lat, 'lon': lon,
                 'pr': np.array([[[1., 2.], [3., 4.]], [[5., 6.], [7., 8.]]], dtype='float32'),
                 'tos': np.ones((2, 2, 2), dtype='float32')*24,
                 'lookup': {pd.Timestamp(date): i for i, date in enumerate(dates)}}
        # Região de SST equatorial não pertence à grade sintética; apenas a
        # validação do mês exato é testada aqui.
        cache['lat'] = np.array([-10., 0.])
        cache['lon'] = np.array([-90., -80.])
        frame = pd.DataFrame({'x': np.arange(8)})
        result = add_features(frame, dates, cache['lat'], cache['lon'], cache)
        np.testing.assert_array_equal(result.geoss2s_pr_lead1.values, [1,2,3,4,5,6,7,8])
        with self.assertRaises(ValueError):
            add_features(pd.DataFrame({'x': np.arange(4)}), [pd.Timestamp('2022-12-01')], cache['lat'], cache['lon'], cache)

    def test_train_predict_and_second_year(self):
        indices = self.data.indices('2010-01-01', '2021-01-01')
        climate = self.data.climatology(indices, 1)
        args = SimpleNamespace(stride=1, history=3, lr=.05, leaves=7, threads=1, rounds=5)
        model = fit(self.data, indices, climate, args)
        X = self.data.frame(pd.Timestamp('2022-12-01'), climate, 1, 3)
        pred = np.maximum(0, X.climatology.to_numpy()+model.predict(X))
        self.assertTrue(np.isfinite(pred).all())
        self.assertEqual(len(self.data.indices('2021-01-01', '2023-01-01')), 24)
        self.assertAlmostEqual(rmse([1, 3], [1, 1]), np.sqrt(2))

    def test_audit_rejects_invalid_values_and_duplicate_ids(self):
        file = self.root / 'candidate.csv'
        pd.DataFrame({'id': ['2023_01_-1.00_-50.00'], 'tp_mm_day': [-1]}).to_csv(file, index=False)
        with self.assertRaises(ValueError): audit(file, official=False)
        pd.DataFrame({'id': ['2023_01_-1.00_-50.00']*2, 'tp_mm_day': [1, 2]}).to_csv(file, index=False)
        with self.assertRaises(ValueError): audit(file, official=False)

class EnsembleGateTests(unittest.TestCase):
    def test_rejects_worse_second_year(self):
        from unittest.mock import patch
        from lucasteste1 import evaluate_ensemble as gate
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for fold, start, months in [('2015full','2015-01-01',24), ('2021','2021-01-01',24), ('2022','2022-01-01',12)]:
                dates = pd.date_range(start, periods=months, freq='MS').values
                truth = np.ones(months, dtype='float32')*2
                base = truth + 1
                candidate = truth + .5
                if fold == '2015full':
                    candidate[12:] = truth[12:] + 2
                prefix = f'E00_fold{fold}_s8_l224_r700_lr0.025_years30_atm_three_ocean'
                for suffix, pred in [('',base),('_nmme_geoss2s',candidate)]:
                    np.savez(root / f'{prefix}{suffix}_predictions.npz', prediction=pred,
                             truth=truth, time=dates, lat=[0], lon=[0])
            with patch.object(gate, 'RESULTS', root), patch.object(gate, 'OUT', root/'gate.json'):
                gate.main()
                result = json.loads((root/'gate.json').read_text())
            self.assertFalse(result['passed'])
            self.assertIsNone(result['selected_weight'])

if __name__ == '__main__':
    unittest.main()
