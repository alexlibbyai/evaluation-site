# Repo: evaluation-site
# Path: pages/payload_sensitivity.py

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from utils.workbook_loader import get_latest_workbook
from utils.render_page_heading import render_page_heading

from modules.payload_thermometer import render_thermometer
from utils.metric_help_texts import METRIC_HELP


render_page_heading("Payload Sensitivity Analysis")

# --------------------------------------------------
# Load values from workbooks
# --------------------------------------------------

cnn_path = get_latest_workbook("ImageCNN")
snn_path = get_latest_workbook("ImageSNN")

cnn_training_df = pd.read_excel(
    cnn_path,
    sheet_name="Detection_Sensitivity"
)

snn_training_df = pd.read_excel(
    snn_path,
    sheet_name="Detection_Sensitivity"
)

comparison_df = cnn_training_df.merge(
    snn_training_df,
    on=["Analysis", "Category"],
    suffixes=("_CNN", "_SNN")
)

# show selected columns, based on metrics used in page
comparison_df = comparison_df[
    [
        "Analysis",
        "Category",
        "Accuracy_CNN",
        "Accuracy_SNN",
        "F1_CNN",
        "F1_SNN",
        "Recall_CNN",
        "Recall_SNN",
        "Precision_CNN",
        "Precision_SNN"
    ]
]

# convert results into percentages
for col in comparison_df.columns:
    if col not in ["Analysis", "Category"]:
        comparison_df[col] = (
            comparison_df[col] * 100
        ).round(2)

comparison_df["Accuracy Gap"] = (
        comparison_df["Accuracy_SNN"]
        - comparison_df["Accuracy_CNN"]
    ).round(2)

# split into 3 smaller tables
payload_size_df = comparison_df[
    comparison_df["Analysis"] == "Payload Size"
]

payload_type_df = comparison_df[
    comparison_df["Analysis"] == "Payload Type"
]

payload_category_df = comparison_df[
    comparison_df["Analysis"] == "Payload Category"
]

# split payload size into small, medium and large
small_row = payload_size_df[
    payload_size_df["Category"] == "small"
].iloc[0]

medium_row = payload_size_df[
    payload_size_df["Category"] == "medium"
].iloc[0]

large_row = payload_size_df[
    payload_size_df["Category"] == "large"
].iloc[0]

# --------------------------------------------------
# Key Findings
# --------------------------------------------------

st.subheader("Key Findings")

st.info(
    """
    • Larger payloads were substantially easier to detect than smaller payloads.

    • ImageSNN outperformed ImageCNN across all payload sizes.

    • The performance gap increased as payload size increased.

    • Encryption had little impact on overall detection performance.
    """
)


# --------------------------------------------------
# Payload Thermometers
# --------------------------------------------------

small_cnn = small_row["Accuracy_CNN"]
small_snn = small_row["Accuracy_SNN"]

medium_cnn = medium_row["Accuracy_CNN"]
medium_snn = medium_row["Accuracy_SNN"]

large_cnn = large_row["Accuracy_CNN"]
large_snn = large_row["Accuracy_SNN"]

small_average = (
    small_cnn + small_snn
) / 2

medium_average = (
    medium_cnn + medium_snn
) / 2

large_average = (
    large_cnn + large_snn
) / 2


col1, col2, col3 = st.columns(3)

with col1:

    render_thermometer(
        payload_name="Small Payload",
        score=small_average,
        cnn_score=small_cnn,
        snn_score=small_snn        
    )

with col2:

    render_thermometer(
        payload_name="Medium Payload",
        score=medium_average,
        cnn_score=medium_cnn,
        snn_score=medium_snn        
    )

with col3:

    render_thermometer(
        payload_name="Large Payload",
        score=large_average,
        cnn_score=large_cnn,
        snn_score=large_snn        
    )   

# --------------------------------------------------
# Comparison visual
# --------------------------------------------------

