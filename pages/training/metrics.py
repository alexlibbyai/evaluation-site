# Repo: evaluation-site
# Path: pages/training/metrics.py

def calculate_health_score(
    validation_accuracy,
    training_loss,
    validation_loss,
    utilisation
):
    """
    Returns:
        score (0-100)
    """

    validation_score = (
        validation_accuracy * 40
    )

    loss_gap = abs(
        validation_loss -
        training_loss
    )

    stability_score = max(
        0,
        30 - (loss_gap * 100)
    )

    utilisation_score = (
        utilisation * 0.30
    )

    score = (
        validation_score +
        stability_score +
        utilisation_score
    )

    return round(
        min(score, 100),
        1
    )


def generate_training_observations(
    validation_accuracy,
    training_loss,
    validation_loss,
    best_epoch,
    utilisation
):
    observations = []

    #
    # Validation Accuracy
    #

    if validation_accuracy >= 0.80:

        observations.append(
            (
                "🟢",
                "#22c55e",
                "Strong Validation Accuracy",
                f"Validation accuracy reached {validation_accuracy:.1%}."
            )
        )

    elif validation_accuracy >= 0.70:

        observations.append(
            (
                "🟡",
                "#f59e0b",
                "Moderate Validation Accuracy",
                f"Validation accuracy is {validation_accuracy:.1%} - further tuning may improve performance."
            )
        )

    else:

        observations.append(
            (
                "🔴",
                "#dc2626",
                "Low Validation Accuracy",
                "Model performance remains below expected levels."
            )
        )

    #
    # Loss Gap
    #

    loss_gap = abs(
        validation_loss -
        training_loss
    )

    if loss_gap > 0.10:

        observations.append(
            (
                "⚠️",
                "#f59e0b",
                "Potential Overfitting",
                f"Validation loss has diverged from training loss, by {loss_gap:.3f}."
            )
        )

    else:

        observations.append(
            (
                "🟢",
                "#22c55e",
                "Stable Training",
                "Training and validation losses remained aligned."
            )
        )

    #
    # Convergence Efficiency
    #

    if utilisation < 75:

        observations.append(
            (
                "🟢",
                "#22c55e",
                "Efficient Convergence",
                f"Peak performance was achieved after {utilisation:.1f}% of the training schedule."
            )
        )

    else:

        observations.append(
            (
                "ℹ️",
                "#3b82f6",
                "Late Convergence",
                "Most of the training schedule was required."
            )
        )

    #
    # Peak Performance
    #

    observations.append(
        (
            "🟢",
            "#22c55e",
            "Peak Performance",
            f"Best validation performance occured at epoch {best_epoch} during training."
        )
    )

    return observations