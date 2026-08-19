# Repo: evaluation-site
# Path: utils/render_page_heading.py

import streamlit as st


def render_page_heading(
    title,
    line_width="250px",
    line_colour="#1f77b4"
):
    st.markdown(
        f"""
        <h1 style="margin-bottom:0;">
            {title}
        </h1>

        <hr style="
            height:1px;
            border:none;
            background-color:#1f77b4;
            margin-top:-10px;
            margin-bottom:30px;
            ">
        """,
        unsafe_allow_html=True
    )