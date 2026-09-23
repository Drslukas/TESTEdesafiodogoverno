"""Inventário NetCDF sem carregar os 2 GB inteiros na memória."""
import argparse
from pathlib import Path
import numpy as np
import xarray as xr
from pipeline import Data, save_json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data')
    parser.add_argument('--output', default='outputs/data_inspection.json')
    args = parser.parse_args()
    data = Data(args.data)
    try:
        report = {'root': str(data.root.resolve()), 'files': []}
        for path in sorted(data.root.glob('*.nc')):
            with xr.open_dataset(path) as ds:
                variables = {}
                for name, field in ds.data_vars.items():
                    # Estatísticas amostrais explicitamente identificadas.
                    if 'time' in field.dims:
                        field = field.isel(time=sorted(set([0, field.sizes['time']//2, field.sizes['time']-1])))
                    values = field.values
                    finite = values[np.isfinite(values)]
                    variables[name] = {'dims': list(ds[name].dims), 'shape': list(ds[name].shape),
                        'units': ds[name].attrs.get('units'), 'sample_size': int(values.size),
                        'sample_missing_fraction': float(1-finite.size/values.size),
                        'sample_min': float(finite.min()) if finite.size else None,
                        'sample_max': float(finite.max()) if finite.size else None}
                report['files'].append({'name': path.name, 'bytes': path.stat().st_size, 'variables': variables})
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        save_json(args.output, report)
        print('Inventário salvo:', args.output)
    finally:
        data.close()

if __name__ == '__main__':
    main()
