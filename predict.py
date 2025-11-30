import streamlit as st
import joblib
import pandas as pd
import numpy as np

#Check Login
if not st.session_state.get("logged_in", False):
    st.warning("Please login on Home page to access this page.")
    st.stop()

st.title("Single Churn Prediction")

# Select and Load Model
MODEL_PATHS = {
    "Subscription Based Industry": "subscription_churn_pipeline.pkl",
    "Telcommunication Industry": "telco_churn_pipeline.pkl",
    "Customer Based Industry": "ecommerce_churn_pipeline.pkl",
    "Banking industry": "banking_churn_pipeline.pkl",
}

# Feature List
FEATURES_IN_MODEL = {
    "Subscription Based Industry": [
        "accountage", "monthlycharges", "totalcharges",
        "subscriptiontype", "paymentmethod", "paperlessbilling",
        "contenttype", "multideviceaccess", "deviceregistered",
        "viewinghoursperweek", "averageviewingduration",
        "contentdownloadspermonth", "genrepreference",
        "userrating", "supportticketspermonth", "gender",
        "watchlistsize", "parentalcontrol", "subtitlesenabled",
    ],
    "Telcommunication Industry": [
        "seniorcitizen", "tenure", "gender",
        "partner", "dependents",
        "phoneservice", "multiplelines",
        "internetservice", "onlinesecurity",
        "onlinebackup", "deviceprotection",
        "techsupport", "streamingtv",
        "streamingmovies", "contract",
        "paperlessbilling", "paymentmethod",
        "monthlycharges", "totalcharges",
    ],
    "Customer Based Industry": [
        "age", "gender", "tenure",
        "monthlycharges", "contracttype",
        "internetservice", "totalcharges",
        "techsupport",
    ],
    "Banking Industry": [
        "creditscore", "geography", "gender",
        "age", "tenure", "balance",
        "numofproducts", "hascrcard",
        "isactivemember", "estimatedsalary",
    ],
}

# Option/Categories
OPTIONS = {
    "gender": ["Male", "Female"],
    "geography": ["France", "Germany", "Spain"],
    "contracttype": ["Month-to-Month", "One-Year", "Two-Year"],
    "contract": ["Month-to-Month", "One-Year", "Two-Year"],
    "internetservice": ["DSL", "Fiber optic", "No"],
    "paperlessbilling": ["Yes", "No"],
    "paymentmethod": [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)",
        "Credit Card", "Debit Card", "Paypal",
    ],
    "techsupport": ["Yes", "No", "No internet service"],
    "multideviceaccess": ["Yes", "No"],
    "hascrcard": ["Yes", "No"],
    "isactivemember": ["Yes", "No"],
    "subscriptiontype": ["Basic", "Premium", "Gold"],
    "subtitlesenabled": ["Yes", "No"],
    "parentalcontrol": ["Yes", "No"],
    "genrepreference": [
        "Comedy", "Mystery", "Thriller", "Sci-Fi",
        "Romance", "Action", "Fantasy", "Drama",
    ],
    "dependents": ["Yes", "No"],
    "partner": ["Yes", "No"],
    "phoneservice": ["Yes", "No"],
    "multiplelines": ["Yes", "No"],
    "onlinesecurity": ["Yes", "No"],
    "onlinebackup": ["Yes", "No"],
    "deviceprotection": ["Yes", "No"],
    "streamingtv": ["Yes", "No"],
    "streamingmovies": ["Yes", "No"],
}

# Numeric Features
NUMERIC_FEATURES = {
    "Telcommunication Industry": ["seniorcitizen", "tenure", "monthlycharges", "totalcharges"],
    "Banking Industry": ["creditscore", "age", "tenure", "balance", "numofproducts", "estimatedsalary"],
    "Customer Based Industry": ["age", "tenure", "monthlycharges", "totalcharges"],
    "Subscription Based Industry": ["accountage", "monthlycharges", "totalcharges", "viewinghoursperweek",
                     "contentdownloadspermonth", "userrating", "supportticketspermonth", "watchlistsize"]
}

# Select Industry
industry = st.selectbox("Select Industry", list(MODEL_PATHS.keys()))

try:
    pipeline = joblib.load(MODEL_PATHS[industry])
    st.success(f"Model loaded for {industry}")
except Exception as e:
    st.error(f"Could not load model for {industry}: {e}")
    st.stop()

features = FEATURES_IN_MODEL[industry]
st.write(f"{len(features)} features expected. Fill form below.")

# Accepting input
input_values = {}
cols = st.columns(2)

for i, feat in enumerate(features):
    col = cols[i % 2]
    label = feat.replace("_", " ").title()
    widget_key = f"{industry}_{feat}_{i}"

    if feat in OPTIONS:
        input_values[feat] = col.selectbox(label, OPTIONS[feat], key=widget_key)
    elif feat in NUMERIC_FEATURES.get(industry, []):
        input_values[feat] = col.number_input(label, min_value=0.0, value=00.0, key=widget_key)
    else:
        input_values[feat] = col.number_input(label, min_value=0.0, value=00.0, key=widget_key)

# Final SIngle Prediction
if st.button("Predict", use_container_width=True):
    try:
        # Create DataFrame with exact column order
        df = pd.DataFrame([input_values], columns=features)

        # Convert numeric columns only
        numeric_cols = NUMERIC_FEATURES.get(industry, [])
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(50.0)

        # Handle seniorcitizen and numofproducts as integers
        for col in ['seniorcitizen', 'numofproducts', "hascrcard", "isactivemember"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # Final cleanup
        df = df.fillna(0.0)


        # Make prediction
        pred = pipeline.predict(df)[0]

        # Get probability if available
        prob_churn = "N/A"
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba(df)[0]
            if len(proba) == 2:
                prob_churn = f"{proba[1]:.1%}"
            else:
                prob_churn = f"{max(proba):.1%}"

        # Display results
        col1, col2 = st.columns(2)
        col1.metric("Prediction", "Will Churn" if pred == 1 else "Will Stay")
        col2.metric("Churn Probability", prob_churn)

    except Exception as e:
        st.error(f"Prediction error: {str(e)}")