st.subheader(
    "Detection Performance Journey"
)

metric = st.selectbox(
    "Journey Metric:",
    [
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
    ]
)

metric_map = {
    "Accuracy": (
        "Accuracy_CNN",
        "Accuracy_SNN"
    ),
    "Precision": (
        "Precision_CNN",
        "Precision_SNN"
    ),
    "Recall": (
        "Recall_CNN",
        "Recall_SNN"
    ),
    "F1": (
        "F1_CNN",
        "F1_SNN"
    )
}

cnn_col, snn_col = metric_map[metric]

journey_df = pd.DataFrame(
    {
        "Payload": payload_size_df["Category"],
        "CNN": payload_size_df[cnn_col],
        "SNN": payload_size_df[snn_col]
    }
)

journey_df["Payload"] = (
  journey_df["Payload"]
  .str.title()
)

fig = go.Figure()

st.markdown(
    f"##### {metric} by Payload Size",
    help=METRIC_HELP[metric]
)

# Best metric by model
best_cnn = journey_df["CNN"].max()
best_snn = journey_df["SNN"].max()

largest_gap = (
    journey_df["SNN"]
    - journey_df["CNN"]
).max()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Best CNN",
        f"{best_cnn:.2f}%"
    )

with col2:
    st.metric(
        "Best SNN",
        f"{best_snn:.2f}%"
    )

with col3:
    st.metric(
        "Largest Gap",
        f"{largest_gap:.2f}%"
    )

fig.add_trace(
    go.Scatter(
        x=journey_df["Payload"],
        y=journey_df["CNN"],

        name="ImageCNN",

        text=[
            "",
            "",
            "ImageCNN"
        ],

        textposition="top left",

        line=dict(
            color="#3498DB",
            width=5
        ),

        marker=dict(
            size=18,
            color="#3498DB",
            line=dict(
                color="white",
                width=2
            )
        ),

        hovertemplate=
        (
            "<b>ImageCNN</b><br>"
            "Payload: %{x}<br>"
            f"{metric}: %{{y:.2f}}%"
            "<extra></extra>"
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=journey_df["Payload"],
        y=journey_df["SNN"],

        name="ImageSNN",

        text=[
            "",
            "",
            "ImageSNN"
        ],

        textposition="top left",

        line=dict(
            color="#E67E22",
            width=6
        ),

        marker=dict(
            size=20,
            color="#E67E22",
            line=dict(
                color="white",
                width=2
            )
        ),

        hovertemplate=
        (
            "<b>ImageSNN</b><br>"
            "Payload: %{x}<br>"
            f"{metric}: %{{y:.2f}}%"
            "<extra></extra>"
        )
    )
)

fig.update_layout(

    template="simple_white",

    height=500,

    margin=dict(
        l=20,
        r=140,
        t=60,
        b=20
    ),

    showlegend=True,

    hovermode="x unified"
)

fig.update_yaxes(
    title=f"{metric} (%)"
)

fig.update_xaxes(
    title=""
)

st.plotly_chart(
    fig,
    width="stretch"
)

# --------------------------------------------------
# Raw Data
# --------------------------------------------------

st.subheader(
    "Supporting Evidence"
)

with st.expander("Payload Size Metrics"):

    payload_size_df = payload_size_df.drop(
        columns=["Analysis"]
    )

    st.dataframe(
        payload_size_df,
        hide_index=True,
        width="stretch"
    )

with st.expander("Payload Type Metrics"):

    payload_type_df = payload_type_df.drop(
        columns=["Analysis"]
    )

    st.dataframe(
        payload_type_df,
        hide_index=True,
        width="stretch"
    )


with st.expander("Payload Category Metrics"):

    payload_category_df = payload_category_df.drop(
        columns=["Analysis"]
    ) 
       
    st.dataframe(
        payload_category_df,
        hide_index=True,
        width="stretch"
    )

