"""Baixa somente os arquivos oficiais; não envia submissões."""
import argparse
from pathlib import Path
import kagglehub

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='data')
    parser.add_argument('--login', action='store_true', help='Solicita token no terminal e baixa no mesmo processo')
    args = parser.parse_args()
    if args.login:
        kagglehub.login()
    path = kagglehub.competition_download(
        'previsao-climatica-de-precipitacao-sobre-a-america-do-sul',
        output_dir=str(Path(args.output).resolve()),
    )
    print('Dados oficiais:', path)
