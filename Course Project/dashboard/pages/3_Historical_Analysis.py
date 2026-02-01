import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Historical Flood Analysis", layout="wide")
st.title("📜 Historical Flood Event Analysis")

st.markdown("""
This analysis identifies extreme rainfall events that exceeded safety thresholds over the last 40+ years.
It tracks when rainfall surpassed the **2-year, 5-year, and 10-year** return periods, which serve as key indicators for flood risk planning.
""")

# ------------------------------
# LOAD DATA
# ------------------------------
@st.cache_data
def load_historical_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Loading the provided dataset with SPI and Return Period info
    csv_path = os.path.join(base_dir, "..", "GeoSpatial Numerical and Categorical Data (For Prince).csv")
    
    try:
        df = pd.read_csv(csv_path)
        # Parse dates - adjusting logic based on known monthly format (YYYY-MM-01 based on metadata)
        # If 'date' column doesn't exist, we might need to construct it or use what's available
        # Based on metadata, 'date' should exist. If not, we look for 'Date'
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        elif 'Date' in df.columns:
            df['date'] = pd.to_datetime(df['Date'])
            df.rename(columns={'Date': 'date'}, inplace=True)
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_historical_data()

if df.empty:
    st.write("No data available.")
    st.stop()

# ------------------------------
# Sidebar / Filter
# ------------------------------
st.sidebar.header("Settings")

# Restrict to specific municipalities as requested
target_municipalities = [
    "Ada East", "Ada West", "Adenta Municipal", "Ayawaso West", 
    "Ga Central Municipal", "Ga East", "Ga South Municipal", 
    "Ga West Municipal", "Kpone Katamanso", "La Dade-Kotopon", 
    "La-Nkwantanang-Madina", "Ledzokuku Municipal", "Ningo/Prampram", 
    "Shai Osudoku", "Tema West Municipal"
]

if 'Name' in df.columns:
    # Get unique available municipalities from data
    available_munis = df['Name'].unique()
    # Intersect with target list to ensure we only show valid options that exist in data
    # Normalizing strings for better matching (strip)
    available_munis = [m.strip() for m in available_munis if isinstance(m, str)]
    
    # Show user list, but only functional ones. Or show ALL from user list and handle empty data.
    # User said "let the drop down show the list".
    municipalities = target_municipalities
else:
    municipalities = target_municipalities

# Default to "Adenta Municipal" or the first one available
default_index = 0
try:
    if "Adenta Municipal" in municipalities:
        default_index = municipalities.index("Adenta Municipal")
except:
    pass

selected_muni = st.sidebar.selectbox("Select Municipality/Region", municipalities, index=default_index)

# Filter data
if 'Name' in df.columns:
    df_muni = df[df['Name'] == selected_muni].sort_values('date')
else:
    st.error("Column 'Name' not found in dataset. Cannot filter by municipality.")
    df_muni = pd.DataFrame()

# ------------------------------
# DATA PREP (Severity Classification)
# ------------------------------
def get_severity(row):
    if row.get('exceeds_10yr') == 1:
        return "10-Year (Extreme)"
    elif row.get('exceeds_5yr') == 1:
        return "5-Year (High)"
    elif row.get('exceeds_2yr') == 1:
        return "2-Year (Moderate)"
    else:
        return "Normal"

df_muni['Severity'] = df_muni.apply(get_severity, axis=1)
df_severe = df_muni[df_muni['Severity'] != "Normal"].copy()


# ------------------------------
# ANALYSIS 2: THRESHOLD MONITOR (Line Chart)
# vs Return Periods
# ------------------------------
st.subheader("🌊 Rainfall Magnitude vs. Safety Thresholds")
st.caption("Comparison of actual monthly maximum rainfall against calculated 2-year and 10-year return period thresholds.")

# We need a metric to plot. 'monthly_max_rfh' is checking against return periods.
fig_threshold = go.Figure()

# Actual Rainfall
fig_threshold.add_trace(go.Scatter(
    x=df_muni['date'], 
    y=df_muni['monthly_max_rfh'],
    name="Max 10-Day Rain (Actual)",
    mode='lines',
    line=dict(color='royalblue', width=1.5),
    opacity=0.8
))

# 2-Year Threshold (Warning)
# Often return_2yr is a relatively constant value per location, or slowly changing.
fig_threshold.add_trace(go.Scatter(
    x=df_muni['date'], 
    y=df_muni['return_2yr'],
    name="2-Year Threshold (Warning)",
    mode='lines',
    line=dict(color='gold', width=2, dash='dash'),
    opacity=0.8
))

# 10-Year Threshold (Critical)
fig_threshold.add_trace(go.Scatter(
    x=df_muni['date'], 
    y=df_muni['return_10yr'],
    name="10-Year Threshold (Critical)",
    mode='lines',
    line=dict(color='crimson', width=2, dash='dot'),
    opacity=0.8
))

fig_threshold.update_layout(
    xaxis_title="Year",
    yaxis_title="Rainfall (mm)",
    template="plotly_white",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig_threshold, use_container_width=True)

# ------------------------------
# METRICS SUMMARY
# ------------------------------
st.subheader("Key Statistics")
col1, col2, col3, col4 = st.columns(4)

total_months = len(df_muni)
extreme_events = len(df_muni[df_muni['exceeds_10yr'] == 1])
high_events = len(df_muni[df_muni['exceeds_5yr'] == 1])
moderate_events = len(df_muni[df_muni['exceeds_2yr'] == 1])

col1.metric("Total Months Recorded", total_months)
col2.metric("2-Year Events (Mod)", moderate_events, help="Occasions where rainfall exceeded the 2-year return period.")
col3.metric("5-Year Events (High)", high_events, help="Occasions where rainfall exceeded the 5-year return period.")
col4.metric("10-Year Events (Extreme)", extreme_events, help="Occasions where rainfall exceeded the 10-year return period.")

# Recent alerts
if not df_severe.empty:
    st.write("### ⚠️ Most Recent Significant Events")
    recent = df_severe.sort_values('date', ascending=False).head(5)
    st.table(recent[['date', 'Severity', 'monthly_max_rfh', 'monthly_total_rfh']])
