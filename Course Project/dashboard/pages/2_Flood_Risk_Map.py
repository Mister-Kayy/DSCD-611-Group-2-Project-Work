import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

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
# LOAD DATA (Kept for Municipality Selector)
# ------------------------------
@st.cache_data
def load_flood_data():
    # Helper to find the CSV relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Assuming CSV location logic remains the same or updated relative to project
    # Note: Original code had: "../Charles/Greater Accra Rainfall Processed Data (for Charles ML).csv"
    # We will keep absolute path resolution to be safe if the original worked
    csv_path = os.path.join(base_dir, "..", "Charles", "Greater Accra Rainfall Processed Data (for Charles ML).csv")
    
    # Fallback if the user's path structure is different, try looking in current dir or just suppress
    # But for now we stick to original logic:
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        # Fallback for demonstration if file is missing in this env
        # Attempt to read from original raw path if strictly needed or just fail gracefully
        # Reverting to exact original string slightly adjusted for cross-platform
        # Original: pd.read_csv("../Charles/Greater Accra Rainfall Processed Data (for Charles ML).csv")
        df = pd.read_csv("../Charles/Greater Accra Rainfall Processed Data (for Charles ML).csv")

    df.columns = df.columns.str.lower().str.strip()
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_flood_data()
    # ------------------------------
    # SELECT MUNICIPALITY
    # ------------------------------
    st.subheader("Select Municipality")
    municipalities = sorted(df['municipality'].unique())
    selected_muni = st.selectbox("Municipality", municipalities)
except Exception as e:
    st.error(f"Data loading failed: {e}")
    # Fallback so map still shows
    st.subheader("Select Municipality")
    st.selectbox("Municipality", ["Adenta Municipal", "Ayawaso East", "Ayawaso West", "Ga East", "Accra Metropolitan"]) 

# ------------------------------
# DISPLAY FLOOD RISK STYLE MAP
# ------------------------------
map_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'flood_risk_style_map.html')

try:
    with open(map_path, 'r', encoding='utf-8') as f:
        map_html = f.read()
    
    # Display the map full width
    components.html(map_html, height=800, scrolling=False)
except Exception as e:
    st.error(f"Could not load map file: {e}")
