# Repo: evaluation-site
# Path: pages/image_quality.py

import pandas as pd
import streamlit as st

from utils.workbook_loader import get_latest_workbook
from utils.metric_help_texts import METRIC_HELP
from utils.render_metric_card import render_metric_card
from utils.render_page_heading import render_page_heading
from modules.artefact_explorer import render_artefact_explorer

render_page_heading(
    "Image Quality"
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
    sheet_name="Image_Quality"
)

snn_metrics = pd.read_excel(
    snn_path,
    sheet_name="Image_Quality"
)

# --------------------------------------------------
# Display
# --------------------------------------------------

st.subheader("Key Findings")

st.markdown("""
✅ **Stego images remain visually indistinguishable** from their corresponding cover images during normal viewing.

✅ **High PSNR and SSIM values** indicate that hidden information can be embedded with minimal impact on image quality.

✅ **Artefact visualisation reveals subtle modifications** that are unlikely to be detected through visual inspection alone.
""")

st.subheader(
    "Research Question"
)

st.info(
    """
    What changes are introduced when a
    steganographic payload is embedded,
    and how visible are those changes
    during normal visual inspection?
    """
)

# --------------------------------------------------

st.subheader(
    "Artefact Explorer"
)

render_artefact_explorer()

# --------------------------------------------------

st.subheader(
    "Dataset Quality Assessment"
)

card_colour="#f39c12"
avg_psnr = cnn_metrics["Average PSNR"].mean()
avg_ssim = cnn_metrics["Average SSIM"].mean()

if avg_ssim >= 0.999:

    fidelity = "Exceptional"
    card_colour = "#2ecc71"
    badge_colour = "#f39c12"

elif avg_ssim >= 0.995:

    fidelity = "Excellent"
    card_colour = "#3498db"
    badge_colour = "#3498db"

elif avg_ssim >= 0.99:

    fidelity = "Very Good"
    card_colour = "#f39c12"
    badge_colour = "#f39c12"

else:

    fidelity = "Moderate"
    card_colour = "#e74c3c"
    badge_colour = "#e74c3c"


col1, col2, col3 = st.columns(3)


with col1:

    render_metric_card(
        "Average PSNR",
        f"{avg_psnr:.2f} dB",
        colour="#2ecc71",
        border_colour="#3498db",
        badge=False,
        help_text=METRIC_HELP["Average PSNR"]
    )

with col2:

    render_metric_card(
        "Average SSIM",
        f"{avg_ssim:.4f}",
        colour="#2ecc71",
        border_colour="#2ecc71",
        badge=False,
        help_text=METRIC_HELP["Average SSIM"]
    )

with col3:

    render_metric_card(
        "Overall Visual Fidelity",
        fidelity,
        colour="#2ecc71",
        badge_colour="#2ecc71",
        border_colour="#f39c12",
        badge=True,
        help_text=METRIC_HELP["Overall Visual Fidelity"]
    )


# --------------------------------------------------

st.subheader(
    "Supporting Evidence"
)

with st.expander("View Detailed Quality Metrics"):
    tab1, tab2 = st.tabs(
        ["ImageCNN", "ImageSNN"]
    )

    with tab1:

        st.dataframe(
            cnn_metrics,
            width='stretch',
            hide_index=True
        )

    with tab2:

        st.dataframe(
            snn_metrics,
            width='stretch',
            hide_index=True
        )
        

# --------------------------------------------------