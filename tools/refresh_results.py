# Repo: evaluation-site
# Path: tools/refresh_results.py

from pathlib import Path
import shutil
import re


CNN_RESULTS = Path(r"C:\ImageCNN\results")
SNN_RESULTS = Path(r"C:\ImageSNN\results")

SITE_RESULTS = Path(
    r"C:\evaluation-site\results"
)


def clear_results_folder():

    SITE_RESULTS.mkdir(
        parents=True,
        exist_ok=True
    )

    for item in SITE_RESULTS.iterdir():

        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)


def newest_file(files):

    return max(
        files,
        key=lambda f: f.stat().st_mtime
    )


def copy_latest_matching(
    source_folder,
    pattern
):

    matches = list(
        source_folder.glob(pattern)
    )

    if not matches:
        return

    latest = newest_file(
        matches
    )

    shutil.copy2(
        latest,
        SITE_RESULTS / latest.name
    )

    print(
        f"Copied latest: {latest.name}"
    )


def copy_static_pngs(
    source_folder,
    prefix
):

    for png in source_folder.glob(
        f"{prefix}_*.png"
    ):

        shutil.copy2(
            png,
            SITE_RESULTS / png.name
        )

        print(
            f"Copied: {png.name}"
        )


def copy_latest_heatmap_folder():

    heatmaps_root = (
        CNN_RESULTS / "heatmaps"
    )

    if not heatmaps_root.exists():
        return

    folders = [
        f
        for f in heatmaps_root.iterdir()
        if f.is_dir()
    ]

    if not folders:
        return

    latest_folder = max(
        folders,
        key=lambda f: f.stat().st_mtime
    )

    destination = (
        SITE_RESULTS / "heatmaps"
    )

    shutil.copytree(
        latest_folder,
        destination
    )

    print(
        f"Copied heatmaps: "
        f"{latest_folder.name}"
    )


def copy_latest_spike_files():

    spike_root = (
        SNN_RESULTS / "spike_analysis"
    )

    if not spike_root.exists():
        return

    destination = (
        SITE_RESULTS / "spike_analysis"
    )

    destination.mkdir(
        exist_ok=True
    )

    groups = {
        "cover_spikes_SNN":
            [],
        "stego_spikes_SNN":
            [],
        "spike_difference_SNN":
            []
    }

    for file in spike_root.iterdir():

        if not file.is_file():
            continue

        name = file.stem

        for group in groups:

            if name.startswith(
                group
            ):
                groups[group].append(
                    file
                )

    for group, files in (
        groups.items()
    ):

        if not files:
            continue

        latest = newest_file(
            files
        )

        shutil.copy2(
            latest,
            destination / latest.name
        )

        print(
            f"Copied spike file: "
            f"{latest.name}"
        )


def main():

    clear_results_folder()

    # CNN
    copy_latest_matching(
        CNN_RESULTS,
        "ImageCNN_*.pdf"
    )

    copy_latest_matching(
        CNN_RESULTS,
        "ImageCNN_*.xlsx"
    )

    copy_latest_matching(
        CNN_RESULTS,
        "CNN_hash_manifest_*.json"
    )

    # SNN
    copy_latest_matching(
        SNN_RESULTS,
        "ImageSNN_*.pdf"
    )

    copy_latest_matching(
        SNN_RESULTS,
        "ImageSNN_*.xlsx"
    )

    copy_latest_matching(
        SNN_RESULTS,
        "SNN_hash_manifest_*.json"
    )

    # Static PNG reports
    copy_static_pngs(
        CNN_RESULTS,
        "CNN"
    )

    copy_static_pngs(
        SNN_RESULTS,
        "SNN"
    )

    # Explainability assets
    copy_latest_heatmap_folder()

    copy_latest_spike_files()

    print(
        "\nResults deployment complete."
    )


if __name__ == "__main__":
    main()