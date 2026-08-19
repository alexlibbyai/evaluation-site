# Repo: evaluation-site
# Path: modules/artefact_explorer/loader.py

from PIL import Image
from pathlib import Path
import streamlit as st

DATASET_ROOT = Path(
    "imagedataset"
)

COVER_FOLDER = (
    DATASET_ROOT / "cover"
)


def get_payload_folders():

    folders = [
        f.name
        for f in DATASET_ROOT.iterdir()
        if f.is_dir()
        and f.name != "cover"
    ]

    return sorted(
        folders
    )


def get_images_for_payload(
    payload_folder
):

    folder = (
        DATASET_ROOT
        / payload_folder
    )

    return sorted(
        [
            f.name
            for f in folder.iterdir()
            if f.is_file()
        ]
    )


def get_image_paths(
    payload_folder,
    filename
):

    cover_path = (
        COVER_FOLDER
        / filename
    )

    stego_path = (
        DATASET_ROOT
        / payload_folder
        / filename
    )

    return (
        cover_path,
        stego_path
    )


def load_image_pair(
    payload_folder,
    filename
):

    image_id = (
        filename.split("_")[0]
    )

    cover_filename = (
        f"{image_id}.pgm"
    )

    cover_path = (
        COVER_FOLDER
        / cover_filename
    )

    stego_path = (
        DATASET_ROOT
        / payload_folder
        / filename
    )

    cover = Image.open(
        cover_path
    )

    stego = Image.open(
        stego_path
    )

    return (
        cover,
        stego
    )


def get_first_image_for_payload(
    payload_folder
):

    images = get_images_for_payload(
        payload_folder
    )

    if not images:
        return None

    return images[0]