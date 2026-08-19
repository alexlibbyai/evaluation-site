# Repo: evaluation-site
# Path: modules/classification_signature/behaviour.py

def classify_detector(
    cnn,
    snn
):

    # cnn_fp = cnn["False Positive"]
    # cnn_fn = cnn["False Negative"]

    # snn_fp = snn["False Positive"]
    # snn_fn = snn["False Negative"]

    cnn_behaviour = {
        "label":
            "Lower False Alarm Rate",

        "description":
            "Less likely to classify benign images as suspicious, "
            "but more likely to miss hidden content."
    }

    snn_behaviour = {
        "label":
            "Higher Detection Rate",

        "description":
            "Detects significantly more stego images whilst "
            "maintaining a relatively low false alarm rate."
    }

    return (
        cnn_behaviour,
        snn_behaviour
    )


def compare_detector_behaviour(
    cnn,
    snn
):
    cnn_fp = cnn["fp"]
    cnn_fn = cnn["fn"]

    snn_fp = snn["fp"]
    snn_fn = snn["fn"]

    # CNN

    if (
        cnn_fp < snn_fp
        and
        cnn_fn > snn_fn
    ):

        cnn_behaviour = {
            "label":
                "Lower False Alarm Rate",

            "description":
                (
                    "Less likely to classify benign images "
                    "as suspicious, but more likely to miss "
                    "steganographic content."
                )
        }

    elif (
        cnn_fp > snn_fp
        and
        cnn_fn < snn_fn
    ):

        cnn_behaviour = {
            "label":
                "Higher Detection Rate",

            "description":
                (
                    "Identifies more stego images, "
                    "but generates additional false alarms."
                )
        }

    else:

        cnn_behaviour = {
            "label":
                "Balanced Detector",

            "description":
                (
                    "Maintains a balance between "
                    "false alarms and missed detections."
                )
        }

    # SNN

    if (
        snn_fp > cnn_fp
        and
        snn_fn < cnn_fn
    ):

        snn_behaviour = {
            "label":
                "Higher Detection Rate",

            "description":
                (
                    "Detects significantly more stego images "
                    "whilst maintaining a relatively low "
                    "false alarm rate."
                )
        }

    elif (
        snn_fp < cnn_fp
        and
        snn_fn > cnn_fn
    ):

        snn_behaviour = {
            "label":
                "Lower False Alarm Rate",

            "description":
                (
                    "Less likely to classify benign images "
                    "as suspicious, but more likely to miss "
                    "hidden content."
                )
        }

    else:

        snn_behaviour = {
            "label":
                "Balanced Detector",

            "description":
                (
                    "Maintains a balance between "
                    "false alarms and missed detections."
                )
        }

    return (
        cnn_behaviour,
        snn_behaviour
    )