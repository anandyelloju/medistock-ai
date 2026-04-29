import streamlit as st
import pandas as pd
from src.data.database_manager import DatabaseManager

st.set_page_config(page_title="Analytics", layout="wide", page_icon="📈")

st.title("📈 Analytics & Reports")
st.markdown("*System performance and decision history*")

db = DatabaseManager()

# Get metrics
success_rate = db.get_success_rate()

st.subheader("System Performance")
col1, col2, col3 = st.columns(3)
col1.metric("AI Accuracy", f"{success_rate:.1f}%", delta="Adaptive")
col2.metric("Decision Quality", "Learning...", delta="In Progress")
col3.metric("System Status", "Active", delta="Operational")

st.divider()

# Recent Actions Log
st.subheader("Recent Actions Log")
try:
    recent_logs = db.get_action_logs(limit=20)
    if not recent_logs.empty:
        # Format for display
        display_df = recent_logs[['medicine_name', 'action_type', 'status', 'quantity', 'timestamp']].copy()
        display_df.columns = ['Medicine', 'Action Type', 'Status', 'Quantity', 'Timestamp']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No action logs yet.")
except Exception as e:
    st.error(f"Error loading action logs: {e}")

st.divider()

# Decision History
st.subheader("Reorder Decision History")
try:
    decisions = db.get_pending_evaluations()
    if not decisions.empty:
        display_df = decisions[['medicine_name', 'stockout_days', 'reorder_qty', 'timestamp']].copy()
        display_df.columns = ['Medicine', 'Stockout Days', 'Reorder Qty', 'Date']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No pending decisions.")
except Exception as e:
    st.error(f"Error loading decisions: {e}")

st.divider()

# Performance Evaluations
st.subheader("Performance Evaluations")
try:
    perf_logs = db.get_all_performance_logs(limit=20)
    if not perf_logs.empty:
        display_df = perf_logs[['medicine_name', 'score', 'comment', 'eval_timestamp']].copy()
        display_df.columns = ['Medicine', 'Score', 'Comment', 'Evaluated At']
        
        # Add color coding
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        with col2:
            score_stats = perf_logs['score'].value_counts()
            st.write("**Score Distribution**")
            for score, count in score_stats.items():
                st.write(f"{score}: {count}")
    else:
        st.info("No performance evaluations yet.")
except Exception as e:
    st.error(f"Error loading performance logs: {e}")
