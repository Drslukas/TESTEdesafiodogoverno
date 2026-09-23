"""Combina dois CSVs somente com o peso aprovado em validação temporal."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from audit_submission import audit

def main():
    root = Path('outputs')
    gate = json.loads((root / 'nmme_gate.json').read_text(encoding='utf-8'))
    if not gate['passed']:
        raise ValueError('Nenhum peso NMME passou nos folds históricos.')
    weight = float(gate['selected_weight'])
    nmme = pd.read_csv(root / 'submission_ocean_nmme_2023_2024.csv', dtype={'id': str})
    if weight == 1:
        result = nmme
    else:
        base = pd.read_csv(root / 'submission_ocean_2023_2024.csv', dtype={'id': str})
        if not base.id.equals(nmme.id):
            raise ValueError('IDs ou ordem incompatíveis entre modelos.')
        result = base.copy()
        result['tp_mm_day'] = np.maximum(0, (1-weight)*base.tp_mm_day.to_numpy() + weight*nmme.tp_mm_day.to_numpy())
    output = root / 'submission_candidate_2023_2024.csv'
    result.to_csv(output, index=False)
    reference = Path('C:/Users/Acer/Downloads/submission_ocean_2023_2024.csv')
    report = audit(output, reference if reference.exists() else None)
    (root / 'candidate_audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Candidato:', output, 'peso NMME:', weight, 'SHA-256:', report['sha256'])

if __name__ == '__main__':
    main()
