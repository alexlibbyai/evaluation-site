# Repo: evaluation-site
# Path: utils/render_insight_card.py

import streamlit as st


def render_insight_card(
    title,
    badge,
    description,
    border_colour,
    badge_colour=None
):

    if badge_colour is None:
        badge_colour = border_colour

    title_html = f"""
    <div style="
        color:#666;
        font-size:16px;
        margin-bottom:15px;
    ">
        {title}
    </div>
    """

    badge_html = f"""
    <div style="
        text-align:center;
        margin-bottom:18px;
    ">
        <span style="
            background:{badge_colour};
            color:white;
            padding:10px 18px;
            border-radius:999px;
            display:inline-block;
            font-size:16px;
            font-weight:600;
        ">
            {badge}
        </span>
    </div>
    """

    description_html = f"""
    <div style="
        color:#444;
        font-size:14px;
        line-height:1.6;
        text-align:center;
    ">
        {description}
    </div>
    """

    full_html = f"""
    <div style="
        border-top:6px solid {border_colour};
        padding:20px;
        border-radius:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        background:white;
        margin-bottom:25px;
        min-height:200px;
    ">
        {title_html}
        {badge_html}
        {description_html}
    </div>
    """

    st.markdown(
        full_html,
        unsafe_allow_html=True
    )