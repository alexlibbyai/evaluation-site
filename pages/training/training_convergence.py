# Repo: evaluation-site
# Path: pages/training/training_convergence.py

import streamlit as st

from pages.training.build_ribbon import build_ribbon

def training_convergence(
    cnn_best_epoch, 
    snn_best_epoch, 
    cnn_training_df, 
    snn_training_df
):

    st.subheader(
        "Training Convergence"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### ImageCNN"
        )

        cnn_colours = build_ribbon(
            cnn_training_df
        )

        ribbon_html = ""

        for i, colour in enumerate(cnn_colours):

            border = ""

            if i + 1 == cnn_best_epoch:

                border = (
                    "border:2px solid black;"
                )

            ribbon_html += (
                f'<div style="'
                f'width:12px;'
                f'height:30px;'
                f'background:{colour};'
                f'display:inline-block;'
                f'margin-right:1px;'
                f'{border}'
                f'"></div>'
            )

        st.markdown(
            ribbon_html,
            unsafe_allow_html=True
        )

        st.caption(
            f"Best Epoch: {cnn_best_epoch}"
        )


    with col2:

        st.markdown(
            "### ImageSNN"
        )

        snn_colours = build_ribbon(
            snn_training_df
        )

        ribbon_html = ""

        for i, colour in enumerate(snn_colours):

            border = ""

            if i + 1 == snn_best_epoch:

                border = (
                    "border:2px solid black;"
                )

            ribbon_html += (
                f'<div style="'
                f'width:12px;'
                f'height:30px;'
                f'background:{colour};'
                f'display:inline-block;'
                f'margin-right:1px;'
                f'{border}'
                f'"></div>'
            )

        st.markdown(
            ribbon_html,
            unsafe_allow_html=True
        )

        st.caption(
            f"Best Epoch: {snn_best_epoch}"
        )