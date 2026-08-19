# Repo: evaluation-site
# Path: modules/artefact_explorer/explorer.py

import streamlit as st

from modules.artefact_explorer.loader import (
    get_first_image_for_payload,
    load_image_pair
)

from modules.artefact_explorer.processor import (
    create_difference_image,
    create_artefact_overlay
)

def render_artefact_explorer():

    payload = "stego_plain_large"

    image_name = get_first_image_for_payload(
        payload
    )

    st.caption(
        f"Using sample image: {image_name}"
    )

    cover, stego = (
        load_image_pair(
            payload,
            image_name
        )
    )

    display_mode = st.radio(
        "Display Mode",
        [
            "Original",
            "Difference",
            "Artefact Overlay"
        ]
    )

    amplification = st.slider(
        "Artefact Amplification",
        1,
        100,
        25
    )

    if display_mode == "Original":

        explorer_image = stego

    elif display_mode == "Difference":

        explorer_image = (
            create_difference_image(
                cover,
                stego
            )
        )

    elif display_mode == "Artefact Overlay":

        overlay_strength = (
            amplification / 100
        )

        explorer_image = (
            create_artefact_overlay(
                cover,
                stego,
                alpha=overlay_strength
            )
        )

    else:

        explorer_image = stego

    col1, col2, col3 = st.columns(3)

    with col1:

        st.image(
            cover,
            caption="Cover"
        )

    with col2:

        st.image(
            stego,
            caption="Stego"
        )

    with col3:

        st.image(
            explorer_image,
            caption=display_mode
        )


