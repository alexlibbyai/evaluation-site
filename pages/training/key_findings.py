# Repo: evaluation-site
# Path: pages/training/key_findings.py

import streamlit as st

def key_findings(cnn_training_df, snn_training_df):

    cnn_best_epoch = cnn_training_df.loc[
        cnn_training_df["Validation Accuracy"].idxmax(),
        "Epoch"
    ]

    snn_best_epoch = snn_training_df.loc[
        snn_training_df["Validation Accuracy"].idxmax(),
        "Epoch"
    ]

    cnn_best_acc = (
        cnn_training_df["Validation Accuracy"]
        .max()
    )

    snn_best_acc = (
        snn_training_df["Validation Accuracy"]
        .max()
    )

    cnn_epochs = len(
        cnn_training_df
    )

    snn_epochs = len(
        snn_training_df
    )

    better_model = (
        "ImageCNN"
        if cnn_best_acc > snn_best_acc
        else "ImageSNN"
    )

    st.subheader(
        "Key Training Findings"
    )

    cnn_ratio = (
        cnn_best_epoch
        / cnn_epochs
    ) * 100

    snn_ratio = (
        snn_best_epoch
        / snn_epochs
    ) * 100

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            **ImageCNN**

            - Epochs: {cnn_epochs}
            - Best Epoch: {cnn_best_epoch}
            - Best Validation Accuracy:
            {cnn_best_acc:.2%}
            """
        )

    with col2:

        st.markdown(
            f"""
            **ImageSNN**

            - Epochs: {snn_epochs}
            - Best Epoch: {snn_best_epoch}
            - Best Validation Accuracy:
            {snn_best_acc:.2%}
            """
        )