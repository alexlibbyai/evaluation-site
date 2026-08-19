# Repo: evaluation-site
# Path: main.py

# main.py

import streamlit as st


st.set_page_config(
    page_title="Steganography Evaluation Dashboard",
    page_icon="📊",
    layout="wide"
)

pg = st.navigation(
    [
        st.Page(
            "pages/overview.py",
            title="Overview"
        ),

        st.Page(
            "pages/model_performance.py",
            title="Model Performance"
        ),

        st.Page(
            "pages/image_quality.py",
            title="Image Quality"
        ),

        st.Page(
            "pages/pair_analysis.py",
            title="Pair Analysis"
        ),

        st.Page(
            "pages/run_history.py",
            title="Run History"
        ),

        st.Page(
            "pages/error_analysis.py",
            title="Error Analysis"
        ),

        st.Page(
            "pages/training_analysis.py",
            title="Training Analysis"
        ),

        st.Page(
            "pages/payload_sensitivity.py",
            title="Payload Sensitivity"
        ),              

        st.Page(
            "pages/classification_outcomes.py",
            title="Classification Outcomes"
        )                
    ]
)

pg.run()