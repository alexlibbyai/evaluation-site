# Repo: evaluation-site
# Path: modules/artefact_explorer/processor.py

import cv2
import numpy as np

from PIL import Image


def create_difference_image(
    cover,
    stego
):

    cover_array = np.array(
        cover,
        dtype=np.int16
    )

    stego_array = np.array(
        stego,
        dtype=np.int16
    )

    difference = np.abs(
        cover_array - stego_array
    )

    if difference.max() > 0:

        difference = (
            difference /
            difference.max()
        ) * 255

    return Image.fromarray(
        difference.astype(np.uint8)
    )


def create_amplified_difference(
    cover,
    stego,
    amplification=25
):

    cover_array = np.array(
        cover,
        dtype=np.int16
    )

    stego_array = np.array(
        stego,
        dtype=np.int16
    )

    difference = np.abs(
        cover_array - stego_array
    )

    #
    # Amplify actual pixel changes
    #

    difference = (
        difference > 0
    ).astype(np.uint8)

    difference = (
        difference * amplification * 2.55
    )

    difference = np.clip(
        difference,
        0,
        255
    )

    return Image.fromarray(
        difference.astype(np.uint8)
    )


def create_artefact_overlay(
    cover,
    stego,
    alpha=0.35
):

    cover_rgb = np.array(
        cover.convert("RGB"),
        dtype=np.float32
    )

    cover_array = np.array(
        cover,
        dtype=np.int16
    )

    stego_array = np.array(
        stego,
        dtype=np.int16
    )

    difference = np.abs(
        cover_array - stego_array
    )

    mask = difference > 0

    overlay = cover_rgb.copy()

    #
    # Red forensic highlight
    #

    overlay[mask] = (
        (1 - alpha)
        * overlay[mask]
        +
        alpha
        * np.array(
            [255, 0, 0]
        )
    )

    return Image.fromarray(
        overlay.astype(
            np.uint8
        )
    )
