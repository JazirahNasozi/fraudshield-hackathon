import streamlit as st
import pandas as pd

st.title("📱 FraudShield - Mobile Money Fraud Detection")

st.write("This is a simple demo app for detecting suspicious mobile money transactions.")

# Upload CSV
uploaded_file = st.file_uploader("Upload a transaction file (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Transactions", df.head())

    # Fake simple rule: if amount > 1,000,000 flag as suspicious
    df["Fraud_Flag"] = df["Amount"].apply(lambda x: "🚨 Suspicious" if x > 1000000 else "✅ Safe")
    
    st.write("### Results", df)
    st.success("Fraud detection completed!")
