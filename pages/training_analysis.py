# Repo: evaluation-site
# Path: pages/training_analysis.py

import pandas as pd
import streamlit as st

from utils.render_page_heading import render_page_heading
from utils.workbook_loader import get_latest_workbook
from utils.csv_loader import load_training_history

from pages.training.build_ribbon import build_ribbon
from pages.training.key_findings import key_findings 
from pages.training.training_convergence import training_convergence
from pages.training.training_progress import training_progress
from pages.training.validation_performance import validation_performance
from pages.training.training_behaviour import training_behaviour 


render_page_heading("Training Analysis")

st.write(
    "This page examines model learning behaviour, "
    "training convergence and validation performance "
    "across the training lifecycle."
)


ribbon_html = ""

# --------------------------------------------------
# Load latest workbooks
# --------------------------------------------------

cnn_training_df = load_training_history(
    "ImageCNN"
)

snn_training_df = load_training_history(
    "ImageSNN"
)

if (
    cnn_training_df is None
    and
    snn_training_df is None
):

    st.warning(
        "No training history files found."
    )
    st.stop()

# --------------------------------------------------
# Calculate values required for metrics
# --------------------------------------------------

snn_colours = build_ribbon(
    snn_training_df
)

cnn_best_epoch = cnn_training_df.loc[
    cnn_training_df["Validation Accuracy"].idxmax(),
    "Epoch"
]

snn_best_epoch = snn_training_df.loc[
    snn_training_df["Validation Accuracy"].idxmax(),
    "Epoch"
]

cnn_best_val_acc = (
    cnn_training_df["Validation Accuracy"]
    .max()
)

snn_best_val_acc = (
    snn_training_df["Validation Accuracy"]
    .max()
)

cnn_final_val_acc = (
    cnn_training_df["Validation Accuracy"]
    .iloc[-1]
)

snn_final_val_acc = (
    snn_training_df["Validation Accuracy"]
    .iloc[-1]
)

cnn_final_train_loss = (
    cnn_training_df["Training Loss"]
    .iloc[-1]
)

snn_final_train_loss = (
    snn_training_df["Training Loss"]
    .iloc[-1]
)

cnn_final_val_loss = (
    cnn_training_df["Validation Loss"]
    .iloc[-1]
)

snn_final_val_loss = (
    snn_training_df["Validation Loss"]
    .iloc[-1]
)

comparison_df = pd.DataFrame(
    {
        "Metric": [
            "Best Epoch",
            "Best Validation Accuracy",
            "Final Validation Accuracy",
            "Final Training Loss",
            "Final Validation Loss"
        ],
        "ImageCNN": [
            cnn_best_epoch,
            round(cnn_best_val_acc, 4),
            round(cnn_final_val_acc, 4),
            round(cnn_final_train_loss, 4),
            round(cnn_final_val_loss, 4)
        ],
        "ImageSNN": [
            snn_best_epoch,
            round(snn_best_val_acc, 4),
            round(snn_final_val_acc, 4),
            round(snn_final_train_loss, 4),
            round(snn_final_val_loss, 4)
        ]
    }
)
# --------------------------------------------------
# Display metrics: Key Training Findings
# --------------------------------------------------

key_findings(cnn_training_df, snn_training_df)


# --------------------------------------------------
# Display metrics: Training Convergence
# --------------------------------------------------

training_convergence(
    cnn_best_epoch, 
    snn_best_epoch, 
    cnn_training_df, 
    snn_training_df
)

# --------------------------------------------------
# Display metrics: Trainning Progress
# --------------------------------------------------

training_progress(cnn_training_df, snn_training_df)

# --------------------------------------------------
# Display metrics: Validation Performance
# --------------------------------------------------

validation_performance(
    cnn_training_df, 
    snn_training_df,
    cnn_best_epoch,
    cnn_best_val_acc,
    snn_best_epoch,
    snn_best_val_acc    
)

# --------------------------------------------------
# Display metrics: Training Behaviour
# --------------------------------------------------

training_behaviour(
    cnn_final_val_loss, 
    snn_final_val_loss,
    cnn_final_train_loss,
    snn_final_train_loss,
    cnn_best_epoch,
    snn_best_epoch,
    cnn_training_df,
    snn_training_df,
    cnn_best_val_acc,
    snn_best_val_acc
)

     
# --------------------------------------------------
# Raw Data
# --------------------------------------------------

st.subheader(
    "Supporting Evidence"
)

with st.expander(
    "Show Training Metrics"
):
    st.dataframe(
        comparison_df.reset_index(drop=True),
            width='stretch',
            hide_index=True
    )