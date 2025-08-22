import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Set browser tab title and icon
# -----------------------
st.set_page_config(
    page_title="FraudShield 💳",
    page_icon="💳",
    layout="wide"
)

# -----------------------
# Header
# -----------------------
st.markdown("<h1 style='color:#1F618D; font-family:Courier New; text-align:center;'>💳 FraudShield</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#566573; font-size:18px; text-align:center;'>AI-powered system to detect & prevent financial fraud in real time 🚀</p>", unsafe_allow_html=True)

# -----------------------
# Sidebar instructions & filters
# -----------------------
st.sidebar.header("ℹ️ How to use FraudShield")
st.sidebar.markdown("""
1. Upload a CSV file with `TransactionID` and `Amount`.  
2. Transactions will be scored for fraud risk.  
3. Review the fraud analysis table and charts.  
4. Download the results using the button below.  
""")

st.sidebar.header("🔍 Filters")
show_only_high_risk = st.sidebar.checkbox("Show only high-risk transactions")
min_amount = st.sidebar.number_input("Minimum Amount", min_value=0, value=0, step=1000)
max_amount = st.sidebar.number_input("Maximum Amount", min_value=0, value=10000000, step=1000)

# -----------------------
# File uploader
# -----------------------
uploaded_file = st.file_uploader("📂 Upload your transactions CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # -----------------------
    # AI-based fraud scoring simulation
    # -----------------------
    def fraud_score(amount):
        if amount > 1000000:
            return "⚠️ High Risk"
        elif amount >= 500000:
            return "⚠️ Medium Risk"
        else:
            return "✅ Low Risk"
    
    data["Fraud Risk"] = data["Amount"].apply(fraud_score)

    # Apply filters
    filtered_data = data[(data["Amount"] >= min_amount) & (data["Amount"] <= max_amount)]
    if show_only_high_risk:
        filtered_data = filtered_data[filtered_data["Fraud Risk"] == "⚠️ High Risk"]

    # -----------------------
    # Summary statistics panel
    # -----------------------
    st.markdown("### 📊 Summary Statistics")
    total_transactions = len(filtered_data)
    high_risk_count = (filtered_data["Fraud Risk"] == "⚠️ High Risk").sum()
    medium_risk_count = (filtered_data["Fraud Risk"] == "⚠️ Medium Risk").sum()
    low_risk_count = (filtered_data["Fraud Risk"] == "✅ Low Risk").sum()
    high_risk_pct = (high_risk_count / total_transactions * 100) if total_transactions > 0 else 0

    st.markdown(f"""
    🧾 **Total Transactions:** {total_transactions}  
    🔴 **High Risk:** {high_risk_count}  
    🟠 **Medium Risk:** {medium_risk_count}  
    🟢 **Low Risk:** {low_risk_count}  
    🚨 **High Risk %:** {high_risk_pct:.2f}%
    """)

    # Highlight risk levels
    def highlight_risk(val):
        color = 'red' if val == '⚠️ High Risk' else 'orange' if val == '⚠️ Medium Risk' else 'green'
        return f'color: {color}; font-weight:bold'
    
    st.markdown("### 📊 Filtered Transaction Data with AI Risk Score")
    st.dataframe(filtered_data.style.applymap(highlight_risk, subset=['Fraud Risk']))

    # -----------------------
    # Charts side by side
    # -----------------------
    st.markdown("### 📈 Fraud Risk Distribution")
    summary = filtered_data["Fraud Risk"].value_counts().rename_axis('Risk').reset_index(name='Count')

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(summary.set_index('Risk'))

    with col2:
        fig, ax = plt.subplots()
        colors_map = {'✅ Low Risk':'green','⚠️ Medium Risk':'orange','⚠️ High Risk':'red'}
        ax.pie(summary["Count"], labels=summary["Risk"], autopct='%1.1f%%', colors=[colors_map[i] for i in summary["Risk"]])
        ax.set_title("Transaction Risk Distribution")
        st.pyplot(fig)

    # -----------------------
    # Download
    # -----------------------
    st.markdown("### 💾 Download Filtered Results")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='ai_fraud_analysis_results.csv',
        mime='text/csv'
    )




