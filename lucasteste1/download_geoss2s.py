"""Subconjunto GEOSS2S causal: emissão S=T-1, lead 1, alvo T."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

BASE = 'https://forecast.ccsr.columbia.edu/data/NMME/NASA-GMAO/GEOSS2S/'
VARIABLES = ('pr', 'tos')

def fetch(variable, period, first, last):
    url = f'{BASE}{period}/{variable}'
    with xr.open_dataset(url, engine='netcdf4') as ds:
        times = pd.DatetimeIndex(ds.S.values)
        selected = np.flatnonzero((times >= pd.Timestamp(first)) & (times <= pd.Timestamp(last)))
        if not len(selected):
            raise ValueError(f'Sem inicializações {period}/{variable} para {first}..{last}')
        if not np.array_equal(selected, np.arange(selected[0], selected[-1]+1)):
            raise ValueError('Inicializações não contíguas.')
        lat_indices = np.flatnonzero((ds.Y.values >= -60) & (ds.Y.values <= 14))[::2]
        lon_indices = np.flatnonzero((ds.X.values >= 270) & (ds.X.values <= 334))[::2]
        lat, lon = ds.Y.values[lat_indices], ds.X.values[lon_indices]-360
        if len(lat) != 38 or len(lon) != 33:
            raise ValueError('Grade GEOSS2S não é 38x33 a 2 graus.')
        target = pd.DatetimeIndex(ds.target.isel(S=selected, L=1).values)
        origin = times[selected]
        if not target.equals(origin + pd.offsets.MonthBegin(1)):
            raise ValueError('NMME: lead 1 não corresponde ao mês seguinte.')
        chunks = []
        for start in range(int(selected[0]), int(selected[-1])+1, 12):
            stop = min(start+12, int(selected[-1])+1)
            raw = ds[variable].isel(S=slice(start, stop), L=1,
                                     Y=slice(lat_indices[0], lat_indices[-1]+1, 2),
                                     X=slice(lon_indices[0], lon_indices[-1]+1, 2)).values
            if variable == 'pr' and (not np.isfinite(raw).all() or np.max(raw) <= 0):
                raise ValueError(f'NMME retornou bloco vazio/zero em {period} {times[start]}..{times[stop-1]}')
            if variable == 'tos':
                raw = np.where((raw > -5) & (raw < 45), raw, np.nan)
            chunks.append(np.nanmean(raw, axis=1).astype('float32'))
            print(variable, period, str(times[stop-1].date()), flush=True)
        field = np.concatenate(chunks)
        if field.shape != (len(target), 38, 33):
            raise ValueError(f'Dimensão inesperada: {field.shape}')
        if variable == 'pr' and not np.isfinite(field).all():
            raise ValueError('GEOSS2S pr tem valores ausentes.')
        return target, field, lat, lon, {'url': url, 'units': ds[variable].attrs.get('units'),
                                         'period': period, 'first_origin': str(origin[0].date()),
                                         'last_origin': str(origin[-1].date()),
                                         'members': int(ds.sizes['M'])}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='data/external/geoss2s_lead1_sa.npz')
    args = parser.parse_args()
    fields = {}
    meta = {}
    all_dates = None
    for variable in VARIABLES:
        groups = []
        for period, first, last in [('hindcast', '1984-01-01', '2017-01-01'),
                                    ('forecast', '2017-02-01', '2024-11-01')]:
            print('Lendo', variable, period, flush=True)
            dates, field, lat, lon, info = fetch(variable, period, first, last)
            groups.append((dates, field)); meta[f'{variable}_{period}'] = info
        dates = groups[0][0].append(groups[1][0])
        if not dates.is_unique or not dates.equals(pd.date_range(dates[0], dates[-1], freq='MS')):
            raise ValueError('Meses GEOSS2S repetidos ou ausentes.')
        if all_dates is not None and not dates.equals(all_dates):
            raise ValueError('Calendários de pr e tos diferentes.')
        all_dates = dates
        fields[variable] = np.concatenate([g[1] for g in groups])
    if not np.isfinite(fields['pr']).all() or np.nanmax(fields['pr']) <= 0:
        raise ValueError('GEOSS2S pr inválido no cache completo.')
    if not (10 < np.nanmax(fields['tos']) < 50):
        raise ValueError('Unidades/valores de GEOSS2S tos inesperados.')
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output, dates=all_dates.values, lat=lat, lon=lon, **fields)
    meta.update({'rows': len(all_dates), 'first_target': str(all_dates[0].date()),
                 'last_target': str(all_dates[-1].date()),
                 'cache_sha256': hashlib.sha256(output.read_bytes()).hexdigest()})
    output.with_suffix('.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print('Cache:', output, 'alvos:', len(all_dates), flush=True)

if __name__ == '__main__':
    main()
