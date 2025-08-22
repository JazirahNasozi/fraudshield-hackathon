import streamlit as st
import pandas as pd

st.set_page_config(page_title="FraudShield AI", page_icon="🛡️")

st.title("🛡️ FraudShield AI - Mobile Money Fraud Detection (Prototype)")
st.write("Upload transaction data and let the system flag suspicious activity.")

# File uploader
uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

if uploaded_file:
    # Load file
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Uploaded Transactions")
    st.dataframe(df.head())

    # --- Simple fraud rule for demo ---
    # Let's say fraud = transactions > 1,000,000
    st.subheader("🚨 Flagged Suspicious Transactions")
    fraud = df[df['amount'] > 1000000] if 'amount' in df.columns else pd.DataFrame()

    if not fraud.empty:
        st.error("⚠️ Suspicious transactions detected!")
        st.dataframe(fraud)
    else:
        st.success("✅ No suspicious transactions found (based on demo rule).")

st.sidebar.header("About FraudShield")
st.sidebar.write("""
FraudShield AI is a prototype app to help detect mobile money fraud.
Future versions will use **Machine Learning (AI)** for more accuracy.
""")

