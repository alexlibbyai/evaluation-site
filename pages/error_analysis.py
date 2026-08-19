# Repo: evaluation-site
# Path: pages/error_analysis.py

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.get_metric import get_metric
from utils.workbook_loader import get_latest_workbook
from utils.render_page_heading import render_page_heading


render_page_heading("Error Analysis")

st.write(
    "This page examines classification mistakes made by ImageCNN and ImageSNN. Analysing false positives, false negatives and overall error rates helps identify potential risks when applying steganalysis in forensic investigations."
)

st.subheader("Key Findings")


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

cnn_error_summary = pd.read_excel(
    cnn_path,
    sheet_name="Error_Summary"
)

snn_error_summary = pd.read_excel(
    snn_path,
    sheet_name="Error_Summary"
)

cnn_pairs_df = pd.read_excel(
    cnn_path,
    sheet_name="Pair Analysis"
)

snn_pairs_df = pd.read_excel(
    snn_path,
    sheet_name="Pair Analysis"
)

# --------------------------------------------------
# Extract Error Summary Metrics
# --------------------------------------------------

cnn_pairs = int(
    get_metric(
        cnn_error_summary,
        "Pairs Analysed"
    )
)

snn_pairs = int(
    get_metric(
        snn_error_summary,
        "Pairs Analysed"
    )
)

cnn_fp = int(
    get_metric(
        cnn_error_summary,
        "False Positives"
    )
)

snn_fp = int(
    get_metric(
        snn_error_summary,
        "False Positives"
    )
)

cnn_fn = int(
    get_metric(
        cnn_error_summary,
        "False Negatives"
    )
)

snn_fn = int(
    get_metric(
        snn_error_summary,
        "False Negatives"
    )
)

cnn_errors = int(
    get_metric(
        cnn_error_summary,
        "Total Errors"
    )
)

snn_errors = int(
    get_metric(
        snn_error_summary,
        "Total Errors"
    )
)

cnn_error_rate = float(
    get_metric(
        cnn_error_summary,
        "Error Rate (%)"
    )
)

snn_error_rate = float(
    get_metric(
        snn_error_summary,
        "Error Rate (%)"
    )
)

cnn_pairs_df["Model"] = "ImageCNN"

snn_pairs_df["Model"] = "ImageSNN"


# --------------------------------------------------
# Create comparison dataframe
# --------------------------------------------------

cnn_error_summary = cnn_error_summary.rename(
    columns={
        "Value": "ImageCNN"
    }
)

snn_error_summary = snn_error_summary.rename(
    columns={
        "Value": "ImageSNN"
    }
)

comparison_df = cnn_error_summary.merge(
    snn_error_summary,
    on="Metric"
)

pair_analysis_df = pd.concat(
    [
        cnn_pairs_df,
        snn_pairs_df
    ],
    ignore_index=True
)

# --------------------------------------------------
# Error rate comparison
# --------------------------------------------------

st.subheader("Error Rate Comparison")

cnn_error_rate = comparison_df.loc[
    comparison_df["Metric"] == "Error Rate (%)",
    "ImageCNN"
].iloc[0]

snn_error_rate = comparison_df.loc[
    comparison_df["Metric"] == "Error Rate (%)",
    "ImageSNN"
].iloc[0]

better_model = (
    "ImageCNN"
    if cnn_error_rate < snn_error_rate
    else "ImageSNN"
)

difference = abs(
    cnn_error_rate - snn_error_rate
)

st.success(
    f"🏆 {better_model} currently demonstrates "
    f"the lower overall error rate by "
    f"{difference:.1f}%."
)

st.markdown(
    "• ImageSNN achieved a lower overall error rate, reducing total classification errors by 39.5% compared with ImageCNN."
)

st.markdown(
    "• Both models generate substantially more false negatives than false positives, suggesting that missed stego images remain the principal detection challenge."
)

st.markdown(
    "• Reductions in both false positives and false negatives indicate that ImageSNN achieved more reliable classification performance than ImageCNN."
)



# --------------------------------------------------
# Error Profile Data
# --------------------------------------------------

error_profile_df = pd.DataFrame(
    {
        "Metric": [
            "False Positives",
            "False Negatives",
            "Total Errors",
            "Error Rate (%)",
            "False Positives",
            "False Negatives",
            "Total Errors",
            "Error Rate (%)",
        ],
        "Model": [
            "ImageCNN",
            "ImageCNN",
            "ImageCNN",
            "ImageCNN",
            "ImageSNN",
            "ImageSNN",
            "ImageSNN",
            "ImageSNN",
        ],
        "Value": [
            cnn_fp,
            cnn_fn,
            cnn_errors,
            cnn_error_rate,
            snn_fp,
            snn_fn,
            snn_errors,
            snn_error_rate,
        ]
    }
)

fig = px.bar(
    error_profile_df,
    x="Metric",
    y="Value",
    color="Value",
    facet_col="Model",
    text="Value",
    custom_data=["Model"],
    color_continuous_scale="RdYlGn_r",
    title="Model Error Profile"
)

fig.update_layout(
    font=dict(
        size=14,
        color="#222222"
    )
)

