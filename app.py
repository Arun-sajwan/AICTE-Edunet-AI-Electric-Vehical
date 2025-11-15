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


import google.generativeai as genai
from dotenv import load_dotenv
import os


# Load API Key---------------------------------------------------------------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Try configuring the API
gemini_enabled = False
try:
    if api_key:
        genai.configure(api_key=api_key)
        gemini_enabled = True
except:
    gemini_enabled = False


# Local Rule-Based Chatbot-----------------------------------------------------------------------

def local_chatbot(user_msg):
    m = user_msg.lower()

    # Greetings
    if any(g in m for g in ("hello", "hi", "hey")):
        return "Hello! I can help with battery SOH, range estimates, charging tips, maintenance and EV best practices."

    # SOH / battery health
    if any(k in m for k in ("soh", "state of health", "battery health")):
        return ("SOH (State of Health) is a measure of remaining battery capacity vs nominal capacity. "
                "If you know capacity: SOH = (measured_capacity / nominal_capacity) × 100%. "
                "Values >80% are generally good; <40% may need replacement depending on vehicle use.")

    if "how is soh calculated" in m or "calculate soh" in m:
        return "SOH is computed from measured capacity divided by nominal capacity (e.g., Ah) and expressed as a percentage."

    # Range & factors
    if any(k in m for k in ("range", "driving range", "estimated range")):
        return ("Estimated range depends on SOH, vehicle efficiency (km/kWh), ambient temperature, terrain and vehicle weight. "
                "Higher SOH and efficiency => longer range; cold temps and heavy loads reduce range.")

    if any(k in m for k in ("improve range", "increase range", "tips", "how to increase")):
        return ("To improve range: reduce vehicle weight, drive smoothly at moderate speeds, keep tires properly inflated, "
                "limit HVAC use, use eco driving modes, and keep battery temperature near optimal (≈20–25°C).")

    # Charging practices
    if any(k in m for k in ("charge", "charging", "fast charge", "dcfc")):
        return ("Regular charging to 80% and avoiding frequent 100% charges can extend battery life. "
                "Fast charging is convenient but frequent use may accelerate degradation; balance fast-charge use with slower charging.")

    # Temperature effects
    if any(k in m for k in ("temperature", "cold", "hot", "ambient")):
        return ("Battery performance degrades in very cold or very hot conditions. Cold reduces instant capacity and power; "
                "heat accelerates long-term degradation. Thermal management is important.")

    # Weight impact
    if any(k in m for k in ("weight", "kg", "payload")):
        return ("Extra weight increases energy consumption roughly proportional to the added mass on typical driving cycles. "
                "Reducing unnecessary load improves range.")

    # Maintenance / replacement
    if any(k in m for k in ("replace battery", "battery replacement", "when replace", "replace")):
        return ("Consider replacement or professional inspection when SOH is consistently low (e.g., <40%) or when range and performance decline significantly.")

    if any(k in m for k in ("maintenance", "service", "checkup")):
        return ("Regular checks: battery health diagnostics, coolant/thermal system checks, tire pressure, and software updates from manufacturer.")

    # Regenerative braking
    if "regenerative" in m or "regen" in m:
        return ("Regenerative braking recovers kinetic energy to recharge the battery and improves efficiency, especially in city driving.")

    # Tire pressure / HVAC
    if "tire" in m or "tire pressure" in m:
        return "Low tire pressure increases rolling resistance and reduces range. Keep tires inflated to manufacturer specs."
    if any(k in m for k in ("hvac", "air conditioning", "heater")):
        return "HVAC use (heating or AC) can noticeably reduce range; use seat heaters and pre-conditioning where possible."

    # Safety & storage
    if any(k in m for k in ("safety", "fire", "thermal runaway")):
        return ("For safety, follow manufacturer guidelines for charging and storage, avoid physical damage, and seek professional help for swollen or hot cells.")

    # Connectors & standards
    if any(k in m for k in ("ccs", "type 2", "chademo", "connector", "plug")):
        return ("Common charging standards: CCS (fast DC + AC in some regions), CHAdeMO (older fast DC), Type 2 (AC). Adapter/support depends on vehicle and charger.")

    # Modeling & data questions
    if any(k in m for k in ("model", "accuracy", "mae", "r2", "r²")):
        return ("Models were trained with RandomForest regressors. Evaluate with MAE and R². More data and time-series features improve robustness.")

    # Misc EV tips
    if any(k in m for k in ("range anxiety", "planning", "trip")):
        return ("Plan trips with buffer, locate chargers along route, and consider charging stops based on expected range and traffic/terrain.")

    # Fallbacks for common short queries
    if "help" in m:
        return "Ask about SOH, range, charging best practices, maintenance, or how specific factors (weight/temp) affect range."

    # Default fallback
    return "Sorry, I couldn't understand that. Ask about SOH, estimated range, charging, maintenance or how temperature/weight affect performance."



# Gemini API -----------------------------------------------------------------------

def get_response(user_input):
    if gemini_enabled:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            return response.text
        except Exception as e:
            return f"(Mode)\n\n{local_chatbot(user_input)}"
    else:
        return f"(Mode)\n\n{local_chatbot(user_input)}"



# Streamlit UI-----------------------------------------------------------------------------------------

st.title("💬 Gemini Chatbot")

if gemini_enabled:
    st.success("Gemini API enabled")
else:
    st.warning("Gemini chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

user_input = st.chat_input("Ask something...")

if user_input:
    # display user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append(("user", user_input))

    # chatbot response
    bot_reply = get_response(user_input)
    st.chat_message("assistant").write(bot_reply)
    st.session_state.messages.append(("assistant", bot_reply))


st.markdown("---")
st.caption("Developed by Arun Sajwan | AICTE Electric Vehicle Project")
