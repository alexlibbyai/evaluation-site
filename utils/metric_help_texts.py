# Repo: evaluation-site
# Path: utils/metric_help_texts.py

METRIC_HELP = {
    "Accuracy":
        "The percentage of images classified correctly. Higher values indicate overall better classification performance.",

    "Precision":
        "Of all images identified as stego, the percentage that were actually stego images. Higher precision means fewer false positives.",

    "Recall":
        "The percentage of stego images successfully detected. Higher recall means fewer false negatives.",

    "F1":
        "A balanced measure that combines precision and recall into a single score. Useful when both false positives and false negatives are important.",

    "PSNR":
        "Peak Signal-to-Noise Ratio. Measures how closely a stego image resembles its original image. Higher values indicate less visible distortion.",

    "AUC":
        "Area Under the ROC Curve. Measures how well a model distinguishes between cover and stego images. Values closer to 1.0 indicate stronger discrimination.",

    "Mean Latency":
        "The average time required to process and classify a single image. Lower values indicate faster performance.",

    "Median Latency":
        "The middle processing time observed across all images. Less affected by unusually slow or fast classification events than the mean latency.",

    "Maximum Latency":
        "The slowest processing time recorded for a single image. Useful for identifying worst-case performance.",

    "Throughput":
        "The number of images processed per second. Higher values indicate greater processing capacity.",

    "Confidence":
        "The model's estimated certainty in its prediction. Higher confidence indicates stronger belief in the classification result, but does not guarantee correctness.",  

    "Average PSNR":
        "Indicates the average amount of visual distortion introduced by embedding. Higher values suggest hidden content is less likely to be noticeable.",

    "Average SSIM":
        "Measures how closely stego images retain the visual structure of their original cover images. Higher values indicate better preservation.",

    "Overall Visual Fidelity":
        "Represents the overall visual quality of stego images compared with their originals. Higher values indicate less perceptible change following embedding.",
    
    "PSNR":
        "Peak Signal-to-Noise Ratio. Measures how similar a stego image is to the original image. Higher values indicate less visible distortion.",

    "SSIM":
        "Structural Similarity Index. Measures how closely the structure of a stego image matches the original image. Higher values indicate greater similarity.",

    "MSE":
        "Mean Squared Error. Measures the average difference between the original and stego image. Lower values indicate less distortion.",

    "Confidence":
        "The model's estimated certainty in its prediction. Higher confidence indicates a stronger belief in the classification result.",

    "Average Confidence":
        "The average confidence score produced across all classifications.",

    "Confidence Tier":
        "Groups confidence scores into categories ranging from Minimal Confidence to Conclusive Confidence.",

    "Grad-CAM":
        "Grad-CAM highlights image regions that contribute most strongly to the model's decision.",

    "Heatmap":
        "A visual representation showing which areas of an image received the greatest attention from the model.",

    "Explainability":
        "Provides additional insight into how a model reached a classification decision.",        

    "True Positive":
        "A stego image correctly identified as stego.",

    "True Negative":
        "A cover image correctly identified as cover.",

    "False Positive":
        "A cover image incorrectly identified as stego.",

    "False Negative":
        "A stego image incorrectly identified as cover.",

    "Classification Signature":
        "A forensic-inspired visualisation showing the balance of true positives, true negatives, false positives and false negatives.",

    "Triage":
        "Prioritising images or image collections that may warrant further investigation.",

    "Suspicious Images":
        "Images classified as showing indicators associated with steganographic activity.",

    "Cover Probability":
        "The model's estimated probability that the image is a genuine cover image with no detectable steganographic content.",

    "Stego Probability":
        "The model's estimated probability that the image contains indicators consistent with steganographic embedding.",

    "Difference":
        "The gap between the Cover and Stego probabilities. Larger differences indicate greater classification confidence.",

    "Cover Percentile":
        "Shows how the Cover Probability compares to all other analysed images. Higher percentiles indicate stronger confidence that the image is a cover image.",

    "Stego Percentile":
        "Shows how the Stego Probability compares to all other analysed images. Higher percentiles indicate stronger suspicion of steganographic content.",

    "Probability Difference":
        "The difference between the Cover and Stego percentile scores. Larger values indicate greater separation between competing classifications.",

    "Stego Cover":
        "XXXXX"
}