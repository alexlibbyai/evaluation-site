# Repo: evaluation-site
# Path: pages/training/training_progress.py

import pandas as pd
import streamlit as st
import plotly.express as px

def training_progress(cnn_training_df, snn_training_df):
    st.subheader(
        "Training Progress"
    )

    st.write(
        "Training and validation loss are tracked "
        "throughout the training lifecycle to assess "
        "learning stability and convergence behaviour."
    )

    cnn_training_df["Model"] = "ImageCNN"

    snn_training_df["Model"] = "ImageSNN"

    combined_training_df = pd.concat(
        [
            cnn_training_df,
            snn_training_df
        ],
        ignore_index=True
    )

    selected_model = st.selectbox(
        "Highlight Model",
        ["Both", "ImageCNN", "ImageSNN"]
    )

    cnn_loss_df = pd.concat(
        [
            cnn_training_df.assign(
                Model="ImageCNN",
                Loss_Type="Training Loss",
                Loss_Value=cnn_training_df["Training Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]],

            cnn_training_df.assign(
                Model="ImageCNN",
                Loss_Type="Validation Loss",
                Loss_Value=cnn_training_df["Validation Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]]
        ]
    )

    snn_loss_df = pd.concat(
        [
            snn_training_df.assign(
                Model="ImageSNN",
                Loss_Type="Training Loss",
                Loss_Value=snn_training_df["Training Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]],

            snn_training_df.assign(
                Model="ImageSNN",
                Loss_Type="Validation Loss",
                Loss_Value=snn_training_df["Validation Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]]
        ]
    )

    loss_df = pd.concat(
        [
            cnn_loss_df,
            snn_loss_df
        ],
        ignore_index=True
    )

    loss_df = pd.concat(
        [
            cnn_training_df.assign(
                Loss_Type="Training Loss",
                Loss_Value=cnn_training_df["Training Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]],

            cnn_training_df.assign(
                Loss_Type="Validation Loss",
                Loss_Value=cnn_training_df["Validation Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]],

            snn_training_df.assign(
                Loss_Type="Training Loss",
                Loss_Value=snn_training_df["Training Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]],

            snn_training_df.assign(
                Loss_Type="Validation Loss",
                Loss_Value=snn_training_df["Validation Loss"]
            )[["Epoch", "Model", "Loss_Type", "Loss_Value"]]
        ],
        ignore_index=True
    )

    fig = px.line(
        loss_df,
        x="Epoch",
        y="Loss_Value",
        color="Model",
        line_dash="Loss_Type",
        markers=True
    )

    fig.update_layout(
        height=600,
        title=dict(
            text="Training and Validation Loss",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Epoch",
        yaxis_title="Loss",
        legend_title=""
    )

    fig.update_traces(
        hovertemplate=
        "<b>%{fullData.name}</b><br>" +
        "Epoch: %{x}<br>" +
        "Loss: %{y:.4f}<br>" +
        "<extra></extra>"
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

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.info(
        "Training loss reflects how well the model "
        "fits the training dataset, while validation "
        "loss measures generalisation to unseen data. "
        "A narrowing gap between the two indicates "
        "stable learning and effective convergence."
    )