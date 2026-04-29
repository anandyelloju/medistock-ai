import streamlit as st
import pandas as pd
from src.data.database_manager import DatabaseManager
from src.core.data_processing import process_data
from src.core.decision_engine import evaluate_row

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="📊")

# Initialize Database Manager
db = DatabaseManager()
df_raw = db.get_all_inventory()
df = process_data(df_raw)

# Get automation setting from session
automation_on = st.session_state.get('automation_mode', False)

st.title("📊 Dashboard Overview")
st.markdown("*Key Performance Indicators & Inventory Health*")

# --- CRITICAL ALERTS BANNER ---
critical_count = len(df[df['Stock_Quantity'] < df['Min_Stock_Level']])
expiry_count = len(df[(df['Expiry_Date'] - pd.to_datetime('today')).dt.days < 30])

if critical_count > 0 or expiry_count > 0:
    st.markdown(f"""
        <div class="critical-banner">
            <b>🚨 ACTION REQUIRED:</b> {critical_count} items are below critical stock levels and {expiry_count} items are expiring within 30 days.
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="info-banner">
            <b>✅ ALL CLEAR:</b> Inventory levels are healthy and no immediate expiry risks detected.
        </div>
    """, unsafe_allow_html=True)

# Refresh button
if st.button("🔄 Refresh Data", type="secondary", use_container_width=False):
    st.rerun()

st.divider()

# KPI Calculations
total_value = (df['Stock_Quantity'] * df['Cost_Per_Unit']).sum()
df['execution_context'] = df.apply(lambda row: evaluate_row(row, automation_enabled=automation_on), axis=1)
df['alerts'] = df['execution_context'].apply(lambda ctx: ctx.get_all_alerts())

expiry_risk_value = df[df['alerts'].apply(lambda x: any(a['priority'] == 1 for a in x))].apply(
    lambda r: r['Stock_Quantity'] * r['Cost_Per_Unit'], axis=1
).sum()

pending_reorders = df['alerts'].apply(lambda x: any(a['priority'] == 2 for a in x)).sum()

# Display KPI Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Inventory Value", f"${total_value:,.2f}")
col2.metric("Expiry Risk Value", f"${expiry_risk_value:,.2f}", delta="-Critical", delta_color="inverse")
col3.metric("Pending Reorders", pending_reorders)
col4.metric("Critical Items", critical_count)

st.divider()

# Inventory Summary Table
st.subheader("Inventory Summary")
summary_df = df[['Item_Name', 'Category', 'Stock_Quantity', 'Min_Stock_Level', 'Days_Until_Stockout', 'Supplier_Name']].copy()
summary_df['Status'] = summary_df.apply(
    lambda row: '🔴 Critical' if row['Stock_Quantity'] < row['Min_Stock_Level'] else '🟡 Low' if row['Days_Until_Stockout'] < 30 else '🟢 Good',
    axis=1
)
st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.divider()

# Distribution Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Items by Category")
    category_counts = df['Category'].value_counts()
    st.bar_chart(category_counts)

with col2:
    st.subheader("Stock Health Distribution")
    health_data = {
        'Critical': critical_count,
        'Expiring Soon': expiry_count,
        'Healthy': len(df) - critical_count - expiry_count
    }
    st.bar_chart(pd.Series(health_data))
