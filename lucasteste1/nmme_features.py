"""Features GEOSS2S inicializadas em T-1 para prever T."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

DEFAULT_CACHE = Path(__file__).resolve().parents[1] / 'data' / 'external' / 'geoss2s_lead1_sa.npz'

def load_cache(path=DEFAULT_CACHE):
    with np.load(path) as source:
        cache = {name: source[name].copy() for name in ('dates', 'lat', 'lon', 'pr', 'tos')}
    dates = pd.DatetimeIndex(cache['dates'])
    if not dates.is_unique or not dates.equals(pd.date_range(dates[0], dates[-1], freq='MS')):
        raise ValueError('Calendário NMME irregular.')
    if cache['pr'].shape != (len(dates), len(cache['lat']), len(cache['lon'])):
        raise ValueError('Dimensões NMME incompatíveis.')
    if cache['tos'].shape != cache['pr'].shape:
        raise ValueError('Dimensões de TSM NMME incompatíveis.')
    cache['tos'] = np.where((cache['tos'] > -5) & (cache['tos'] < 45), cache['tos'], np.nan)
    cache['lookup'] = {pd.Timestamp(date): i for i, date in enumerate(dates)}
    return cache

def _grid(field, cache, lat, lon):
    lat, lon = np.asarray(lat), np.asarray(lon)
    if np.array_equal(lat, cache['lat']) and np.array_equal(lon, cache['lon']):
        return field.astype('float32')
    la, lo = np.meshgrid(np.clip(lat, cache['lat'][0], cache['lat'][-1]),
                         np.clip(lon, cache['lon'][0], cache['lon'][-1]), indexing='ij')
    result = RegularGridInterpolator((cache['lat'], cache['lon']), field,
                                     bounds_error=True)(np.column_stack((la.ravel(), lo.ravel())))
    return result.reshape(la.shape).astype('float32')

def add_features(frame, targets, lat, lon, cache):
    npoints = len(lat)*len(lon)
    if len(frame) != len(targets)*npoints:
        raise ValueError('Grade do frame incompatível com NMME.')
    precipitation, sst_local, sst_pacific = [], [], []
    iy = (cache['lat'] >= -10) & (cache['lat'] <= 0)
    ix = (cache['lon'] >= -90) & (cache['lon'] <= -80)
    for target in pd.DatetimeIndex(targets):
        if target not in cache['lookup']:
            raise ValueError(f'NMME sem alvo {target:%Y-%m}')
        index = cache['lookup'][target]
        rain = cache['pr'][index]
        sst = cache['tos'][index]
        precipitation.append(_grid(rain, cache, lat, lon).ravel())
        sst_local.append(np.nan_to_num(_grid(sst, cache, lat, lon), nan=-999.0).ravel())
        value = np.nanmean(sst[np.ix_(iy, ix)])
        if not np.isfinite(value):
            raise ValueError(f'TSM do Pacífico ausente para {target:%Y-%m}')
        sst_pacific.append(np.full(npoints, value, dtype='float32'))
    frame['geoss2s_pr_lead1'] = np.concatenate(precipitation)
    frame['geoss2s_tos_local_lead1'] = np.concatenate(sst_local)
    frame['geoss2s_tos_pacific_lead1'] = np.concatenate(sst_pacific)
    if not np.isfinite(frame[['geoss2s_pr_lead1','geoss2s_tos_local_lead1','geoss2s_tos_pacific_lead1']].to_numpy()).all():
        raise ValueError('Features NMME não finitas.')
    return frame
