import streamlit as st
import requests

st.title("Optimisation du ROI")

with st.sidebar:
    st.header("Configuration Budgétaire")
    tv = st.slider("TV (M€)", 0.0, 500.0, 150.0)
    radio = st.slider("Radio (M€)", 0.0, 100.0, 30.0)
    social = st.slider("Social Media (M€)", 0.0, 100.0, 20.0)
    influencer = st.selectbox("Type d'Influenceur", ["Mega", "Macro", "Micro", "Nano"])

if st.button("Estimer les Ventes"):
    payload = {
        "TV": tv,
        "Radio": radio,
        "Social_Media": social,
        "Influencer": influencer
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            prediction = response.json()["predicted_sales_millions"]
            st.success(f"📈 Ventes estimées : {prediction} millions d'euros")
            
            total_budget = tv + radio + social
            roi = (prediction / total_budget) if total_budget > 0 else 0
            st.metric("ROI Estimé", f"{roi:.2f}")
        else:
            st.error("Erreur lors de la communication avec l'API.")
            
    except Exception as e:
        st.error(f"Impossible de joindre l'API : {e}")