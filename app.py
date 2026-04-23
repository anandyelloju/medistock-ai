import streamlit as st
from src.data_processing import load_data, process_data
from src.decision_engine import evaluate_row
from src.llm_explainer import generate_explanation

df = load_data("data/inventory.csv")
df = process_data(df)

st.title("MediStock AI Dashboard")

for _, row in df.iterrows():
    decisions = evaluate_row(row)

    if decisions:
        explanation = generate_explanation(row, decisions)
        st.write(f"🔍 {explanation}")