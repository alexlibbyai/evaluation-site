# Repo: evaluation-site
# Path: pages/run_history.py

import pandas as pd
import streamlit as st
import plotly.express as px

from pathlib import Path
from utils.ordinal import ordinal
from utils.render_page_heading import render_page_heading

# ==================================================
# Mock Data
# ==================================================

history_file = Path(
    "history/run_history.csv"
)

history_df = pd.read_csv(
    history_file,
    encoding="utf-8-sig"
)

# ==================================================
# Summary Metrics
# ==================================================

num_experiments = len(history_df)

latest_run = history_df[
    "timestamp"
].max()

best_accuracy = history_df[
    "accuracy"
].max()

models_tracked = history_df[
    "model"
].nunique()

history_df["timestamp"] = pd.to_datetime(
    history_df["timestamp"],
    dayfirst=True
)

latest_run = history_df[
    "timestamp"
].max()

formatted_latest_run = (
    f"{ordinal(latest_run.day)} "
    f"{latest_run.strftime('%B, %Y')}"
    )

# ==================================================
# Page Header
# ==================================================

render_page_heading(
    "Run History"
)


# ==================================================
# Summary Cards
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Experiments",
        num_experiments
    )

with col2:
    st.markdown(
    f"""
    <div>
        <div style="font-size:14px;">
            Latest Run
        </div>
        <div style="font-size:28px;">
            {formatted_latest_run}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with col3:
    st.metric(
        "Best Accuracy",
        f"{best_accuracy:.1%}"
    )

with col4:
    st.metric(
        "Models",
        models_tracked
    )

# ==================================================
# Accuracy Trend
# ==================================================

st.subheader(
    "Accuracy Trend"
)

if len(history_df) < 3:
    st.info(
        "Additional runs are required before meaningful performance trends can be displayed."
    )

fig = px.line(
    history_df,
    x="timestamp",
    y="accuracy",
    color="model",
    markers=True
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ==================================================
# Improvement Summary
# ==================================================

st.subheader(
    "Performance Evolution"
)

for model in [
    "ImageCNN",
    "ImageSNN"
]:

    model_df = history_df[
        history_df["model"] == model
    ]

    if len(model_df) == 0:
        st.info(
            f"No run history available for {model}."
        )
        continue

    elif len(model_df) == 1:
        st.write(
            f"**{model}** currently has a single recorded run. Additional experiments are required before performance trends can be evaluated."
        )
        continue

    else:
        improvement = (
            model_df.iloc[-1]["accuracy"]
            -
            model_df.iloc[0]["accuracy"]
        ) * 100   

    st.write(
        f"**{model}** improved by "
        f"{improvement:.2f}% accuracy "
        f"since the first recorded run."
    )

# ==================================================
# Recent Experiments
# ==================================================

st.subheader(
    "Recent Experiments"
)

display_df = history_df.copy()

display_df["timestamp"] = (
    display_df["timestamp"]
    .dt.strftime("%d/%m/%Y %H:%M")
)

st.dataframe(
    display_df.sort_values(
        "timestamp",
        ascending=False
    ),
    width="stretch",
    hide_index=True
)