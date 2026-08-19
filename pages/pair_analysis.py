# Repo: evaluation-site
# Path: pages/pair_analysis.py

import cv2
import pandas as pd
import streamlit as st


from utils.workbook_loader import (
    get_latest_workbook
)

from config.dashboard import COVER_FOLDER, STEGO_FOLDER
from utils.metric_help_texts import METRIC_HELP
from utils.render_page_heading import render_page_heading

# ==================================================
# Page Header
# ==================================================

render_page_heading("Pair Analysis")

st.write(
    """
    Compare ImageCNN and ImageSNN predictions
    for the same cover/stego image pair.
    """
)

# ==================================================
# Load Workbooks
# ==================================================

cnn_path = get_latest_workbook(
    "ImageCNN"
)

snn_path = get_latest_workbook(
    "ImageSNN"
)

# ==================================================
# Load Pair Analysis Sheets
# ==================================================

cnn_pairs = pd.read_excel(
    cnn_path,
    sheet_name="Pair Analysis"
)

snn_pairs = pd.read_excel(
    snn_path,
    sheet_name="Pair Analysis"
)

# ==================================================
# Rename Columns
# ==================================================

cnn_pairs = cnn_pairs.rename(
    columns={
        "difference": "cnn_difference"
    }
)

snn_pairs = snn_pairs.rename(
    columns={
        "difference": "snn_difference"
    }
)

# ==================================================
# Merge
# ==================================================

comparison_df = cnn_pairs.merge(
    snn_pairs,
    on=[
        "filename_cover",
        "filename_stego"
    ],
    how="outer"
)

# ==================================================
# Pair Selector
# ==================================================

available_pairs = (
    comparison_df["filename_cover"]
    .dropna()
    .sort_values()
    .unique()
    .tolist()
)

selected_pair = st.selectbox(
    "Select Cover Image",
    available_pairs
)

selected_row = comparison_df[
    comparison_df["filename_cover"]
    == selected_pair
].iloc[0]


# ==================================================
# Preview Images
# ==================================================

cover_path = (
    COVER_FOLDER
    / selected_row["filename_cover"]
)

stego_path = (
    STEGO_FOLDER
    / selected_row["filename_stego"]
)

st.subheader(f"Image Preview of {selected_row['filename_cover']}")

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"### Cover")

    img = cv2.imread(
        str(cover_path),
        cv2.IMREAD_GRAYSCALE
    )

    st.image(
        img,
        clamp=True
    )

with col2:

    st.markdown(f"### Stego")

    img = cv2.imread(
        str(stego_path),
        cv2.IMREAD_GRAYSCALE
    )

    st.image(
        img,
        clamp=True
    )

   
# ==================================================
# Metrics Comparison
# ==================================================

st.subheader("Supporting Evidence")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### ImageCNN")

    st.metric(
        "Cover Probability",
        f"{selected_row['probability_cover']:.4f}",
        help=METRIC_HELP["Stego Cover"]
    )

    st.metric(
        "Stego Probability",
        f"{selected_row['probability_stego']:.4f}",
        help=METRIC_HELP["Stego Probability"]
    )

    st.metric(
        "Difference",
        f"{selected_row['cnn_difference']:.4f}",
        help="Magnitude of separation between cover and stego predictions."
    )

with col2:

    st.markdown("### ImageSNN")

    if "percentile_cover" in selected_row:

        st.metric(
            "Cover Percentile",
            f"{selected_row['percentile_cover']:.4f}",
            help=METRIC_HELP["Cover Percentile"]
        )

    if "percentile_stego" in selected_row:

        st.metric(
            "Stego Percentile",
            f"{selected_row['percentile_stego']:.4f}",
            help=METRIC_HELP["Stego Percentile"]
        )

    difference = selected_row.get(
        "snn_difference",
        0
    )

    if abs(difference) > 0.0001:

        st.metric(
            "Difference",
            f"{difference:.4f}",
            help="Magnitude of separation between cover and stego percentiles."
        )

    else:

        st.metric(
            "Difference",
            "No Difference",
            help="Cover and stego percentiles are identical for this image."
        )

# ==================================================
# Winner Calculation
# ==================================================

cnn_diff = abs(
    selected_row.get(
        "cnn_difference",
        0
    )
)

snn_diff = abs(
    selected_row.get(
        "snn_difference",
        0
    )
)

st.divider()

st.subheader("Winner")

if cnn_diff > snn_diff:

    st.info(
        f"🟦 ImageCNN wins with an advantage of {cnn_diff - snn_diff:.4f}"
    )

elif snn_diff > cnn_diff:

    st.success(
        f"🟩 ImageSNN wins with an advantage of {snn_diff - cnn_diff:.4f}"
    )

else:

    st.warning(
        "🤝 Draw"
    )

# ==================================================
# Raw Comparison Data
# ==================================================

st.subheader(
    "Supporting Evidence"
)

with st.expander(
    "Show Comparison Data"
):

    st.dataframe(
        comparison_df,
        width='stretch'
    )