# Repo: evaluation-site
# Path: utils/csv_loader.py

import pandas as pd

from pathlib import Path


TRAINING_FOLDER = Path("training")

def load_training_history(model_name):

    files = sorted(
        TRAINING_FOLDER.glob(
            f"{model_name}_training_history_*.csv"
        ),
        reverse=True
    )

    if not files:
        return None

    return pd.read_csv(files[0])