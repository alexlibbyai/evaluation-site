# Repo: evaluation-site
# Path: pages/overview.py

import pandas as pd
import streamlit as st

from utils.workbook_loader import (
    get_latest_workbook
)


st.title(
    "Steganography Evaluation Dashboard"
)

st.success(
    "Dashboard online"
)

st.markdown(
    """
    Welcome to the evaluation dashboard.

    Use the navigation menu on the left to browse
    evaluation results.
    """
)

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
    sheet_name="Metrics"
)

snn_metrics = pd.read_excel(
    snn_path,
    sheet_name="Metrics"
)

# --------------------------------------------------
# Create comparison dataframe, with filtered metrics
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
    on="Metric"
)

accuracy_row = comparison_df[
    comparison_df["Metric"] == "Accuracy"
].iloc[0]

cnn_accuracy = accuracy_row["ImageCNN"]

snn_accuracy = accuracy_row["ImageSNN"]

# --------------------------------------------------
# Display date of last update
# --------------------------------------------------

from pathlib import Path
from datetime import datetime

cnn_modified = datetime.fromtimestamp(
    Path(cnn_path).stat().st_mtime
)

age = (datetime.now() - cnn_modified).days




# --------------------------------------------------
# Display KPIs
# --------------------------------------------------

col1, col2 = st.columns([1,1])

with col1:
    st.subheader(
        "Latest Workbooks"
    )

    st.write("ImageCNN model:", cnn_path)
    st.write("ImageSNN model:", snn_path)

    st.subheader(
        "Latest Run"
    )

    st.write(
        cnn_modified.strftime(
            "%d %b %Y at %H:%M"
        )
    )

    if age <= 1:

        st.success(
            "Results are current"
        )

    elif age <= 7:

        st.warning(
            f"Results are {age} days old"
        )

    else:

        st.error(
            f"Results are {age} days old - please update"
        )


with col2:

    st.markdown(
        f"""
        <div style="
            background:#1f77b4;
            padding:20px;
            border-radius:10px;
            text-align:center;
            color:white;
            margin-bottom:20px;
            max-width: 420px; 
            width: 100%;
            margin: 0 auto 20px auto;                       
        ">
            <div style="font-size:18px;">
                ImageCNN
            </div>
            <div style="
                font-size:42px;
                font-weight:bold;
            ">
                {cnn_accuracy:.1%}
            </div>
            <div style="font-size:16px;">
                Accuracy
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            background:#d62728;
            padding:20px;
            border-radius:10px;
            text-align:center;
            color:white;
            max-width: 420px;
            width: 100%;
            margin: 0 auto;
        ">
            <div style="font-size:18px;">
                ImageSNN
            </div>
            <div style="
                font-size:42px;
                font-weight:bold;
            ">
                {snn_accuracy:.1%}
            </div>
            <div style="font-size:16px;">
                Accuracy
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Small KPI row
    # --------------------------------------------------

    kpi_container = st.container()

    with kpi_container:

        # Centre the KPI area beneath the 300px cards
        spacer1, centre, spacer2 = st.columns([1, 3, 1])

        with centre:

            kpi1, kpi2 = st.columns(2, gap="small" )

            with kpi1:

                st.markdown(
                    """
                    <div style="
                        background:#0f766e;
                        padding:20px;
                        border-radius:10px;
                        text-align:center;
                        color:white;
                        margin-bottom:20px;
                        width:100%;
                        max-width: 420px;
                        margin-top:20px;
                        min-height: 120px; 
                    ">
                        <div style="font-size:18px;">
                            Images in Dataset
                        </div>
                        <div style="
                            font-size:22px;
                            font-weight:bold;
                        ">
                            10,000
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with kpi2:

                st.markdown(
                    """
                    <div style="
                        background:#7c3aed;
                        padding:20px;
                        border-radius:10px;
                        text-align:center;
                        color:white;
                        width:100%;
                        max-width: 420px;
                        margin-top:20px;
                        min-height: 120px;                        
                    ">
                        <div style="font-size:18px;">
                            Stego Images Detected
                        </div>
                        <div style="
                            font-size:22px;
                            font-weight:bold;
                        ">
                            1,264
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# --------------------------------------------------
# Raw Data
# --------------------------------------------------


st.subheader(
    "Supporting Evidence"
)

overview_metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1",
    "AUC",
    "MSE"
]

comparison_df = comparison_df[
    comparison_df["Metric"].isin(
        overview_metrics
    )
]

with st.expander(
    "Show Comparison Metrics"
):
    st.dataframe(
        comparison_df.reset_index(drop=True),
            width='stretch',
            hide_index=True
    )