# 🔋 Battery Health & Range Prediction using Machine Learning

## 🧠 Project Overview
This project predicts the **State of Health (SOH)** of an electric vehicle’s battery and estimates the **driving range** based on that health using **Machine Learning (ML)**.

It combines **sensor data**, **battery test metadata**, and **regression modeling** to create a predictive pipeline that can:
- Estimate the **remaining capacity** of a battery (in Ah)
- Calculate **battery SOH (%)**
- Predict the **expected driving range (km)** for given trip conditions

---

## 🎯 Problem Statement
Electric vehicle batteries degrade over time, leading to reduced performance and driving range.  
This project aims to:
1. Analyze battery data (voltage, current, temperature)
2. Train an ML model to predict **battery health**
3. Extend the prediction to estimate the **vehicle range** under real-world conditions

---

## ⚙️ Dataset Description
The project uses the following datasets:

| File | Description |
|------|--------------|
| **Battery-5.csv** | Time-series data of voltage, current, temperature, and load measurements during charge/discharge cycles |
| **metadata (1).csv** | Metadata for multiple battery tests (includes ambient temperature, capacity, internal resistance, etc.) |

Data source: *NASA Battery Dataset / CALCE Battery Research Data / keggle battery Datasets.*

---

## 🧩 Machine Learning Pipeline

### 1️⃣ Battery Health Prediction (SOH)
- **Input features:** Ambient temperature, internal resistance (Re, Rct)
- **Model used:** Random Forest Regressor
- **Output:** Predicted capacity (Ah) → converted to SOH (%)

### 2️⃣ Range Estimation
- **Input features:** SOH, efficiency (km/kWh), ambient temperature, terrain factor
- **Model used:** Random Forest Regressor
- **Output:** Estimated driving range (km)

---

## 🧠 Technologies Used
- Python 3.10+
- Jupyter Notebook
- pandas, numpy
- scikit-learn
- matplotlib / seaborn (for visualization)

---

## 🚀 How to Run the Project

### Option 1: Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/BatteryHealthPrediction.git
   cd BatteryHealthPrediction
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Open the Jupyter Notebook:
   ```bash
   jupyter notebook BatteryHealth.ipynb
   ```
4. Run all cells to train the models and view predictions.

### Option 2: Run on Google Colab
- Upload both `Battery-5.csv` and `metadata (1).csv`
- Open `BatteryHealth.ipynb`
- Run all cells sequentially.

---

## 📊 Results Summary

| Metric | Battery Health Model | Range Model |
|---------|----------------------|--------------|
| MAE | 0.25 Ah | 22.1 km |
| R² Score | 0.46 | 0.64 |

**Predicted for Battery-5:**
- Capacity: **≈ 0.91 Ah**
- SOH: **≈ 82.6%**
- Estimated Range: **≈ 174 km**

---

## 📁 Repository Structure
```
BatteryHealthPrediction/
│
├── BatteryHealth.ipynb            # Main Jupyter Notebook
├── Battery-5.csv                  # Battery test data
├── metadata (1).csv               # Metadata with capacity and test info
└── README.md                      # Project documentation
```
---
## ✨ Author
**Arun Sajwan**  
B.Tech in Computer Science 
[GitHub](https://github.com/)
