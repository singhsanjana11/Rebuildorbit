import streamlit as st
import joblib
import pandas as pd
#Login Check
if not st.session_state.get("logged_in", False):
    st.warning("Please login from the Home page to access this page.")
    st.stop()

st.title("Batch Churn Prediction")

#Model Loading
MODEL_PATHS = {
    "Subscription Based Industry": "subscription_churn_pipeline.pkl",
    "Telcommunication Industry": "telco_churn_pipeline.pkl",
    "Customer Based Industry": "ecommerce_churn_pipeline.pkl",
    "Banking Industry": "banking_churn_pipeline.pkl",
}

#Feature List
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
#Expected Feature List
EXPECTED_FEATURES = {
    "Banking Industry": [
        "creditscore", "geography", "gender", "age", "tenure",
        "balance", "numofproducts", "hascrcard", "isactivemember", "estimatedsalary"
    ],
    "Telcommunication Industry": [
        "seniorcitizen", "tenure", "gender", "partner", "dependents",
        "phoneservice", "multiplelines", "internetservice", "onlinesecurity",
        "onlinebackup", "deviceprotection", "techsupport", "streamingtv",
        "streamingmovies", "contract", "paperlessbilling", "paymentmethod",
        "monthlycharges", "totalcharges"
    ],
    "Customer Based Industry": [
        "age", "tenure", "balance", "monthlycharges", "numofproducts"
    ],
    "Subscription Based Industry": [
        "tenure", "monthlycharges", "totalcharges", "numofproducts", "balance"
    ]
}
#Feature Categorization
NUMERIC_FEATURES = {
    "Telcommunication Industry": ["seniorcitizen", "tenure", "monthlycharges", "totalcharges"],
    "Banking Industry": ["creditscore", "age", "tenure", "balance", "numofproducts", "estimatedsalary"],
    "Customer Based Industry": ["age", "tenure", "monthlycharges", "totalcharges"],
    "Subscription Based Industry": [
        "accountage", "monthlycharges", "totalcharges",
        "viewinghoursperweek", "contentdownloadspermonth",
        "userrating", "supportticketspermonth", "watchlistsize"
    ]
}
# Industry Selection
industry = st.selectbox("Select Industry", list(MODEL_PATHS.keys()))
st.subheader("Expected CSV columns")

req_cols = EXPECTED_FEATURES[industry]

st.markdown(
    "Your CSV must contain at least the following columns "
    f"for the selected industry ({industry}):"
)

st.write(req_cols)

st.markdown(
    "_Column names must match exactly (case-sensitive, no extra spaces)._"
)

# Load model
try:
    pipeline = joblib.load(MODEL_PATHS[industry])
    st.success(f"{industry} Model Loaded Successfully")
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

expected_features = FEATURES_IN_MODEL[industry]
st.write(f"Model expects {len(expected_features)} columns.")

# File Upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Standardize column names to lowercase
    df.columns = df.columns.str.lower().str.strip()

    # Fix uppercase user CSV column issue
    required = [c.lower() for c in expected_features]

    missing = [col for col in required if col not in df.columns]

    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    # Subset required columns
    df = df[required]

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Cleaning Numeric FIelds
    for col in NUMERIC_FEATURES[industry]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Force int fields
    for col in ["seniorcitizen", "numofproducts"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df = df.fillna(0)

    # Prediction Button
    if st.button("Predict", use_container_width=True):
        try:
            preds = pipeline.predict(df)

            # Probability (if available)
            probs = None
            if hasattr(pipeline, "predict_proba"):
                prob_values = pipeline.predict_proba(df)
                if prob_values.shape[1] == 2:
                    probs = prob_values[:, 1]

            # Prepare output
            out = df.copy()
            out["Prediction"] = preds



            if probs is not None:
                out["Churn_Probability"] = probs.round(4)

            st.subheader("Prediction Results")
            st.dataframe(out.head())

            prediction_df = out

            st.subheader("Churn Summary")

            total = len(prediction_df)
            churn_count = prediction_df["Prediction"].sum()
            non_churn = total - churn_count
            churn_rate = round((churn_count / total) * 100, 2)

            colA, colB, colC = st.columns(3)
            colA.metric("Total Customers", total)
            colB.metric("Churners", churn_count)
            colC.metric("Churn Rate", f"{churn_rate}%")

            # Chart Visualization
            import matplotlib.pyplot as plt

            col1, col2 = st.columns(2)

            # Pie Chart
            with col1:
                fig1, ax1 = plt.subplots()
                ax1.pie([churn_count, non_churn],
                        labels=["Churn", "Not Churn"],
                        autopct="%1.1f%%")
                st.pyplot(fig1)

            # Bar Chart
            with col2:
                fig2, ax2 = plt.subplots()
                ax2.bar(["Churn", "Not Churn"], [churn_count, non_churn])
                st.pyplot(fig2)

            # Download Final Predictions
            csv = out.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Predictions CSV",
                data=csv,
                file_name="batch_churn_predictions.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Prediction failed: {e}")
