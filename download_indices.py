"""Baixa séries mensais NOAA/PSL e conserva um snapshot para treino reproduzível."""
import argparse
import hashlib
import json
from pathlib import Path
import requests

SOURCES = {
    'soi': 'https://psl.noaa.gov/data/correlation/soi.data',
    'nino12': 'https://psl.noaa.gov/data/correlation/nina1.anom.data',
    'nino3': 'https://psl.noaa.gov/data/correlation/nina3.anom.data',
    'nino4': 'https://psl.noaa.gov/data/correlation/nina4.anom.data',
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='data/indices')
    args = parser.parse_args()
    dest = Path(args.output)
    dest.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, url in SOURCES.items():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.content
        if len(data) < 100 or not data[:20].decode('ascii', errors='ignore').strip()[:4].isdigit():
            raise ValueError(f'Formato inesperado em {url}')
        path = dest / f'{name}.data'
        path.write_bytes(data)
        manifest[name] = {'url': url, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        print(name, len(data), 'bytes')
    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