fig.update_traces(
    textposition="outside",
    textfont=dict(
        size=15,
        color="black"
    )
)

fig.update_layout(
    height=550,
    showlegend=False,
    coloraxis_colorbar_title="Error Count"
)

fig.update_traces(
    hovertemplate=
    "<b>%{x}</b><br>" +
    "Model: %{customdata[0]}<br>" +
    "Value: %{y}<br>" +
    "<extra></extra>"
)

fig.update_layout(
    margin=dict(
        l=60,
        r=40,
        t=80,
        b=100
    )
)

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial",
        font_color="black"
    )
)

fig.update_layout(
    title=dict(
        text="Model Error Profile",
        x=0.5,
        xanchor="center",
        font=dict(
            size=22,
            color="#1f2937"
        )
    ),
    paper_bgcolor="white",
    plot_bgcolor="white"
)

for annotation in fig.layout.annotations:

    if "=" in annotation.text:

        annotation.text = (
            f"<b>{annotation.text.split('=')[1]}</b>"
        )

        annotation.font.size = 20
        annotation.font.color = "#222222"


st.plotly_chart(
    fig,
    width='stretch'
)

st.caption(
    "Green indicates lower error counts. "
    "Red indicates higher error counts. "
    "The chart highlights where each model's "
    "classification errors originate."
)

st.info(
    f"ImageCNN recorded {cnn_errors} total errors "
    f"compared with {snn_errors} for ImageSNN. "
    f"The largest contributor to CNN error was "
    f"false negatives ({cnn_fn})."
)

# --------------------------------------------------
# "What's Driving the Errors?"
# --------------------------------------------------

st.subheader("What's Driving The Errors?")

st.write(
    "This section examines the impact and composition "
    "of classification errors for each model."
)

col1, divider, col2 = st.columns(
    [1, 0.02, 1]
)

with col1:

    st.markdown("### Error Impact")

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.metric(
            "CNN Errors",
            cnn_errors
        )

    with row1_col2:
        st.metric(
            "CNN Error Rate",
            f"{cnn_error_rate:.1f}%"
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.metric(
            "SNN Errors",
            snn_errors
        )

    with row2_col2:
        st.metric(
            "SNN Error Rate",
            f"{snn_error_rate:.1f}%"
        )

    reduction = (
        (cnn_errors - snn_errors)
        / cnn_errors
    ) * 100

    st.success(
        f"ImageSNN reduced total errors "
        f"by {reduction:.1f}%."
    )

with divider:

    st.markdown(
        """
        <div style="
            border-left: 1px solid #d1d5db;
            height: 550px;
            margin: 0 auto;
        "></div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        "### Error Composition"
    )

    selected_model = st.radio(
        "Model:",
        ["ImageCNN", "ImageSNN"],
        horizontal=True
    )

    if selected_model == "ImageCNN":

        donut_df = pd.DataFrame(
            {
                "Category": [
                    "False Positives",
                    "False Negatives"
                ],
                "Value": [
                    cnn_fp,
                    cnn_fn
                ]
            }
        )

    else:

        donut_df = pd.DataFrame(
            {
                "Category": [
                    "False Positives",
                    "False Negatives"
                ],
                "Value": [
                    snn_fp,
                    snn_fn
                ]
            }
        )


    fig = px.pie(
        donut_df,
        names="Category",
        values="Value",
        hole=0.55,
        color="Category",
        color_discrete_map={
            "False Positives": "#1f77b4",
            "False Negatives": "#d62728"
        }
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Count: %{value}<br>" +
        "Contribution: %{percent}<br>" +
        "<extra></extra>"
    )

    fig.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )


# --------------------------------------------------
# Confidence Separation Analysis
# --------------------------------------------------

st.subheader("Confidence Separation Analysis")

st.caption(
    "Larger separation values indicate stronger "
    "distinction between cover and stego images."
)

fig = px.violin(
    pair_analysis_df,
    x="Model",
    y="difference",
    color="Model",
    box=True,
    points="outliers",
    color_discrete_map={
        "ImageCNN": "#1f77b4",
        "ImageSNN": "#d62728"
    },
    title="Confidence Separation Distribution"
)

fig.update_layout(
    height=550,
    showlegend=False,
    title=dict(
        text="Confidence Separation Distribution",
        x=0.5,
        xanchor="center",
        font=dict(
            size=22,
            color="#1f2937"
        )
    ),
    yaxis_title="Cover-Stego Difference",
    xaxis_title=""
)

fig.update_traces(
    hovertemplate=
    "<b>%{x}</b><br>" +
    "Difference: %{y:.4f}<br>" +
    "<extra></extra>"
)

st.plotly_chart(
    fig,
    width='stretch'
)

cnn_mean = cnn_pairs_df["difference"].mean()
snn_mean = snn_pairs_df["difference"].mean()

better_model = (
    "ImageCNN"
    if cnn_mean > snn_mean
    else "ImageSNN"
)

st.info(
    f"{better_model} demonstrates greater average "
    f"confidence separation between cover and stego "
    f"images, suggesting stronger discrimination "
    f"between the two classes."
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
