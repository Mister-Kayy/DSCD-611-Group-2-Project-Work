import streamlit as st

st.header("ℹ️ About the Flood Early Warning System")

st.markdown("""
## Project Overview

This dashboard is a **data-driven flood early warning support system**
designed to support disaster preparedness and decision-making in Ghana,
with a focus on **Greater Accra**.

It integrates:
- Rainfall forecast anomalies
- Historical rainfall patterns
- Engineered hydrometeorological indicators
- Machine learning–ready features

---

## Data Sources

### 🌧️ Rainfall Data
- CHIRPS and processed rainfall observations
- Aggregated at administrative and municipal levels

### 🧠 Engineered Features
- Rainfall intensity and accumulation (rfh, r3h)
- Lagged rainfall effects
- Seasonal indicators
- Rainfall surge detection
- Binary high-rainfall flags

---

## Methodology

### 1️⃣ Rainfall Forecast Analysis
Rainfall anomalies are analyzed over time to identify:
- Above-normal rainfall (flood-prone)
- Near-normal conditions
- Below-normal conditions

### 2️⃣ Flood Risk Assessment
Flood risk is inferred using:
- Recent rainfall intensity
- Temporal persistence of rainfall
- Sudden rainfall increases
- Historical wetness indicators

A rule-based interpretation layer translates these signals into:
- Low Risk
- Moderate Risk
- High Risk alerts

---

## Machine Learning Integration (Ongoing)

The system is designed to integrate:
- Tree-based models (Random Forest, XGBoost)
- Time-aware training strategies
- Classification of flood risk likelihood

---

## Disclaimer

This system is intended for **decision support and academic demonstration**.
It does not replace official meteorological or emergency warnings.

---

### Developed by  
**Group 2:**
Etornam Agbetonyo
Charles Ahorsu
Kwame Atua-Ntow
Prince Obeng Nkoah        
""")
