"""
Compara o modelo v1 (já submetido no Kaggle, sem lag_meses, treinado com tp
sempre fresco) contra o v2 (lag-aware), os dois avaliados nos MESMOS blocos
de validação realista (tp congelado + lag crescente) - pra isolar o efeito
real da correção do lag, sem misturar com "mudamos a forma de medir".

Uso:
    .venv/bin/python scripts/compare_v1_v2_realistic.py
"""

import numpy as np
import lightgbm as lgb
import pandas as pd

from features_lagged import build_realistic_validation_block, load_raw_strided
from baseline_climatology import rmse
from train_lightgbm import FEATURES as FEATURES_V1

FEATURES_V2 = FEATURES_V1 + ["lag_meses"]

BLOCK_1 = ("1997-05-01", "1998-04-01")
BLOCK_2 = ("2015-01-01", "2016-05-01")


def main():
    arrays, lat_s, lon_s, time_full = load_raw_strided()

    model_v1 = lgb.Booster(model_file="../outputs/lgb_model_final.txt")  # o que foi submetido (2.2287 no Kaggle)
    model_v2 = lgb.Booster(model_file="../outputs/lgb_model_v2.txt")

    for name, (first, last) in (("Bloco 1997-98", BLOCK_1), ("Bloco 2015-16", BLOCK_2)):
        val_df = build_realistic_validation_block(arrays, lat_s, lon_s, time_full, first, last)
        y_true = val_df["target"].values

        preds_v1 = np.clip(model_v1.predict(val_df[FEATURES_V1]), 0, None)
        score_v1 = rmse(preds_v1, y_true)

        preds_v2 = np.clip(model_v2.predict(val_df[FEATURES_V2]), 0, None)
        score_v2 = rmse(preds_v2, y_true)

        print(f"{name} (mesma validação realista pros dois):")
        print(f"  v1 (submetido, tp sempre 'fresco' no treino): RMSE={score_v1:.4f}")
        print(f"  v2 (lag-aware):                                RMSE={score_v2:.4f}")
        print(f"  melhora: {(score_v1-score_v2)/score_v1*100:.1f}%\n")


if __name__ == "__main__":
    main()
