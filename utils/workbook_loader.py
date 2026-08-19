# Repo: evaluation-site
# Path: utils/workbook_loader.py

from pathlib import Path

RESULTS_DIR = Path("results")

def get_latest_workbook(model_name):

    files = sorted(
        RESULTS_DIR.glob(
            f"{model_name}_*.xlsx"
        )
    )

    if not files:
        return None

    return files[-1]