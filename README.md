# 🌾 AGRI INTELLIGENCE: National Agri-Price Command Center

## 📘 Project Overview

**AGRI INTELLIGENCE** is a comprehensive machine learning-powered web application and command center designed to forecast the prices of agricultural and horticultural commodities in India. The platform helps farmers, agri-businesses, and policymakers by delivering accurate crop price predictions, supporting data-driven decision-making, and reducing financial risk due to unpredictable market fluctuations.

Developed with a focus on accessibility, modern aesthetics, and real-world utility, this system uses real datasets from [data.gov.in](https://data.gov.in), including historical crop prices, rainfall data, and wholesale price index (WPI) statistics. Using this multi-faceted data, a **Decision Tree Regression** model is trained to predict the prices of various crops for up to **12 future months**.

---

## 🎯 Command Center Highlights
Our latest update completely transforms the platform into a high-tech **Command Center**:
- 🎨 **Premium UI/UX Enhancements:** A completely refreshed visual aesthetic featuring distinct glowing elements, dynamic hover states, responsive dashboards, and fully interactive footers.
- 📡 **HTML5 Geolocation (AI Farmer):** The AI Farmer Advisor now utilizes exact satellite-based GPS tracking via the HTML5 Geolocation API, officially replacing the older, inaccurate IP-based lookup system. The platform will automatically reverse-geocode your exact village, district, and State for localized weather predictions and precise ML crop advice.
- 📈 **Rebranded Identity:** We fully transitioned the platform identity from "Apna Anaaj" to **AGRI INTELLIGENCE** to reflect the modern scope of the tooling.

---

## 🧠 Our Approach

### 1. Data Collection & Curation
We use authenticated datasets from [data.gov.in](https://data.gov.in):
- Historical monthly crop price data for 23 key commodities.
- Rainfall data which influences crop yield.
- Wholesale Price Index (WPI) values that reflect market trends.

### 2. Feature Engineering
For each crop entry, we generate features like:
- Month index (seasonality factor)
- Average rainfall for the region
- Corresponding WPI for that commodity type
- Historical moving average of crop price trends

### 3. Model Training
We use **Decision Tree Regressors**, a supervised learning technique from **scikit-learn**. The model is trained on preprocessed data, achieving accuracy between **93% and 95%**.

### 4. Visualization & Forecasting
All forecast results are presented through dynamic JavaScript visualizations (Chart.js):
- 📈 Dynamic line graphs
- 📉 Tabular data comparisons
- 🔼 Top Gainers & 🔽 Top Losers based on projected changes

---

## 💻 Technology Stack

| Component         | Technology Used                             |
|------------------|---------------------------------------------|
| Language          | Python 3                                    |
| Backend           | Flask Web Framework                         |
| Machine Learning  | scikit-learn (DecisionTreeRegressor)        |
| Frontend          | HTML, CSS, JavaScript                       |
| Charts            | Chart.js                                    |

---

## 🚀 Features

- 📌 23 Crops Supported: Cereals, fruits, vegetables, spices, etc.
- 📈 12-Month Custom Prediction Window
- 🔍 Top Gainers & Losers Tracker
- 📉 Side-by-side Historical vs Predicted Graphs
- 🌦️ Deep Weather/Location Integration via Open-Meteo & OpenStreetMap
- 🖥️ Modern Command Center UI with AGRI INTELLIGENCE branding

---

## 🔧 How to Run Locally

```bash
# Step 1: Clone the repository
git clone https://github.com/adavesh19/AgriIntelligence.git
cd AgriIntelligence

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start the Flask server
python app.py

# Step 4: Open in your browser
# Go to: http://127.0.0.1:5000
```

----------

### 📷 Command Center Screenshots
*A glimpse into the AGRI INTELLIGENCE dashboards:*

**1. National Agri-Price Command Center Dashboard:**
<img src="static/screenshot-cmd2.png" width="800" alt="Main Dashboard"/>

**2. 23 Commodities Real-time Tracking & Top Gainers:**
<img src="static/screenshot-cmd3.png" width="800" alt="All Crops Listing"/>

**3. Commodity Details & Interactive AI Forecast Charts:**
<img src="static/screenshot-cmd1.png" width="800" alt="Commodity Charts"/>

**4. AI Farming Advisor with exact HTML5 Geolocation Tracking:**
<img src="static/screenshot-cmd4.png" width="800" alt="AI Farmer Advisor"/>

----------

### 📁 Directory Structure
```
AgriIntelligence/
├── app.py               # Flask backend logic
├── crops.py             # Data parser & prediction ML logic
├── templates/           # HTML templates (index, commodity, ai_farmer)
├── static/              # CSS, JS, and image assets (AGRI INTELLIGENCE logo)
├── requirements.txt     # Python dependencies
├── README.md            # Command Center Documentation
```

-----------

### ✨ Mission Statement
**AGRI INTELLIGENCE** is built to bridge the gap between advanced predictive models and localized farming insights, enhancing rural economic resilience through modern tech infrastructure.
