import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Rainfall Forecast", layout="wide")
st.title("📈 Rainfall Forecast & Anomaly Analysis")

st.markdown("""
This section visualizes rainfall anomalies over time for selected regions.
It helps to identify periods of high or low rainfall and potential flood risk.
""")

# ------------------------------
# LOAD DATA
# ------------------------------
@st.cache_data
def load_rainfall_data():
    df = pd.read_csv("../forecast_precipitation_anomalies_adm0.csv")
    df.columns = df.columns.str.strip()
    df['date'] = pd.to_datetime(df['valid_year'].astype(str) + '-' +
                                df['valid_month'].astype(str) + '-01')
    return df

df = load_rainfall_data()

# ------------------------------
# SELECT REGION
# ------------------------------
st.subheader("Select Region")
regions = df['adm0_name'].unique()
selected_region = st.selectbox("Region", regions)

df_region = df[df['adm0_name'] == selected_region].sort_values('date')

# ------------------------------
# SELECT VARIABLE
# ------------------------------
st.subheader("Select Rainfall Variable")
numeric_cols = ['mean_anomaly', 'median_anomaly']
selected_col = st.selectbox("Variable", numeric_cols)

# ------------------------------
# YEAR FILTER
# ------------------------------
st.subheader("Filter by Year")
years = sorted(df_region['date'].dt.year.unique())
selected_years = st.multiselect("Select year(s)", years, default=years)
df_region_filtered = df_region[df_region['date'].dt.year.isin(selected_years)]

# ------------------------------
# LINE CHART WITH MOVING AVERAGE
# ------------------------------
st.subheader(f"{selected_col} Over Time for {selected_region}")

df_region_filtered['moving_avg'] = df_region_filtered[selected_col].rolling(window=3, min_periods=1).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_region_filtered['date'],
    y=df_region_filtered[selected_col],
    mode='lines+markers',
    name=selected_col
))
fig.add_trace(go.Scatter(
    x=df_region_filtered['date'],
    y=df_region_filtered['moving_avg'],
    mode='lines',
    name='3-Period Moving Avg',
    line=dict(dash='dash', color='orange')
))
fig.update_layout(
    xaxis_title="Date",
    yaxis_title=selected_col,
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# INTERPRETATION BLOCK
# ------------------------------
st.subheader("🌧️ Flood Risk Interpretation")
latest = df_region_filtered.iloc[-1][selected_col]

if latest > 1.5:
    st.error("⚠️ High positive rainfall anomaly detected. Elevated flood risk likely.")
elif latest > 0.5:
    st.warning("🌦 Moderate positive anomaly. Monitor for potential flooding.")
elif latest < -0.5:
    st.info("☀️ Below-normal rainfall. Flood risk is low.")
else:
    st.success("✅ Near-normal rainfall. No immediate flood concerns.")

# ------------------------------
# DATA PREVIEW
# ------------------------------
with st.expander(f"Preview Raw Data for {selected_region}"):
    st.dataframe(df_region_filtered[['date', 'mean_anomaly', 'median_anomaly']].tail(20))
