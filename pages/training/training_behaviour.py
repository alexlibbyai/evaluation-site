# Repo: evaluation-site
# Path: pages/training/training_behaviour.py

import streamlit as st    
import plotly.graph_objects as go

from pages.training.metrics import (
    calculate_health_score,
    generate_training_observations
)


def observation_card(
    icon,
    colour,
    title,
    text
):
    st.markdown(
        f"""
        <div style="
            padding:12px;
            margin-bottom:8px;
            border-left:6px solid {colour};
            box-shadow:0 1px 3px rgba(0,0,0,0.08);
            border:1px solid #d1d5db;
            background-color:#f8fafc;
            border-radius:6px;
        ">
            <b>{icon} {title}</b><br>
            <span style="color:#111827;">
                {text}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def training_behaviour(
    cnn_final_val_loss, 
    snn_final_val_loss,
    cnn_final_train_loss,
    snn_final_train_loss,
    cnn_best_epoch,
    snn_best_epoch,
    cnn_training_df,
    snn_training_df,
    cnn_best_val_acc,
    snn_best_val_acc
):
    st.header(
        "Training Behaviour"
    )

    cnn_utilisation = (
        cnn_best_epoch /
        len(cnn_training_df)
    ) * 100

    snn_utilisation = (
        snn_best_epoch /
        len(snn_training_df)
    ) * 100

    row1_col1, row1_col2 = st.columns(2)

    # ----------------------------------
    # ImageCNN
    # ----------------------------------

    cnn_health = calculate_health_score(
        cnn_best_val_acc,
        cnn_final_train_loss,
        cnn_final_val_loss,
        cnn_utilisation
    )

    snn_health = calculate_health_score(
        snn_best_val_acc,
        snn_final_train_loss,
        snn_final_val_loss,
        snn_utilisation
    )

    average_health = (
        cnn_health +
        snn_health
    ) / 2

    cnn_score = cnn_health
    snn_score = snn_health
    average_score = average_health

    with row1_col1:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=cnn_score,

                title={
                    "text": "ImageCNN Health"
                },

                delta={
                    "reference": average_score,

                    "increasing": {
                        "color": "green"
                    },

                    "decreasing": {
                        "color": "red"
                    },
                    "relative": True,
                    "valueformat": ".1%"
                },

                gauge={
                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "darkblue"
                    },

                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#dc2626"
                        },
                        {
                            "range": [40, 70],
                            "color": "#facc15"
                        },
                        {
                            "range": [70, 100],
                            "color": "#16a34a"
                        }
                    ],

                    "threshold": {
                        "line": {
                            "color": "black",
                            "width": 4
                        },
                        "thickness": 0.9,
                        "value": average_score
                    }
                }
            )
        )

        fig.update_layout(
            height=225,
            margin=dict(
                l=25,
                r=25,
                t=50,
                b=25
            )
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    # ----------------------------------
    # ImageSNN
    # ----------------------------------

    with row1_col2:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=snn_score,

                title={
                    "text": "ImageSNN Health"
                },

                delta={
                    "reference": average_score,

                    "increasing": {
                        "color": "green"
                    },

                    "decreasing": {
                        "color": "red"
                    },
                    "relative": True,
                    "valueformat": ".1%"
                },

                gauge={
                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "darkblue"
                    },

                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#dc2626"
                        },
                        {
                            "range": [40, 70],
                            "color": "#facc15"
                        },
                        {
                            "range": [70, 100],
                            "color": "#16a34a"
                        }
                    ],

                    "threshold": {
                        "line": {
                            "color": "black",
                            "width": 4
                        },
                        "thickness": 0.9,
                        "value": average_score
                    }
                }
            )
        )

        fig.update_layout(
            height=225,
            margin=dict(
                l=25,
                r=25,
                t=50,
                b=25
            )
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    st.caption(
        f"Average Health Score: "
        f"{average_score:.1f}"
    )


    st.markdown(
        "##### Health Observations"
    )

    obs_col1, obs_col2 = st.columns(2)
    cnn_observations = []

    with obs_col1:

        st.markdown(
            "### ImageCNN"
        )

        cnn_observations = (
            generate_training_observations(
                cnn_best_val_acc,
                cnn_final_train_loss,
                cnn_final_val_loss,
                cnn_best_epoch,
                cnn_utilisation
            )
        )

        for icon, colour, title, text in cnn_observations:

            observation_card(
                icon,
                colour,
                title,
                text
            )        

    with obs_col2:

        snn_observations = []

        st.markdown(
            "### ImageSNN"
        )

        snn_observations = (
            generate_training_observations(
                snn_best_val_acc,
                snn_final_train_loss,
                snn_final_val_loss,
                snn_best_epoch,
                snn_utilisation
            )
        )

        for icon, colour, title, text in snn_observations:

            observation_card(
                icon,
                colour,
                title,
                text
            )
