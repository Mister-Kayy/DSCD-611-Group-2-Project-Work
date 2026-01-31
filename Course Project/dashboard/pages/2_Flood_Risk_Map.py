# 2_Flood_Risk_Map.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Flood Risk Assessment", layout="wide")
st.title("🗺️ Flood Risk Assessment – Greater Accra")


st.markdown("""
This section uses rainfall indicators, lag effects, and surge metrics
to assess flood risk at the municipal level.
""")

# ------------------------------
# LOAD DATA
# ------------------------------
@st.cache_data
def load_flood_data():
    df = pd.read_csv("../Charles/Greater Accra Rainfall Processed Data (for Charles ML).csv")
    df.columns = df.columns.str.lower().str.strip()
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_flood_data()

# ------------------------------
# SELECT MUNICIPALITY
# ------------------------------
st.subheader("Select Municipality")
municipalities = sorted(df['municipality'].unique())
selected_muni = st.selectbox("Municipality", municipalities)
df_muni = df[df['municipality'] == selected_muni].sort_values('date')
latest = df_muni.iloc[-1]

# ------------------------------
# METRICS CARDS
# ------------------------------
st.subheader("📊 Latest Flood Risk Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Recent Rainfall (rfh)", f"{latest['rfh']:.2f} mm")
col2.metric("3-Dekad Rainfall (r3h)", f"{latest['r3h']:.2f} mm")
col3.metric("Rainfall Surge", f"{latest['rfh_rate_change']:.2f}")

# ------------------------------
# FLOOD RISK LOGIC + COLORED CARD
# ------------------------------
st.subheader("⚠️ Flood Risk Level")
risk_score = 0
if latest['high_rainfall_flag'] == 1 and latest['rfh_rate_change'] > 0:
    risk_score = 3
elif latest['high_rainfall_flag'] == 1:
    risk_score = 2
else:
    risk_score = 1

risk_level = "LOW"
risk_color = "green"
if risk_score == 2:
    risk_level = "MODERATE"
    risk_color = "orange"
elif risk_score == 3:
    risk_level = "HIGH"
    risk_color = "red"

st.markdown(f"""
<div style="padding: 15px; border-radius: 12px; background-color: {risk_color}; color: white; text-align: center;">
    <h3>⚠️ Flood Risk Level: {risk_level}</h3>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# YEAR FILTER
# ------------------------------
st.subheader("Filter by Year")
years = sorted(df_muni['date'].dt.year.unique())
selected_years = st.multiselect("Select year(s)", years, default=years)
df_muni_filtered = df_muni[df_muni['date'].dt.year.isin(selected_years)]

# ------------------------------
# TREND CHART (PLOTLY)
# ------------------------------
st.subheader("📈 Rainfall Trend")
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=df_muni_filtered['date'],
    y=df_muni_filtered['rfh'],
    mode='lines+markers',
    name='rfh',
    line=dict(color='royalblue', width=2),
    marker=dict(size=5)
))
fig_trend.add_trace(go.Scatter(
    x=df_muni_filtered['date'],
    y=df_muni_filtered['r3h'],
    mode='lines+markers',
    name='r3h',
    line=dict(color='orange', width=2),
    marker=dict(size=5)
))
fig_trend.update_layout(
    xaxis=dict(showgrid=True, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridcolor='lightgray'),
    hovermode="x unified",
    template="plotly_white",
    title=f"Rainfall Trends for {selected_muni}"
)

# ------------------------------
# HEATMAP (MATPLOTLIB / SEABORN)
# ------------------------------
st.subheader("🌡️ Monthly Rainfall Heatmap")
heatmap_data = df_muni_filtered.copy()
heatmap_data['month'] = heatmap_data['date'].dt.month
heatmap_data['year'] = heatmap_data['date'].dt.year
pivot = heatmap_data.pivot_table(
    index='month',
    columns='year',
    values='rfh',
    aggfunc='mean'
).sort_index(ascending=False)

heatmap_fig, ax = plt.subplots(figsize=(12,5))
sns.heatmap(
    pivot,
    annot=True,
    fmt=".1f",
    cmap="Blues",
    linewidths=0.5,
    linecolor='gray',
    ax=ax
)
ax.set_xlabel("Year")
ax.set_ylabel("Month")

# ------------------------------
# TABS FOR ORGANIZATION
# ------------------------------
tab1, tab2, tab3 = st.tabs(["Trend Chart", "Heatmap", "Data Table"])
with tab1:
    st.plotly_chart(fig_trend, use_container_width=True)
with tab2:
    st.pyplot(heatmap_fig)
with tab3:
    st.dataframe(df_muni_filtered[['date','rfh','r3h','rfh_rate_change','high_rainfall_flag']].tail(20))
