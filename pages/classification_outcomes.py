# Repo: evaluation-site
# Path: pages/classification_outcomes.py

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from utils.workbook_loader import get_latest_workbook
from utils.render_insight_card import render_insight_card
from modules.classification_signature import classify_detector
from modules.classification_signature import load_classification_metrics
from modules.classification_signature.behaviour import compare_detector_behaviour

from modules.fingerprint_visual import render_fingerprint
from utils.render_page_heading import render_page_heading


render_page_heading("Classification Outcomes")

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

# --------------------------------------------------
# Display metrics
# --------------------------------------------------

st.write(
    "This page explores how ImageCNN and ImageSNN classify cover and stego images by examining true positives, true negatives, false positives and false negatives. These outcomes provide insight into model behaviour, reliability and the practical implications of classification errors."
)

# Image source:
# <a href="https://www.vecteezy.com/free-vector/fingerprint">Fingerprint Vectors by Vecteezy</a>

cnn_path = get_latest_workbook(
    "ImageCNN"
)

snn_path = get_latest_workbook(
    "ImageSNN"
)

cnn = load_classification_metrics(
    cnn_path
)

snn = load_classification_metrics(
    snn_path
)

cnn_behaviour, snn_behaviour = classify_detector(
    cnn, 
    snn
)

st.subheader("Detection Behaviour")

col1, col2 = st.columns(2)

with col1:

    render_insight_card(
        title="ImageCNN",
        badge=cnn_behaviour["label"],
        description=cnn_behaviour["description"],
        border_colour="#6c757d"
    )

with col2:

    render_insight_card(
        title="ImageSNN",
        badge=snn_behaviour["label"],
        description=snn_behaviour["description"],
        border_colour="#2ecc71"
    )


cnn_behaviour, snn_behaviour = (
    compare_detector_behaviour(
        cnn,
        snn
    )
)

metric_lookup = (
    comparison_df
    .set_index("Metric")
    .to_dict("index")
)

st.subheader(
    "Classification Signature"
)

col1, col2 = st.columns(2)

with col1:
    # ImageCNN
    render_fingerprint(
        tp_cnn=metric_lookup["True Positive"]["ImageCNN"],
        tp_snn=metric_lookup["True Positive"]["ImageSNN"],
        tn_cnn=metric_lookup["True Negative"]["ImageCNN"],
        tn_snn=metric_lookup["True Negative"]["ImageSNN"],
        fp_cnn=metric_lookup["False Positive"]["ImageCNN"],
        fp_snn=metric_lookup["False Positive"]["ImageSNN"],
        fn_cnn=metric_lookup["False Negative"]["ImageCNN"],
        fn_snn=metric_lookup["False Negative"]["ImageSNN"],
        ridge_1="#2ECC71",
        ridge_2="#3498DB",
        ridge_3="#F39C12",
        ridge_4="#E74C3C",
        ridge_5="#555555"
    )

with col2:

    st.markdown("#### Classification Legend")

    legend_items = [
        ("🟩", "True Positives"),
        ("🔵", "True Negatives"),
        ("🟧", "False Negatives"),
        ("🔴", "False Positives")
    ]

    for colour, label in legend_items:

        st.markdown(
            f"{colour} **{label}**"
        )



    st.info(
        "Hover over a coloured ridge to compare "
        "classification outcomes between ImageCNN "
        "and ImageSNN."
    )


st.divider()

# --------------------------------------------------
# TP / FP / TN / FN and Rates
# --------------------------------------------------

st.subheader(
    "Threshold Confidence Comparison"
)

above_cnn = metric_lookup[
    "Above Threshold"
]["ImageCNN"]

above_snn = metric_lookup[
    "Above Threshold"
]["ImageSNN"]

below_cnn = metric_lookup[
    "Below Threshold"
]["ImageCNN"]

below_snn = metric_lookup[
    "Below Threshold"
]["ImageSNN"]

threshold_cnn = metric_lookup[
    "Threshold Proportion (%)"
]["ImageCNN"]

threshold_snn = metric_lookup[
    "Threshold Proportion (%)"
]["ImageSNN"]

cnn_remaining = 100 - threshold_cnn
snn_remaining = 100 - threshold_snn

journey_gap = threshold_snn - threshold_cnn

# Display journey bars
col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "ImageCNN Above Threshold",
        f"{threshold_cnn:.2f}%"
    )

with col2:

    st.metric(
        "ImageSNN Above Threshold",
        f"{threshold_snn:.2f}%"
    )

with col3:

    st.metric(
        "Confidence Gap",
        "20.86%"
    )


st.markdown("#### Journey to Ideal Classification")

st.write("Compare how much of the journey towards ideal classification has been completed by each model. Hover over a journey bar for detailed threshold metrics.")


