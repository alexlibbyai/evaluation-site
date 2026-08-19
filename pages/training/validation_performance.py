# Repo: evaluation-site
# Path: pages/training/validation_performance.py

import pandas as pd
import streamlit as st
import plotly.express as px


def validation_performance(
    cnn_training_df, 
    snn_training_df,
    cnn_best_epoch,
    cnn_best_val_acc,
    snn_best_epoch,
    snn_best_val_acc    
):
    st.header(
        "Validation Performance"
    )

    st.write(
        "Validation accuracy measures how effectively "
        "each model generalises to unseen data during "
        "training."
    )

    selected_model = st.selectbox(
        "Highlight Model",
        [
            "Both",
            "ImageCNN",
            "ImageSNN"
        ],
        key="validation_model"
    )

    cnn_val_df = cnn_training_df.copy()
    cnn_val_df["Model"] = "ImageCNN"

    snn_val_df = snn_training_df.copy()
    snn_val_df["Model"] = "ImageSNN"

    validation_df = pd.concat(
        [
            cnn_val_df,
            snn_val_df
        ],
        ignore_index=True
    )

    fig = px.line(
        validation_df,
        x="Epoch",
        y="Validation Accuracy",
        color="Model",
        color_discrete_map={
            "ImageCNN": "#1f77b4",
            "ImageSNN": "#d62728"
        },
        markers=True,
        title="Validation Accuracy by Epoch"
    )

    for trace in fig.data:

        if selected_model == "Both":

            trace.update(
                opacity=1.0,
                line=dict(width=3)
            )

        elif selected_model in trace.name:

            trace.update(
                opacity=1.0,
                line=dict(width=4)
            )

        else:

            trace.update(
                opacity=0.2,
                line=dict(width=2)
            )

    fig.add_scatter(
        x=[cnn_best_epoch],
        y=[cnn_best_val_acc],
        mode="markers",
        marker=dict(
            size=12,
            symbol="diamond",
            color="gold"
        ),
        name="CNN Best Epoch"
    )

    fig.add_scatter(
        x=[snn_best_epoch],
        y=[snn_best_val_acc],
        mode="markers",
        marker=dict(
            size=12,
            symbol="diamond",
            color="black"
        ),
        name="SNN Best Epoch"
    )

    fig.update_layout(
        height=600,
        title=dict(
            text="Validation Accuracy by Epoch",
            x=0.5
        ),
        xaxis_title="Epoch",
        yaxis_title="Validation Accuracy",
        yaxis_tickformat=".0%"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    better_model = (
        "ImageCNN"
        if cnn_best_val_acc > snn_best_val_acc
        else "ImageSNN"
    )

    st.info(
        f"{better_model} achieved the highest "
        f"validation accuracy during training. "
        f"Peak performance occurred at Epoch "
        f"{cnn_best_epoch} for ImageCNN and "
        f"Epoch {snn_best_epoch} for ImageSNN."
    )