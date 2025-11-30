import streamlit as st
import plotly.express as px
import pandas as pd


st.title("Churn Dashboard")
st.write("Visualize churn patterns and customer insights across multiple industries.")

st.markdown("---")

# ============= TELECOM INDUSTRY =============
st.header("Telecom Industry")

col1, col2 = st.columns(2)

with col1:
    telecom_data = pd.DataFrame({
        "Customer_Segment": ["Prepaid", "Postpaid", "Corporate"],
        "Churn_Rate": [25, 15, 8]
    })
    fig1 = px.bar(
        telecom_data, x="Customer_Segment", y="Churn_Rate",
        color="Customer_Segment", title="Churn Rate by Segment"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    monthly_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Churn_Count": [120, 100, 90, 110, 105]
    })
    fig2 = px.line(
        monthly_data, x="Month", y="Churn_Count",
        markers=True, title="Monthly Churn Trend"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ============= FINANCE INDUSTRY =============
st.header("Finance Industry")

col3, col4 = st.columns(2)

with col3:
    finance_data = pd.DataFrame({
        "Product": ["Credit Card", "Loans", "Insurance"],
        "Churn_Rate": [18, 22, 12]
    })
    fig3 = px.pie(
        finance_data, names="Product", values="Churn_Rate",
        title="Churn Distribution by Product"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    age_data = pd.DataFrame({
        "Age_Group": ["18-25", "26-35", "36-50", "51+"],
        "Churn_Rate": [25, 20, 15, 10]
    })
    fig4 = px.bar(
        age_data, x="Age_Group", y="Churn_Rate",
        title="Churn Rate by Age Group", color="Age_Group"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============= PUBLISHING INDUSTRY =============
st.header("Publishing Industry")

col5, col6 = st.columns(2)

with col5:
    pub_data = pd.DataFrame({
        "Subscription_Type": ["Monthly", "Quarterly", "Yearly"],
        "Churn_Rate": [30, 18, 10]
    })
    fig5 = px.bar(
        pub_data, x="Subscription_Type", y="Churn_Rate",
        color="Subscription_Type",
        title="Churn by Subscription Type"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    device_data = pd.DataFrame({
        "Device": ["Mobile", "Tablet", "Desktop"],
        "Churn_Rate": [28, 22, 18]
    })
    fig6 = px.pie(
        device_data, names="Device", values="Churn_Rate",
        title="Churn Distribution by Device"
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ============= SAAS INDUSTRY =============
st.header("SaaS Industry")

col7, col8 = st.columns(2)

with col7:
    saas_data = pd.DataFrame({
        "Customer_Tier": ["Free", "Standard", "Enterprise"],
        "Churn_Rate": [35, 18, 5]
    })
    fig7 = px.bar(
        saas_data, x="Customer_Tier", y="Churn_Rate",
        color="Customer_Tier",
        title="Churn by Customer Tier"
    )
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    region_data = pd.DataFrame({
        "Region": ["North America", "Europe", "Asia", "Others"],
        "Churn_Rate": [15, 20, 12, 10]
    })
    fig8 = px.line(
        region_data, x="Region", y="Churn_Rate",
        markers=True, title="Regional Churn Insights"
    )
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")