journey_html = f"""
<div class="journey-container">

    
    <div class="journey-label">
        ImageCNN
    </div>

    <div class="journey-track-container">
        <div class="ideal-label">100%</div>        
    
        <div class="journey-tooltip">
            <div class="journey-tooltip-title cnn-title">Journey Status</div>
            <div class="journey-tooltip-row">
                <span>Completed</span>
                <strong>{threshold_cnn:.1f}%</strong>
            </div>
            <div class="journey-tooltip-row">
                <span>Remaining</span>
                <strong>{cnn_remaining:.1f}%</strong>
            </div>
            <hr>
            <div class="journey-tooltip-row">
                <span>Above Threshold</span>
                <strong>{above_cnn:.0f}</strong>
            </div>

            <div class="journey-tooltip-row">
                <span>Below Threshold</span>
                <strong>{below_cnn:.0f}</strong>
            </div>
        </div>
        <div class="journey-track">

            <div
                class="journey-fill cnn"
                style="
                    width:{threshold_cnn}%;
                    --target-width:{threshold_cnn}%;
                "
            >
                {threshold_cnn:.0f}%
            </div>    
        </div>
        <div class="journey-remaining">
            {cnn_remaining:.0f}% Remaining
        </div>
    </div>

    <br>

    <div class="journey-label">
        ImageSNN
    </div>

    <div class="journey-track-container">
        <div class="ideal-label">100%</div>
        
        <div class="journey-tooltip">
            <div class="journey-tooltip-title snn-title">Journey Status</div>
            <div class="journey-tooltip-row">
                <span>Completed</span>
                <strong>{threshold_snn:.1f}%</strong>
            </div>
            <div class="journey-tooltip-row">
                <span>Remaining</span>
                <strong>{snn_remaining:.1f}%</strong>
            </div>
            <hr>
            <div class="journey-tooltip-row">
                <span>Above Threshold</span>
                <strong>{above_snn:.0f}</strong>
            </div>

            <div class="journey-tooltip-row">
                <span>Below Threshold</span>
                <strong>{below_snn:.0f}</strong>
            </div>
        </div>

        <div class="journey-track">
            <div
                class="journey-fill snn"
                style="
                    width:{threshold_snn}%;
                    --target-width:{threshold_snn}%;
                "
            >
                {threshold_snn:.0f}%
            </div>    
        </div>
        <div class="journey-remaining">
            {snn_remaining:.0f}% Remaining
        </div>            
    </div>
</div>

<style>

.journey-container {{
    font-family:sans-serif;
}}

.journey-label {{
    font-weight:600;
    margin-bottom:6px;
}}

.journey-track {{
    width:100%;
    height:32px;
    border-radius:16px;
    overflow:hidden;
    position:relative;
    background:
        repeating-linear-gradient(
            45deg,
            #E8ECF2,
            #E8ECF2 8px,
            #F7F9FB 8px,
            #F7F9FB 16px
        );
}}

.journey-track-container:hover
.journey-tooltip {{

    visibility:visible;
    opacity:1;
}}

@keyframes fillJourney {{
    from {{
        width:0;
    }}

    to {{
        width:var(--target-width);
    }}

}}

.journey-fill {{
    height:100%;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:flex-end;
    color:white;
    font-weight:700;
    padding-right:12px;   
    width:0;
    animation:
        fillJourney
        1.8s cubic-bezier(
            0.22,
            1,
            0.36,
            1
        )
        forwards;  
    box-sizing:border-box;
    white-space:nowrap;
    overflow:hidden;
    min-width:60px;
    position:relative;
}}

.journey-tooltip {{
    visibility:hidden;
    opacity:0;
    position:absolute;
    top:-180px;
    right:0px;
    width:220px;
    transition:0.2s ease;
    background:white;
    border:1px solid #E6EAF1;
    border-radius:12px;
    padding:12px;
    box-shadow:
        0 4px 12px rgba(0,0,0,.10),
        0 1px 3px rgba(0,0,0,.06);
    color:#31333F;
    z-index:9999;
}}

.journey-fill:hover
.journey-tooltip {{
    visibility:visible;
    opacity:1;
}}

.journey-tooltip-title {{
    font-size:18px;
    font-weight:700;
    margin-bottom:10px;
    color:#3498DB;
}}

.journey-tooltip-row {{
    display:flex;
    justify-content:space-between;
    margin-bottom:6px;
    font-size:14px;
}}

.journey-value {{
    margin-top:6px;
    font-weight:700;
}}

.journey-insight {{
    margin-top:20px;
    padding:14px 16px;
    border-left:4px solid #E67E22;
    background:#FFF8F1;
    border-radius:8px;
    font-size:14px;
    line-height:1.6;
}}

.journey-track-container {{
    position:relative;
}}

.journey-remaining {{
    margin-top:4px;
    font-size:13px;
    color:#667085;
}}

.ideal-label {{
    text-align:right;
    font-size:12px;
    color:#667085;
    margin-top:4px;
}}

.cnn {{
    background:#3498DB;
}}

.snn {{
    background:#E67E22;
}}

.cnn-title {{
    color:#3498DB;
}}

.snn-title {{
    color:#E67E22;
}}
</style>
"""

journey_gap = threshold_snn - threshold_cnn

journey_html += f"""
<div class="journey-insight">

    <strong>Key Insight</strong><br>

    ImageSNN closes an additional
    {journey_gap:.2f}% of the journey
    towards ideal classification
    compared with ImageCNN.

</div>
"""

st.html(journey_html)

# --------------------------------------------------
# Raw Data
# --------------------------------------------------

st.subheader(
    "Supporting Evidence"
)

with st.expander(
    "Show Comparison Metrics"
):
    overview_metrics = [
        "True Positive",
        "True Negative",
        "False Positive",
        "False Negative",
        "Above Threshold",
        "Below Threshold",
        "Threshold Proportion (%)"
    ]

    comparison_df = comparison_df[
        comparison_df["Metric"].isin(
            overview_metrics
        )
    ]

    st.dataframe(
        comparison_df.reset_index(drop=True),
            width='stretch',
            hide_index=True
    )