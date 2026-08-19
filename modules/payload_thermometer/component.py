# Repo: evaluation-site
# Path: modules/payload_thermometer/component.py

import streamlit as st

# Source for the thermometer: https://freesvg.org/temperatur


def get_detection_profile(score):

    if score >= 95:
        return "Conclusive", "#C0392B"

    elif score >= 80:
        return "Strong", "#E67E22"

    elif score >= 60:
        return "Moderate", "#F1C40F"

    elif score >= 40:
        return "Weak", "#3498DB"


def render_thermometer(
    payload_name,
    score,
    cnn_score=None,
    snn_score=None    
):
    profile, colour = (
        get_detection_profile(score)
    )

    #
    # SVG coordinates
    #
    # Tube:
    # y=5 to y=165
    #

    tube_top = 5
    tube_height = 160

    fill_height = (
        tube_height
        * (score / 100)
    )

    fill_y = (
        tube_top
        + tube_height
        - fill_height 
    )

    profile, colour = get_detection_profile(score)

    model_breakdown = ""

    if cnn_score is not None and snn_score is not None:

        best_model = (
            "ImageSNN"
            if snn_score > cnn_score
            else "ImageCNN"
        )

        model_breakdown = f"""
        <table style="
            width:100%;
            margin-bottom:10px;
        ">
            <tr>
                <td><b>ImageCNN</b></td>
                <td style="text-align:right;">
                    {cnn_score:.2f}%
                </td>
            </tr>

            <tr>
                <td><b>ImageSNN</b></td>
                <td style="text-align:right;">
                    {snn_score:.2f}%
                </td>
            </tr>
        </table>

        <hr>

        <div style="margin-bottom:8px;">
            <div>
                <b>Performance Gap</b>
            </div>

            <div style="
                font-size:24px;
                font-weight:bold;
                color:#2C3E50;
                margin-bottom:10px;
            ">
                {abs(snn_score - cnn_score):.2f}%
            </div>
            
        </div>

        <div style="
            color:#E67E22;
            font-weight:bold;
        ">
            Best Performer: {best_model}
        </div>
        """    

    html = f"""
    <style>

    .thermo-wrapper {{
        display:flex;
        flex-direction:column;
        align-items:center;
        font-family:sans-serif;
        width:220px;
    }}

    .tooltip {{
        position:relative;
        display:inline-block;
    }}

    .tooltip-content {{

        visibility:hidden;
        opacity:0;

        transition:0.3s;

        position:absolute;

        left:50%;
        top:10px;
        transform: translateX(-10%);

        width:220px;

        background:white;

        border-radius:12px;

        box-shadow:
            0 4px 15px
            rgba(0,0,0,0.15);

        padding:14px;

        z-index:999;
    }}

    .tooltip:hover
    .tooltip-content {{

        visibility:visible;
        opacity:1;
    }}

    .value {{
        font-size:30px;
        font-weight:700;
        color:{colour};
        margin-left: 20px;
    }}

    .profile {{
        color:#666;
        font-size:14px;
        margin-left: 20px;
    }}
    </style>

    <div class="thermo-wrapper">

        <b>{payload_name}</b>

        <div class="tooltip">

        <svg
            width="240"
            height="260"
            viewBox="0 0 120 240"
        >

            <!-- fill -->

            <rect
                class="liquid"
                x="15"
                y="{fill_y}"
                width="12"
                height="{fill_height + 10}"
                rx="8"
                fill="{colour}"
            />

            <!-- bulb fill -->

            <circle
                cx="21"
                cy="182"
                r="15"
                fill="{colour}"
            />

            <!-- THERMOMETER SVG -->

            <path
                d="M21 14
                   a10 10 0 0 0-10 10
                   v140
                   a20 20 0 1 0 20 0
                   v-140
                   a10 10 0 0 0-10 -10"

                fill="none"
                stroke="#000"
                stroke-width="3"
            />

            <!-- tick marks -->
            <line x1="39" y1="25" x2="59" y2="25" stroke="#888"/>
            <line x1="39" y1="55" x2="49" y2="55" stroke="#888"/>
            <line x1="39" y1="85" x2="59" y2="85" stroke="#888"/>
            <line x1="39" y1="115" x2="49" y2="115" stroke="#888"/>
            <line x1="39" y1="145" x2="59" y2="145" stroke="#888"/>

            <!-- legend -->

            <text x="70" y="28" font-size="15" text-anchor="start">
                Conclusive
            </text>

            <text x="70" y="58" font-size="15" text-anchor="start">
            Strong
            </text>

            <text x="70" y="88" font-size="15" text-anchor="start">
            Moderate
            </text>

            <text x="70" y="118" font-size="15" text-anchor="start">
            Weak
            </text>

            <text x="70" y="148" font-size="15" text-anchor="start">
            Minimal
            </text>
        </svg>

        <div class="tooltip-content">

            <div style="
                font-size:14px;
                color:#666;
                margin-bottom:5px;
            ">
                Overall Detection Rate
            </div>

            <div style="
                font-size:32px;
                color:{colour};
                font-weight:bold;
                margin-bottom:12px;
            ">
                {score:.2f}%
            </div>

            {model_breakdown}

        </div>

        <div class="value">
            {score:.2f}%
        </div>

        <div class="profile">
            {profile}
        </div>

    </div>
    """

    st.iframe(
        html,
        height=420
    )