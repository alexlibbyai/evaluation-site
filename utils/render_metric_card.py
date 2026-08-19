# Repo: evaluation-site
# Path: utils/render_metric_card.py

import streamlit as st

def render_metric_card(
    title,
    value,
    colour,
    badge_colour=None,
    border_colour=None,
    badge=False,
    help_text=None
):

    if border_colour is None:
        border_colour = colour

    if badge_colour is None:
        badge_colour = colour      

    if badge:

        value_html = f"""
        <div style="
            text-align:center;
            margin-top:20px;
            min-height:75px;
        ">
            <span style="
                background:{badge_colour};
                color:white;
                padding:14px 24px;
                border-radius:999px;
                display:inline-block;
                text-align:center;
                font-size:24px;
                font-weight:700;
                box-shadow:0 2px 6px rgba(0,0,0,0.08);
            ">
                {value}
            </span>
        </div>
        """

    else:

        value_html = f"""
        <div style="
            text-align:center;
            margin-top:20px;
            min-height:75px;
        ">
            <span style="
                padding:14px 24px;
                border-radius:999px;
                display:inline-block;
                text-align:center;
                font-size:34px;
                font-weight:700;
            ">
                {value}
            </span>
        </div>
        """

    if help_text:

        title_html = f"""
        <div style="
            color:#666;
            font-size:16px;
            display:flex;
            align-items:center;
            gap:6px;
            vertical-align:middle;
        ">
            <span>{title}</span>
            <span
                title="{help_text}"
                style="
                    cursor:help;
                    color:#666;
                    font-size:14px;
                "
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon" aria-hidden="true" focusable="false">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3">
                </path>
                <line x1="12" y1="17" x2="12.01" y2="17">
                </line></svg>
            </span>
        </div>
        """

    else:

        title_html = f"""
        <div style="
            color:#666;
            font-size:16px;
        ">
            {title}
        </div>
        """


    st.markdown(
        f"""
        <div style="
            border-top:6px solid {border_colour};
            padding:20px;
            border-radius:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
            background:white;
            margin-bottom: 25px;
            min-height: 150px;
        ">
            {title_html}
            {value_html}
        </div>
        """,
    unsafe_allow_html=True
)
