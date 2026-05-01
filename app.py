import streamlit as st
import pandas as pd
import folium
from pathlib import Path
from streamlit_folium import st_folium

st.set_page_config(page_title="Vision Zero Chicago Dashboard", layout="wide")

st.title("Vision Zero Chicago: Spatiotemporal Deep Learning Extension")

st.markdown("""
This dashboard presents the final project outputs: ConvLSTM/LGBM crash-risk predictions,
speed-camera fusion, computer-vision results, and equity-oriented safety findings.
""")

OUTPUTS = Path("outputs")

def load_csv(name):
    path = OUTPUTS / name
    if path.exists():
        return pd.read_csv(path)
    st.warning(f"Missing file: {path}")
    return pd.DataFrame()

# Load outputs
convlstm = load_csv("cdot_priority_cells_convlstm.csv")
lgbm = load_csv("cdot_priority_cells_lgbm.csv")
cameras = load_csv("cameras_per_cell.csv")
cv = load_csv("clip_copresence.csv")
mismatch = load_csv("mismatch_cells.csv")

# Sidebar
st.sidebar.header("Controls")

model_choice = st.sidebar.selectbox(
    "Prediction model",
    ["ConvLSTM", "LightGBM"]
)

priority = convlstm if model_choice == "ConvLSTM" else lgbm

max_points = st.sidebar.slider(
    "Number of priority cells to display",
    50, 1000, 300, 50
)

show_cameras = st.sidebar.checkbox("Show speed-camera layer", True)
show_cv = st.sidebar.checkbox("Show computer-vision clips", True)

# Metrics
c1, c2, c3, c4 = st.columns(4)

c1.metric("Selected Model", model_choice)
c2.metric("Priority Cells", len(priority))
c3.metric("Camera Cells", len(cameras))
c4.metric("CV Clips", len(cv))

# Map
st.subheader("Interactive Chicago Safety Map")

m = folium.Map(
    location=[41.84, -87.68],
    zoom_start=11,
    tiles="cartodbpositron"
)

tier_color = {
    "CRITICAL": "red",
    "HIGH": "orange",
    "MONITOR": "gold",
    "BASELINE": "gray"
}

if not priority.empty and {"lat", "lon"}.issubset(priority.columns):
    df = priority.dropna(subset=["lat", "lon"]).copy()

    if "rank" in df.columns:
        df = df.sort_values("rank")

    df = df.head(max_points)

    fg_priority = folium.FeatureGroup(name=f"{model_choice} Priority Cells")

    for _, row in df.iterrows():
        tier = row.get("tier", "BASELINE")
        color = tier_color.get(tier, "gray")

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
            radius=7 if tier in ["CRITICAL", "HIGH"] else 4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.70,
            popup=folium.Popup(popup, max_width=300),
            tooltip=f"{tier} | rank {row.get('rank', 'NA')}"
        ).add_to(fg_priority)

    fg_priority.add_to(m)

if show_cameras and not cameras.empty and {"lat", "lon"}.issubset(cameras.columns):
    fg_camera = folium.FeatureGroup(name="Speed Camera Violation Cells")

    max_v = cameras["violation_score"].max() if "violation_score" in cameras.columns else 1

    for _, row in cameras.dropna(subset=["lat", "lon"]).iterrows():
        v = row.get("violation_score", 0)
        radius = 4 + 10 * (v / max_v) if max_v > 0 else 4

        popup = f"""
        <b>Speed Camera Cell</b><br>
        <b>Violations/day:</b> {v:.2f}<br>
        <b>Cameras:</b> {row.get('n_cameras', 'NA')}<br>
        <b>Address:</b> {row.get('addresses', 'NA')}<br>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.35,
            popup=folium.Popup(popup, max_width=300),
            tooltip=f"Violations/day: {v:.1f}"
        ).add_to(fg_camera)

    fg_camera.add_to(m)

if show_cv and not cv.empty and {"lat", "lon"}.issubset(cv.columns):
    fg_cv = folium.FeatureGroup(name="Computer Vision Clips")

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

st_folium(m, width=None, height=700)

# Tables
st.subheader("Output Tables")

tab1, tab2, tab3, tab4 = st.tabs([
    "Priority Cells",
    "Speed Cameras",
    "Mismatch Analysis",
    "Computer Vision"
])

with tab1:
    st.dataframe(priority, use_container_width=True)

with tab2:
    st.dataframe(cameras, use_container_width=True)

with tab3:
    st.dataframe(mismatch, use_container_width=True)

with tab4:
    st.dataframe(cv, use_container_width=True)

st.markdown("---")
st.markdown("""
**Interpretation:** ConvLSTM is useful for broad citywide vulnerability scanning,
while LightGBM is stronger for concentrated hotspot prioritization. Speed-camera,
computer-vision, and public-reporting layers help explain whether predicted risk
aligns with enforcement patterns, pedestrian–vehicle exposure, and public perception.
""")
