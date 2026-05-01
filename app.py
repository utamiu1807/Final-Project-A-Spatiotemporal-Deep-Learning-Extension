import streamlit as st
import pandas as pd
import folium
from pathlib import Path
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Chicago Crash Risk",
    layout="wide"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

OUTPUTS = Path("outputs")

def load_csv(name):
    path = OUTPUTS / name
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

convlstm = load_csv("cdot_priority_cells_convlstm.csv")
lgbm = load_csv("cdot_priority_cells_lgbm.csv")
cameras = load_csv("cameras_per_cell.csv")
mismatch = load_csv("mismatch_cells.csv")
cv = load_csv("clip_copresence.csv")
sentiment = load_csv("chicago_traffic_sentiment.csv")
equity = load_csv("equity_audit_convlstm.csv")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Configuration")

model_choice = st.sidebar.selectbox(
    "Prediction model",
    ["ConvLSTM", "LightGBM"]
)

priority = convlstm if model_choice == "ConvLSTM" else lgbm

show_cameras = st.sidebar.checkbox("Show speed-camera layer", True)
show_cv = st.sidebar.checkbox("Show CV clip layer", True)

max_points = st.sidebar.slider(
    "Max priority cells on map",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🚦 Chicago Crash Risk")
st.markdown(
    "Spatiotemporal forecasting for Vision Zero Chicago · MSPPM-DA Final Project"
)

# --------------------------------------------------
# Summary cards
# --------------------------------------------------

critical_count = 0
high_count = 0
actual_severe = 0
top_capture = None

if not priority.empty:
    if "tier" in priority.columns:
        critical_count = (priority["tier"] == "CRITICAL").sum()
        high_count = (priority["tier"] == "HIGH").sum()
    if "true" in priority.columns:
        actual_severe = int(priority["true"].sum())

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("CRITICAL cells", f"{critical_count:,}")

with c2:
    st.metric("HIGH cells", f"{high_count:,}")

with c3:
    st.metric("Actual severe crashes", f"{actual_severe:,}")

with c4:
    st.metric("Selected model", model_choice)

# --------------------------------------------------
# Tabs ABOVE map
# --------------------------------------------------

tab_map, tab_detail, tab_compare, tab_camera, tab_cv, tab_equity, tab_sentiment, tab_about = st.tabs(
    [
        "🗺️ Risk Map",
        "📋 Output Tables",
        "📊 Model Comparison",
        "📷 Speed Camera Fusion",
        "🎥 Computer Vision",
        "⚖️ Equity Audit",
        "💬 Sentiment",
        "ℹ️ About"
    ]
)

# --------------------------------------------------
# TAB 1 — Risk Map
# --------------------------------------------------

with tab_map:
    st.subheader("Interactive Chicago Risk Map")

    m = folium.Map(
        location=[41.84, -87.68],
        zoom_start=11,
        tiles="cartodbpositron"
    )

    tier_color = {
        "CRITICAL": "#b91c1c",
        "HIGH": "#ea580c",
        "MONITOR": "#facc15",
        "BASELINE": "#9ca3af"
    }

    tier_radius = {
        "CRITICAL": 11,
        "HIGH": 8,
        "MONITOR": 5,
        "BASELINE": 3
    }

    # Priority cells
    if not priority.empty and {"lat", "lon"}.issubset(priority.columns):
        df = priority.dropna(subset=["lat", "lon"]).copy()

        if "rank" in df.columns:
            df = df.sort_values("rank")

        df = df.head(max_points)

        fg_priority = folium.FeatureGroup(
            name=f"{model_choice} priority cells",
            show=True
        )

        for _, row in df.iterrows():
            tier = row.get("tier", "BASELINE")
            color = tier_color.get(tier, "#9ca3af")

            popup = f"""
            <b>{model_choice} Priority Cell</b><br>
            <b>Tier:</b> {tier}<br>
            <b>Rank:</b> {row.get('rank', 'NA')}<br>
            <b>Predicted severe:</b> {row.get('pred', 'NA')}<br>
            <b>Observed severe:</b> {row.get('true', 'NA')}<br>
            <b>Grid:</b> ({row.get('h', 'NA')}, {row.get('w', 'NA')})
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=tier_radius.get(tier, 4),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.72,
                weight=1.5,
                popup=folium.Popup(popup, max_width=320),
                tooltip=f"{tier} | rank {row.get('rank', 'NA')}"
            ).add_to(fg_priority)

        fg_priority.add_to(m)

    # Camera cells
    if show_cameras and not cameras.empty and {"lat", "lon"}.issubset(cameras.columns):
        fg_cameras = folium.FeatureGroup(
            name="Speed-camera violation cells",
            show=True
        )

        max_v = cameras["violation_score"].max() if "violation_score" in cameras.columns else 1

        for _, row in cameras.dropna(subset=["lat", "lon"]).iterrows():
            v = row.get("violation_score", 0)
            radius = 3 + 10 * (v / max_v) if max_v > 0 else 4

            popup = f"""
            <b>Speed Camera Cell</b><br>
            <b>Violations/day:</b> {v:.2f}<br>
            <b>Cameras:</b> {row.get('n_cameras', 'NA')}<br>
            <b>Address:</b> {row.get('addresses', 'NA')}<br>
            <b>Grid:</b> ({row.get('h', 'NA')}, {row.get('w', 'NA')})
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=radius,
                color="#2563eb",
                fill=True,
                fill_color="#2563eb",
                fill_opacity=0.35,
                popup=folium.Popup(popup, max_width=320),
                tooltip=f"Violations/day: {v:.1f}"
            ).add_to(fg_cameras)

        fg_cameras.add_to(m)

    # CV clips
    if show_cv and not cv.empty and {"lat", "lon"}.issubset(cv.columns):
        fg_cv = folium.FeatureGroup(
            name="Computer vision clips",
            show=True
        )

        for _, row in cv.dropna(subset=["lat", "lon"]).iterrows():
            popup = f"""
            <b>CV Clip:</b> {row.get('clip_id', 'NA')}<br>
            <b>Category:</b> {row.get('category', 'NA')}<br>
            <b>Pedestrians/frame:</b> {row.get('mean_pedestrian_count', 0):.3f}<br>
            <b>Vehicles/frame:</b> {row.get('mean_vehicle_count', 0):.3f}<br>
            <b>Copresence:</b> {row.get('copresence_rate', 0):.2%}<br>
            <b>Interaction:</b> {row.get('interaction_rate', 0):.2%}
            """

            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(popup, max_width=350),
                tooltip=f"CV Clip {row.get('clip_id', '')}",
            ).add_to(fg_cv)

        fg_cv.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    st_folium(m, width=None, height=720)

