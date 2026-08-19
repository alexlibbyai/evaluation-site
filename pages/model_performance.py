# Repo: evaluation-site
# Path: pages/model_performance.py

import pandas as pd
import streamlit as st

from utils.workbook_loader import get_latest_workbook
from utils.metric_help_texts import METRIC_HELP
from utils.render_page_heading import render_page_heading


st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        border: 1px solid #dcdcdc;
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

render_page_heading("Model Performance")

st.write("This page compares the performance characteristics of ImageCNN and ImageSNN, highlighting differences in latency, throughput and overall processing behaviour.")

# --------------------------------------------------
# Load latest workbooks
# --------------------------------------------------

cnn_path = get_latest_workbook(
    "ImageCNN"
)

snn_path = get_latest_workbook(
    "ImageSNN"
)

# --------------------------------------------------
# Load Metrics sheets
# --------------------------------------------------

cnn_metrics = pd.read_excel(
    cnn_path,
    sheet_name="Performance"
)

snn_metrics = pd.read_excel(
    snn_path,
    sheet_name="Performance"
)

# --------------------------------------------------
# Create comparison dataframe
# --------------------------------------------------

cnn_metrics = cnn_metrics.rename(
    columns={
        "Value": "ImageCNN"
    }
)

snn_metrics = snn_metrics.rename(
    columns={
        "Value": "ImageSNN"
    }
)

comparison_df = cnn_metrics.merge(
    snn_metrics,
    on=[
        "Category",
        "Metric"
    ]
)

mean_latency_row = comparison_df[
    comparison_df["Metric"] == "Mean Latency (ms)"
].iloc[0]

cnn_mean_latency = mean_latency_row["ImageCNN"]
snn_mean_latency = mean_latency_row["ImageSNN"]

throughput_row = comparison_df[
    comparison_df["Metric"] == "Images per Second"
].iloc[0]

cnn_throughput = throughput_row["ImageCNN"]
snn_throughput = throughput_row["ImageSNN"]

latency_delta = (
    (snn_mean_latency - cnn_mean_latency)
    / cnn_mean_latency
) * 100

throughput_delta = (
    (snn_throughput - cnn_throughput)
    / cnn_throughput
) * 100



# --------------------------------------------------
# Prepare remaining metrics
# --------------------------------------------------

median_latency_row = comparison_df[
    comparison_df["Metric"]
    == "Median Latency (ms)"
].iloc[0]

cnn_median_latency = median_latency_row[
    "ImageCNN"
]

snn_median_latency = median_latency_row[
    "ImageSNN"
]

max_latency_row = comparison_df[
    comparison_df["Metric"]
    == "Maximum Latency (ms)"
].iloc[0]

cnn_max_latency = max_latency_row[
    "ImageCNN"
]

snn_max_latency = max_latency_row[
    "ImageSNN"
]

# --------------------------------------------------
# Interpretation
# --------------------------------------------------

performance_results = {
    "Mean Latency": {
        "winner": (
            "ImageCNN"
            if cnn_mean_latency < snn_mean_latency
            else "ImageSNN"
        ),
        "advantage": abs(
            (snn_mean_latency - cnn_mean_latency)
            / cnn_mean_latency
        ) * 100
    },

    "Median Latency": {
        "winner": (
            "ImageCNN"
            if cnn_median_latency < snn_median_latency
            else "ImageSNN"
        ),
        "advantage": abs(
            (snn_median_latency - cnn_median_latency)
            / cnn_median_latency
        ) * 100
    },

    "Maximum Latency": {
        "winner": (
            "ImageCNN"
            if cnn_max_latency < snn_max_latency
            else "ImageSNN"
        ),
        "advantage": abs(
            (snn_max_latency - cnn_max_latency)
            / cnn_max_latency
        ) * 100
    },

    "Throughput": {
        "winner": (
            "ImageCNN"
            if cnn_throughput > snn_throughput
            else "ImageSNN"
        ),
        "advantage": abs(
            (cnn_throughput - snn_throughput)
            / cnn_throughput
        ) * 100
    }
}


cnn_wins = sum(
    1
    for metric in performance_results.values()
    if metric["winner"] == "ImageCNN"
)

snn_wins = sum(
    1
    for metric in performance_results.values()
    if metric["winner"] == "ImageSNN"
)

best_metric = max(
    performance_results.items(),
    key=lambda x: x[1]["advantage"]
)

# --------------------------------------------------
# Key findings
# --------------------------------------------------

st.subheader("Key Findings")

if cnn_mean_latency < snn_mean_latency:

    improvement = (
        (snn_mean_latency - cnn_mean_latency)
        / snn_mean_latency
    ) * 100

    st.markdown(
        f"• ImageCNN achieved "
        f"**{improvement:.1f}%** lower mean latency."
    )

if cnn_throughput > snn_throughput:

    improvement = (
        (cnn_throughput - snn_throughput)
        / snn_throughput
    ) * 100

    st.markdown(
        f"• ImageCNN processed "
        f"**{improvement:.1f}%** more images per second."
    )

st.subheader(
    "Performance Verdict"
)

overall_winner = (
    "ImageCNN"
    if cnn_wins > snn_wins
    else "ImageSNN"
)

st.success(
    f"""
    {overall_winner} outperformed the
    competing model in
    {max(cnn_wins, snn_wins)}
    of
    {len(performance_results)}
    measured performance metrics.

    Greatest advantage:
    {best_metric[0]}
    ({best_metric[1]['advantage']:.1f}%).
    """
)

# --------------------------------------------------
# Latency
# --------------------------------------------------

st.subheader(
    "Latency Comparison - ImageSNN Relative to ImageCNN"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        label="Mean Latency",
        value=f"{snn_mean_latency:.2f} ms",
        delta=f"{latency_delta:.1f}%",
        delta_color="inverse",
        help=METRIC_HELP["Mean Latency"]
    )

with col2:

    st.metric(
        label="Throughput",
        value=f"{snn_throughput:.2f} img/s",
        delta=f"{throughput_delta:.1f}%",
        help=METRIC_HELP["Throughput"]
    )


col3, col4 = st.columns(2)

with col3:

    st.metric(
        label="Median Latency",
        value=f"{snn_median_latency:.2f} ms",
        delta=f"{((snn_median_latency - cnn_median_latency) / cnn_median_latency) * 100:.1f}%",
        delta_color="inverse",
        help=METRIC_HELP["Median Latency"]
    )

with col4:

    st.metric(
        label="Maximum Latency",
        value=f"{snn_max_latency:.2f} ms",
        delta=f"{((snn_max_latency - cnn_max_latency) / cnn_max_latency) * 100:.1f}%",
        delta_color="inverse",
        help=METRIC_HELP["Maximum Latency"]
    )



# --------------------------------------------------
# Raw Data
# --------------------------------------------------

st.subheader(
    "Supporting Evidence"
)

with st.expander(
    "Show Comparison Metrics"
):
    st.dataframe(
        comparison_df,
        width='stretch'
    )

