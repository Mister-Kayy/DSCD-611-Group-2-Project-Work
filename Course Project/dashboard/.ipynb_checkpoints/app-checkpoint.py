import streamlit as st

st.set_page_config(
    page_title="Ghana Rainfall & Flood Risk Early Warning System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("### 🌍 Navigation")
st.sidebar.markdown(
    "Select pages from the sidebar:\n\n"
    "- 📈 Forecast: Rainfall anomalies over time\n"
    "- 🗺️ Flood Risk: Municipal-level risk indicators\n"
    "- ℹ️ About: Methodology and dataset info"
)

st.image("assets/app.png", width=12000)

page_bg_img = """
<style>
body {
background-image: url("assets/weather_bg.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("🌧️ Ghana Rainfall & Flood Risk Early Warning System")
st.subheader("📈 Rainfall Forecast & Anomaly Analysis")
st.subheader("🗺️ Flood Risk Assessment – Greater Accra")
st.subheader("ℹ️ About / Methodology")

