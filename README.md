# 🔋 Battery Health & Range Prediction - Streamlit App

An interactive web application built with **Streamlit** to predict the **State of Health (SOH)** and **driving range** of Electric Vehicle (EV) batteries using machine learning models.

## 🎯 Features

- **Battery Health Prediction (SOH)** — Estimates battery capacity based on resistance and temperature data
- **Driving Range Estimation** — Calculates EV range considering SOH, efficiency, terrain, temperature, and vehicle weight
- **Weight Impact Analysis** — Shows how vehicle weight affects driving range
- **Health Status Indicator** — Visual feedback on battery condition (Excellent/Good/Fair/Poor)
- **Interactive Parameters** — User-friendly inputs for custom predictions

## 📊 Input Parameters

### Battery Parameters
- **Ambient Temperature** (-10°C to 60°C) — Operating environment temperature
- **Re (Electrolyte Resistance)** (0 to 1 Ω) — Battery internal resistance
- **Rct (Charge Transfer Resistance)** (0 to 1 Ω) — Impedance of charge transfer

### Trip Parameters
- **Efficiency** (3 to 8 km/kWh) — Vehicle energy consumption rate
- **Terrain Factor** (0.7 to 1.0) — 1.0 = flat, 0.7 = hilly
- **Vehicle Weight** (1000 to 3000 kg) — Total vehicle mass

## 🔑 API Keys / Gemini setup

The chatbot uses Google Generative (Gemini) when a valid API key is provided. You can supply the key via:

- Streamlit secrets (recommended): add `GOOGLE_API_KEY` or `GEMINI_API_KEY` in `.streamlit/secrets.toml`  
- Environment variable: set `GEMINI_API_KEY` or `GOOGLE_API_KEY`  
- Session input in the app (temporary)

Example `.env` (do NOT commit this file):
```
GEMINI_API_KEY=your_key_here
# or
GOOGLE_API_KEY=your_key_here
```
## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation

Install dependencies:
```bash
pip install streamlit scikit-learn joblib pandas numpy
```
SOH_model.joblib
soh_imputer.joblib
range_model.joblib
range_imputer.joblib
```

### Running the App

```bash
streamlit run chatbot.py
```

## 📈 Output Metrics

### Primary Outputs
- **Battery Health (SOH)** — Percentage of battery capacity remaining
- **Battery Capacity** — Predicted capacity in Ah
- **Estimated Range** — Driving range in km

### Secondary Outputs
- **Battery Health Status** — Condition assessment with recommendations
- **Environmental Metrics** — Temperature and resistance values
- **Weight Impact Analysis** — Percentage range loss due to vehicle weight
- **Range Breakdown** — Optimal vs worst-case scenario ranges

## 🔧 Model Architecture

### SOH Model
- **Type** — Random Forest Regressor (200 estimators)
- **Features** — [ambient_temperature, Re, Rct]
- **Target** — Battery Capacity (Ah)
- **Preprocessing** — SimpleImputer (mean strategy)

### Range Model
- **Type** — Random Forest Regressor (200 estimators)
- **Features** — [SOH, efficiency_km_per_kWh, ambient_temp, terrain_factor, vehicle_weight_kg]
- **Target** — Driving Range (km)
- **Preprocessing** — SimpleImputer (mean strategy)

## 📊 Health Status Thresholds

| SOH Range | Status | Recommendation |
|-----------|--------|-----------------|
| ≥ 80% | ✅ Excellent | Battery in great condition |
| 60-79% | ⚠️ Good | Battery performing well |
| 40-59% | ⚠️ Fair | Consider maintenance soon |
| < 40% | ❌ Poor | Battery replacement recommended |

## 🧮 Calculations

### State of Health (SOH)
```
SOH (%) = (Predicted Capacity / Nominal Capacity) × 100
Nominal Capacity = 1.1 Ah
```

### Weight Impact
```
Weight Factor = Vehicle Weight / Reference Weight (1500 kg)
Range Loss (%) = ((Predicted Range - Range Without Weight) / Range Without Weight) × 100
```

### Range Scenarios
```
Optimal Range = Predicted Range (ideal conditions)
Worst Case Range = Predicted Range × 0.8 (harsh conditions)
```

## 📁 Project Structure

```
AICTE electric vehical/
├── chatbot.py                 # Streamlit app (main file)
├── BatteryHealth.ipynb        # Model training notebook
├── SOH_model.joblib           # Trained SOH model
├── soh_imputer.joblib         # SOH data imputer
├── range_model.joblib         # Trained range model
├── range_imputer.joblib       # Range data imputer
├── battery-5.csv              # Sample battery data
├── metadata(1).csv            # Battery metadata
└── README.md                  # This file
```

## 💡 How to Use

1. **Enter Parameters** — Input battery characteristics and trip conditions
2. **Click Predict Button** — Process inputs through ML models
3. **View Results** — Get SOH percentage, capacity, and range estimates
4. **Analyze Impact** — See how weight and conditions affect range
5. **Make Decisions** — Use insights for battery management

## 📝 Example Scenario

**Initial Inputs:**
- Ambient Temp: 30°C
- Re: 0.055 Ω
- Rct: 0.20 Ω
- Efficiency: 5.7 km/kWh
- Terrain: 0.9 (slightly hilly)
- Vehicle Weight: 1500 kg

**Output:**
- SOH: 95.45%
- Capacity: 1.05 Ah
- Range: 190 km
- Status: ✅ Excellent

## 🔬 Model Training

Models were trained using:
- **Algorithm** — Random Forest Regression
- **Training Data** — Battery sensor data and metadata
- **Test Split** — 80-20 (training-testing)
- **Hyperparameters** — 200 estimators, random_state=42

For retraining, see `BatteryHealth.ipynb`


## 👨‍💻 Author

**Arun Sajwan**  
-Guru Ram Dass Institute of Management and Technology
⚡ AICTE AI/ML in Electric Vehicles 

---

**Last Updated:** November 14, 2025  

