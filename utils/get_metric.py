# Repo: evaluation-site
# Path: utils/get_metric.py

def get_metric(df, metric_name):

    return df.loc[
        df["Metric"] == metric_name,
        "Value"
    ].iloc[0]