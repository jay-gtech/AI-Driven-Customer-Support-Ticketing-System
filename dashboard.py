import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI Ticketing Dashboard", layout="wide")

# -----------------------------
#  Simple Authentication
# -----------------------------
def login():
    st.title(" Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# -----------------------------
#  Sidebar Analytics Panel
# -----------------------------
st.sidebar.title(" System Analytics")

if "history" not in st.session_state:
    st.session_state["history"] = []

history_df = pd.DataFrame(st.session_state["history"])

if not history_df.empty:
    st.sidebar.metric("Total Predictions", len(history_df))
    st.sidebar.metric("Avg Risk %", f"{history_df['risk'].mean():.2f}")
    st.sidebar.metric("Escalations Triggered",
                      history_df["flag"].sum())

# -----------------------------
# 🖥 Main Dashboard
# -----------------------------
st.title(" AI-Driven Customer Support Ticketing System")

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject")
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    customer_plan = st.selectbox("Customer Plan", ["Free", "Pro", "Enterprise"])
    sla_breached = st.selectbox("SLA Breached", [0, 1])

with col2:
    description = st.text_area("Description")

if st.button("Predict Ticket Risk"):

    payload = {
        "subject": subject,
        "description": description,
        "priority": priority,
        "customer_plan": customer_plan,
        "sla_breached": sla_breached
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict-ticket",
            json=payload
        )

        result = response.json()

        risk_percent = result["escalation_probability"] * 100

        # Store history
        st.session_state["history"].append({
            "category": result["predicted_category"],
            "sentiment": result["predicted_support_sentiment"],
            "risk": risk_percent,
            "flag": result["escalation_flag"]
        })

        st.markdown("---")
        st.subheader(" Prediction Results")

        colA, colB = st.columns(2)

        with colA:
            st.metric("Category", result["predicted_category"])
            st.metric("Sentiment", result["predicted_support_sentiment"])

        with colB:
            # Risk Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_percent,
                title={'text': "Escalation Risk %"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "red" if risk_percent > 70 else "orange"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgreen"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightcoral"}
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

        if result["escalation_flag"] == 1:
            st.error(" Escalation Required")
        else:
            st.success(" No Escalation Needed")

    except:
        st.error("API not running. Start FastAPI first.")