# --------------------------------------------------
# TAB 2 — Output Tables
# --------------------------------------------------

with tab_detail:
    st.subheader("Output Tables")

    table_choice = st.selectbox(
        "Select output table",
        [
            "Priority cells",
            "Speed-camera cells",
            "Mismatch analysis",
            "Computer vision",
            "Equity audit",
            "Sentiment"
        ]
    )

    if table_choice == "Priority cells":
        st.dataframe(priority, use_container_width=True)

    elif table_choice == "Speed-camera cells":
        st.dataframe(cameras, use_container_width=True)

    elif table_choice == "Mismatch analysis":
        st.dataframe(mismatch, use_container_width=True)

    elif table_choice == "Computer vision":
        st.dataframe(cv, use_container_width=True)

    elif table_choice == "Equity audit":
        st.dataframe(equity, use_container_width=True)

    elif table_choice == "Sentiment":
        st.dataframe(sentiment, use_container_width=True)

# --------------------------------------------------
# TAB 3 — Model Comparison
# --------------------------------------------------

with tab_compare:
    st.subheader("Model Comparison")

    comparison = pd.DataFrame({
        "Model": [
            "Historical average",
            "Negative Binomial GLM",
            "LightGBM-Poisson",
            "ConvLSTM"
        ],
        "Poisson deviance": [
            1.302,
            0.862,
            0.883,
            0.411
        ],
        "ECE": [
            0.069,
            0.071,
            0.088,
            0.020
        ],
        "PAI@200": [
            8.38,
            3.17,
            3.18,
            5.30
        ],
        "Capture@200": [
            "24.4%",
            "26.1%",
            "26.2%",
            "15.4%"
        ]
    })

    st.dataframe(comparison, use_container_width=True)

    st.markdown("""
    **Interpretation:** ConvLSTM achieved the strongest aggregate calibration and lowest
    Poisson deviance, while LightGBM produced sharper hotspot prioritization.
    ConvLSTM is best understood as a citywide vulnerability-scanning model;
    LightGBM is stronger for concentrated top-k operational targeting.
    """)

# --------------------------------------------------
# TAB 4 — Speed Camera Fusion
# --------------------------------------------------

with tab_camera:
    st.subheader("Speed-Camera Fusion and Mismatch Analysis")

    st.markdown("""
    This section compares predicted severe-crash risk against real speed-camera violation
    activity. Preventative cells have high enforcement activity but lower predicted
    severity. Enforcement-gap cells have high predicted severity but lower enforcement
    activity.
    """)

    st.dataframe(cameras, use_container_width=True)

    if not mismatch.empty:
        st.subheader("Mismatch Cells")
        st.dataframe(mismatch, use_container_width=True)

# --------------------------------------------------
# TAB 5 — Computer Vision
# --------------------------------------------------

with tab_cv:
    st.subheader("Computer Vision Pilot")

    st.markdown("""
    YOLOv8 was used as a pilot computer-vision layer to measure pedestrian–vehicle
    copresence and interaction rates from selected video clips. Because only a small
    number of clips were analyzed, this section should be interpreted as a feasibility
    demonstration rather than citywide statistical evidence.
    """)

    st.dataframe(cv, use_container_width=True)

# --------------------------------------------------
# TAB 6 — Equity Audit
# --------------------------------------------------

with tab_equity:
    st.subheader("Equity Audit")

    st.markdown("""
    The equity audit evaluates whether predicted severe-crash risk is concentrated in
    historically underserved communities. The purpose is not to label communities as
    dangerous, but to identify where infrastructure investment may be most needed.
    """)

    st.dataframe(equity, use_container_width=True)

# --------------------------------------------------
# TAB 7 — Sentiment
# --------------------------------------------------

with tab_sentiment:
    st.subheader("Public-Reported Traffic Safety Sentiment")

    st.markdown("""
    This section compares public complaint sentiment with predicted crash-risk hotspots.
    Weak alignment may indicate that complaint systems underrepresent latent traffic
    danger in some communities.
    """)

    st.dataframe(sentiment, use_container_width=True)

# --------------------------------------------------
# TAB 8 — About
# --------------------------------------------------

with tab_about:
    st.subheader("About This Dashboard")

    st.markdown("""
    This dashboard is part of a Vision Zero Chicago final project.

    **Project layers:**

    1. Spatiotemporal crash forecasting using ConvLSTM  
    2. LightGBM-Poisson hotspot comparison  
    3. Speed-camera mismatch analysis  
    4. YOLOv8 computer-vision pilot  
    5. Public traffic-safety sentiment analysis  
    6. Equity audit by Chicago community area  

    **Main policy insight:**  
    Predictive traffic-safety systems should guide preventative infrastructure
    investment, corridor redesign, lighting improvement, crosswalk protection,
    and pedestrian-safety interventions rather than relying solely on enforcement.
    """)
