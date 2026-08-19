# Repo: evaluation-site
# Path: pages/training/build_ribbon.py

def build_ribbon(training_df):

    losses = training_df[
        "Validation Loss"
    ]

    min_loss = losses.min()
    max_loss = losses.max()

    colours = []

    for loss in losses:

        normalised = (
            (loss - min_loss)
            /
            (max_loss - min_loss)
        )

        if normalised > 0.66:
            colours.append("#dc2626")  # red

        elif normalised > 0.33:
            colours.append("#f59e0b")  # amber

        else:
            colours.append("#16a34a")  # green

    return colours

