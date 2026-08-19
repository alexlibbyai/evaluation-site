# Repo: evaluation-site
# Path: modules/fingerprint_visual.py

import streamlit as st
import streamlit.components.v1 as components

from modules.build_fingerprint import build_tooltip_script

def render_fingerprint(
    tp_cnn=None,
    tp_snn=None,
    tn_cnn=None,
    tn_snn=None,
    fp_cnn=None,
    fp_snn=None,
    fn_cnn=None,
    fn_snn=None,      
    ridge_1="#FF0000",
    ridge_2="#0000FF",
    ridge_3="#800080",
    ridge_4="#FFA500",
    ridge_5="#00AA00",
    width=400
):
    tp_diff = tp_snn - tp_cnn
    tn_diff = tn_snn - tn_cnn
    fp_diff = fp_snn - fp_cnn
    fn_diff = fn_snn - fn_cnn

    svg_markup = f"""
        <svg
        xmlns="http://www.w3.org/2000/svg"
        width={width}
        height="400"
        viewBox="0 0 512 512"
        fill="none"
        stroke="currentColor"
        stroke-width="12"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="fingerprint"
    >

    <style>
        .ridge {{
            transition:
                opacity 0.2s ease,
                filter 0.2s ease,
                transform 0.2s ease;

            transform-origin:center;
        }}

        .fingerprint:hover .ridge {{
            opacity:0.25;
            filter:grayscale(100%);
        }}

        .fingerprint .ridge:hover {{
            opacity:1;
            transform:scale(1.03);
            filter:none;
        }}

        .fingerprint-wrapper {{
            position:relative;
            display:inline-block;
        }}

        .tooltip-content {{
            font-family:sans-serif;
            visibility:hidden;
            opacity:0;
            padding:14px;
            transition:0.2s ease;
            position:absolute;
            top:20px;
            left:220px;
            width:180px;
            background:white;
            border:1px solid #E6EAF1;
            border-radius:12px;
            box-shadow:
                0 4px 12px rgba(0,0,0,.10),
                0 1px 3px rgba(0,0,0,.06);
            z-index:999;
        }}

        .tooltip-title {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        .tooltip-row {{
            display:flex;
            justify-content:space-between;

            font-size:15px;
            margin-bottom:6px;
        }}

        .tooltip-model {{
            font-weight:600;
        }}

        .tooltip-divider {{
            margin:12px 0;
            border:none;
            border-top:1px solid #D8DDE6;
        }}

        .tooltip-label {{
            font-size:14px;
            color:#667085;
        }}

        .tooltip-value {{
            font-size:28px;
            font-weight:700;
            color:#3498DB;
        }}

        .tooltip-insight {{
            margin-top:12px;
            font-size:14px;
            line-height:1.4;
        }}    

        .fingerprint-wrapper:hover
        .tooltip-content {{
            visibility:visible;
            opacity:1;
        }}
    </style>
        <g class="metric-group">
            <path class="ridge ridge-tp" fill="{ridge_1}" stroke="none" data-title="True Positives" data-cnn="{int(tp_cnn)}" data-snn="{int(tp_snn)}" data-diff="{tp_diff:+}"
            d="M390.42 75.28a10.45 10.45 0 0 1-5.32-1.44C340.72 50.08 302.35 40 256.35 40c-45.77 0-89.23 11.28-128.76 33.84C122 77 115.11 74.8 111.87 69a12.4 12.4 0 0 1 4.63-16.32A281.8 281.8 0 0 1 256.35 16c49.23 0 92.23 11.28 139.39 36.48a12 12 0 0 1 4.85 16.08 11.3 11.3 0 0 1-10.17 6.72" />
        </g>

        <g class="metric-group">
            <path class="ridge ridge-tn" title="True Negatives" fill="{ridge_2}" stroke="none" data-title="True Negatives" data-cnn="{int(tn_cnn)}" data-snn="{int(tn_snn)}" data-diff="{tn_diff:+}"
            d="M59.63 201.28a11.73 11.73 0 0 1-6.7-2.16 12.26 12.26 0 0 1-2.78-16.8c22.89-33.6 52-60 86.69-78.48 72.58-38.84 165.51-39.12 238.32-.24 34.68 18.48 63.8 44.64 86.69 78a12.29 12.29 0 0 1-2.78 16.8 11.26 11.26 0 0 1-16.18-2.88c-20.8-30.24-47.15-54-78.36-70.56-66.34-35.28-151.18-35.28-217.29.24-31.44 16.8-57.79 40.8-78.59 71a10 10 0 0 1-9.02 5.08" />
        </g>

        <g class="metric-group">
            <path class="ridge ridge-fn" title="False Negatives" fill="{ridge_4}" stroke="none" data-title="False Negatives" data-cnn="{int(fn_cnn)}" data-snn="{int(fn_snn)}" data-diff="{fn_diff:+}"
            d="M204.1 491a10.66 10.66 0 0 1-8.09-3.6C175.9 466.48 165 453 149.55 424c-16-29.52-24.27-65.52-24.27-104.16 0-71.28 58.71-129.36 130.84-129.36S387 248.56 387 319.84a11.56 11.56 0 1 1-23.11 0c0-58.08-48.32-105.36-107.72-105.36S148.4 261.76 148.4 319.84c0 34.56 7.39 66.48 21.49 92.4 14.8 27.6 25 39.36 42.77 58.08a12.67 12.67 0 0 1 0 17 12.44 12.44 0 0 1-8.56 3.68" />
        </g>

        <path class="ridge ridge-overall"  fill="{ridge_5}" stroke="none"      
        d="M370.75 447.4c-27.51 0-51.78-7.2-71.66-21.36a129.1 129.1 0 0 1-55-105.36 11.57 11.57 0 1 1 23.12 0 104.28 104.28 0 0 0 44.84 85.44c16.41 11.52 35.6 17 58.72 17a147.4 147.4 0 0 0 24-2.4c6.24-1.2 12.25 3.12 13.4 9.84a11.92 11.92 0 0 1-9.47 13.92 152.3 152.3 0 0 1-27.95 2.88Z">
        </path>

        <g class="metric-group">        
            <path class="ridge ridge-fp" title="False Positives" fill="{ridge_3}" stroke="none" data-title="False Positives" data-cnn="{int(fp_cnn)}" data-snn="{int(fp_snn)}" data-diff="{fp_diff:+}"
            d="M323.38 496a13 13 0 0 1-3-.48c-36.76-10.56-60.8-24.72-86-50.4-32.37-33.36-50.16-77.76-50.16-125.28 0-38.88 31.9-70.56 71.19-70.56s71.2 31.68 71.2 70.56c0 25.68 21.5 46.56 48.08 46.56s48.08-20.88 48.08-46.56c0-90.48-75.13-163.92-167.59-163.92-65.65 0-125.75 37.92-152.79 96.72-9 19.44-13.64 42.24-13.64 67.2 0 18.72 1.61 48.24 15.48 86.64 2.32 6.24-.69 13.2-6.7 15.36a11.34 11.34 0 0 1-14.79-7 276.4 276.4 0 0 1-16.88-95c0-28.8 5.32-55 15.72-77.76 30.75-67 98.94-110.4 173.6-110.4 105.18 0 190.71 84.24 190.71 187.92 0 38.88-31.9 70.56-71.2 70.56s-71.2-31.68-71.2-70.56c.01-25.68-21.49-46.6-48.07-46.6s-48.08 20.88-48.08 46.56c0 41 15.26 79.44 43.23 108.24 22 22.56 43 35 75.59 44.4 6.24 1.68 9.71 8.4 8.09 14.64a11.39 11.39 0 0 1-10.87 9.16" />
        </g>
    </svg>
    """

    html = f"""
    <div class="fingerprint-wrapper">

        {svg_markup}

        <div
            id="tooltip"
            class="tooltip-content"
        >
            Hover over a ridge to compare metrics.
        </div>

    </div>

    <script>
        {build_tooltip_script()}
    </script>
    """

    st.iframe(
        html,
        height=450
    )    
