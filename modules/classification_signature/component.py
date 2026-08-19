# Repo: evaluation-site
# Path: modules/classification_signature/component.py

import streamlit as st
import plotly.graph_objects as go


def build_signature(
    model_name,
    comparison_model_name,
    primary,
    comparison
):

    values = {
        "TP": primary["tp"],
        "FP": primary["fp"],
        "FN": primary["fn"],
        "TN": primary["tn"]
    }

    comparison_values = {
        "TP": comparison["tp"],
        "FP": comparison["fp"],
        "FN": comparison["fn"],
        "TN": comparison["tn"]
    }

    largest = max(
        values.values()
    )

    positions = {
        "TP": (0.5, 0.85),
        "FP": (0.15, 0.5),
        "FN": (0.85, 0.5),
        "TN": (0.5, 0.15)
    }

    fig = go.Figure()

    #
    # Fingerprint ridge structure
    #

    ridge_paths = [
        (
            [0.15, 0.30, 0.50, 0.70, 0.85],
            [0.50, 0.75, 0.85, 0.75, 0.50]
        ),
        (
            [0.15, 0.30, 0.50, 0.70, 0.85],
            [0.50, 0.65, 0.70, 0.65, 0.50]
        ),
        (
            [0.15, 0.30, 0.50, 0.70, 0.85],
            [0.50, 0.35, 0.30, 0.35, 0.50]
        ),
        (
            [0.15, 0.30, 0.50, 0.70, 0.85],
            [0.50, 0.25, 0.15, 0.25, 0.50]
        )
    ]

    for xs, ys in ridge_paths:

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,

                mode="lines",

                line=dict(
                    color="rgba(120,120,120,0.25)",
                    width=2
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )

    #
    # Letter Nodes
    #

    for metric, value in values.items():

        x, y = positions[metric]

        intensity = (
            value / largest
        )

        size = (
            28 +
            (value / largest) * 70
        )

        opacity = (
            0.35 +
            intensity * 0.65
        )

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],

                mode="text",

                text=[metric],

                textfont=dict(
                    size=size,
                    color=f"rgba(30,60,200,{opacity})"
                ),

                hovertemplate=(
                    f"<b>{metric}</b><br>"
                    f"{model_name}: {value}<br>"
                    f"{comparison_model_name}: "
                    f"{comparison_values[metric]}<br>"
                    f"Difference: "
                    f"{value - comparison_values[metric]}"
                    "<extra></extra>"
                ),

                showlegend=False
            )
        )

    fig.add_annotation(
        x=0.5,
        y=1.0,

        text=f"<b>{model_name}</b>",

        showarrow=False,

        font=dict(
            size=20
        )
    )

    fig.update_layout(
        height=700,

        paper_bgcolor="white",

        plot_bgcolor="white",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis=dict(
            visible=False,
            range=[0, 1]
        ),

        yaxis=dict(
            visible=False,
            range=[0, 1.05]
        )
    )

    return fig

def render_signature(
    model_name,
    comparison_model_name,
    primary,
    comparison
):

    fig = build_signature(
        model_name,
        comparison_model_name,
        primary,
        comparison
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )