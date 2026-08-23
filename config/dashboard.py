# Repo: evaluation-site
# Path: config/dashboard.py

from pathlib import Path

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FOLDER = (
    PROJECT_ROOT
    / "imagedataset"
)

COVER_FOLDER = (
    DATASET_FOLDER
    / "cover"
)

STEGO_FOLDER = (
    DATASET_FOLDER
    / "stego_plain_large"
)