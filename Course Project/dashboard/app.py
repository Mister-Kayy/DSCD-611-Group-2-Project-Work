import streamlit as st

st.set_page_config(
    page_title="Ghana Rainfall & Flood Risk Early Warning System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("### 🌍 Navigation")
st.sidebar.markdown("Select pages from the sidebar:\n\n"
                    "- 📈 Forecast: Rainfall anomalies over time\n"
                    "- 🗺️ Flood Risk Map: Municipal-level risk indicators\n"
                    "- 📜 Historical Analysis: Past flood events\n"
                    "- ℹ️ About: Methodology and dataset info")


page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background: linear-gradient(
rgba(10,15,25,0.85),
rgba(10,15,25,0.95)
),
url("assets/weather_bg.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}

[data-testid="stSidebar"] {
background-color: rgba(20,20,30,0.95);
}

h1, h2, h3 {
color: #FFFFFF;
}
</style>
"""
glass_style = """
<style>
.block-container {
    background-color: rgba(30, 35, 45, 0.75);  /* semi-transparent dark layer */
    padding: 2rem;
    border-radius: 15px;
}

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF;
}

.stMetric {
    background-color: rgba(50, 55, 70, 0.7);
    padding: 1rem;
    border-radius: 10px;
}
</style>
"""
st.markdown(glass_style, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("🌧️ Ghana Rainfall & Flood Risk Early Warning System")
st.subheader("📈 Rainfall Forecast & Anomaly Analysis")
st.subheader("🗺️ Flood Risk Assessment – Greater Accra")
st.subheader("ℹ️ About / Methodology")

st.markdown("## 📊 Key Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌧 Avg Rainfall (5yr)", "124 mm", "+6%")
col2.metric("⚠ High Risk Districts", "6", "+1")
col3.metric("📈 10-Year Extreme Events", "3", "Stable")
col4.metric("🌡 Rainfall Anomaly Index", "1.42", "Above Normal")

st.markdown("---")