import streamlit as st
import joblib

# trained models----------------------------------------------------------------------------------------------------------------------------

soh_model = joblib.load("SOH_model.joblib")
soh_imputer = joblib.load("soh_imputer.joblib")
range_model = joblib.load("range_model.joblib")
range_imputer = joblib.load("range_imputer.joblib")

# title and description---------------------------------------------------------------------------------------------------------------------

st.set_page_config(page_title="Battery Health & Range Predictor", page_icon="🔋")
st.title("🔋 Battery Health & Range Prediction")
st.markdown(" this app is to predict the **State of Health (SOH)** and **driving range** of an EV battery.")

# Input fields------------------------------------------------------------------------------------------------------------------------------

st.subheader("Enter Battery & Trip Parameters")
col1, col2 = st.columns(2)
ambient_temp = col1.number_input("Ambient Temperature (°C)", min_value=-10.0, max_value=60.0, value=30.0)
Re = col1.number_input("Re-Electrolyte Resistance (Ω)", min_value=0.0, max_value=1.0, value=0.055)
Rct = col1.number_input("Rct-Charge Transfer Resistance (Ω)", min_value=0.0, max_value=1.0, value=0.20)

efficiency = col2.number_input("Efficiency (km/kWh)", min_value=3.0, max_value=8.0, value=5.7)
terrain = col2.slider("Terrain Factor (Hilly = 0.75, Flat = 1.0)", min_value=0.7, max_value=1.0, value=0.9)
vehicle_weight = col2.number_input("Vehicle Weight (kg)", min_value=1000, max_value=3000, value=1500)

# Predict button----------------------------------------------------------------------------------------------------------------------------

if st.button("🚀 Predict"):

# Predict SOH----------------------------------------------------------------------------------------------------------------------------

    X = soh_imputer.transform([[ambient_temp, Re, Rct]])
    capacity = soh_model.predict(X)[0]
    soh_percent = (capacity / 1.1) * 100  # Assuming 1.1 Ah nominal capacity

# Predict Range-------------------------------------------------------------------------------------------------------------------------

    Xr = range_imputer.transform([[soh_percent, efficiency, ambient_temp, terrain, vehicle_weight]])
    predicted_range = range_model.predict(Xr)[0]

# Display results------------------------------------------------------------------------------------------------------------------------

    st.success("✅ Prediction Complete!")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Battery Health (SOH)", value=f"{soh_percent:.2f}%")
    col2.metric(label="Battery Capacity", value=f"{capacity:.3f} Ah")
    col3.metric(label="Estimated Range", value=f"{predicted_range:.1f} km")

# Additional insights----------------------------------------------------------------------------------------------------------------------

    st.subheader("📊 Battery Health Status")

# Health status indicator-------------------------------------------------------------------------------------------------------------------

    if soh_percent >= 80:
        st.info("✅ **Excellent** - Battery is in great condition")
    elif soh_percent >= 60:
        st.warning("⚠️ **Good** - Battery is performing well")
    elif soh_percent >= 40:
        st.warning("⚠️ **Fair** - Consider maintenance soon")
    else:
        st.error("❌ **Poor** - Battery replacement recommended")

# Additional metrics-------------------------------------------------------------------------------------------------------------------------

    col4, col5, col6 = st.columns(3)
    col4.metric(label="Ambient Temperature", value=f"{ambient_temp:.1f}°C")
    col5.metric(label="Charge Transfer Resistance", value=f"{Rct:.4f} Ω")
    col6.metric(label="Electrolyte Resistance", value=f"{Re:.4f} Ω")

# Weight impact analysis--------------------------------------------------------------------------------------------------------------------

    st.subheader("⚖️ Weight Impact Analysis")
    weight_factor = vehicle_weight / 1500  # Reference weight: 1500 kg
    range_without_weight = predicted_range / weight_factor
    weight_loss_percent = ((predicted_range - range_without_weight) / range_without_weight) * 100
    
    col9, col10 = st.columns(2)
    col9.metric(label="Vehicle Weight", value=f"{vehicle_weight} kg")
    col10.metric(label="Weight Impact on Range", value=f"{abs(weight_loss_percent):.1f}%", delta=f"{abs(weight_loss_percent):.1f}%")

# Range breakdown---------------------------------------------------------------------------------------------------------------------------

    st.subheader("🛣️ Range Breakdown")
    optimal_range = predicted_range
    worst_case_range = predicted_range * 0.8  # 20% reduction in harsh conditions
    col7, col8 = st.columns(2)
    col7.metric(label="Optimal Conditions Range", value=f"{optimal_range:.1f} km")
    col8.metric(label="Worst Case Range", value=f"{worst_case_range:.1f} km")

    

st.markdown("---")
st.caption("Developed by Arun Sajwan | AICTE Electric Vehicle Project")
