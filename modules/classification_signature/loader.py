# Repo: evaluation-site
# Path: modules/classification_signature/loader.py

import pandas as pd


def load_classification_metrics(
    workbook_path
):
    metrics_df = pd.read_excel(
        workbook_path,
        sheet_name="Metrics"
    )

    lookup = dict(
        zip(
            metrics_df["Metric"],
            metrics_df["Value"]
        )
    )

    return {
        "tp": int(
            lookup["True Positive"]
        ),
        "tn": int(
            lookup["True Negative"]
        ),
        "fp": int(
            lookup["False Positive"]
        ),
        "fn": int(
            lookup["False Negative"]
        ),

        "tpr": float(
            lookup["True Positive Rate (%)"]
        ),

        "tnr": float(
            lookup["True Negative Rate (%)"]
        ),

        "fpr": float(
            lookup["False Positive Rate (%)"]
        ),

        "fnr": float(
            lookup["False Negative Rate (%)"]
        )
    }