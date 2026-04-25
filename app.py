import streamlit as st
from src.database_manager import DatabaseManager
from src.data_processing import process_data
from src.decision_engine import evaluate_row
from src.llm_explainer import generate_explanation

# Initialize Database Manager
db = DatabaseManager()

# Pull data from SQLite
df = db.get_all_inventory()

# Process data to calculate derived metrics (Days_To_Expiry, etc.)
# This ensures the agent logic remains compatible
df = process_data(df)

# Sidebar Configuration
st.sidebar.header("🛠️ Settings")
show_critical_only = st.sidebar.checkbox("Show Only Critical Alerts", value=False)

st.title("💊 MediStock AI Dashboard")

# KPI Calculations
total_value = (df['Stock_Quantity'] * df['Cost_Per_Unit']).sum()

# Pre-evaluate alerts for all rows to calculate KPIs
df['alerts'] = df.apply(lambda row: evaluate_row(row), axis=1)

# KPI: Expiry Risk Value (Sum of cost for items with Priority 1 alerts)
expiry_risk_value = df[df['alerts'].apply(lambda x: any(a['priority'] == 1 for a in x))].apply(
    lambda r: r['Stock_Quantity'] * r['Cost_Per_Unit'], axis=1
).sum()

# KPI: Pending Reorders (Count of items with Priority 2 alerts)
pending_reorders = df['alerts'].apply(lambda x: any(a['priority'] == 2 for a in x)).sum()

# Display KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Inventory Value", f"${total_value:,.2f}")
col2.metric("Expiry Risk Value", f"${expiry_risk_value:,.2f}", delta="-Critical", delta_color="inverse")
col3.metric("Pending Reorders", pending_reorders)

st.divider()

# Display Alerts with Priority
st.subheader("Inventory Action Center")

for _, row in df.iterrows():
    alerts = row['alerts']
    
    # Apply Sidebar Filter
    if show_critical_only:
        alerts = [a for a in alerts if a['priority'] == 1]
    
    if alerts:
        with st.expander(f"Analysis: {row['Item_Name']}"):
            # Show individual priority alerts
            for alert in alerts:
                if alert['priority'] == 1:
                    st.error(alert['message'])
                elif alert['priority'] == 2:
                    st.warning(alert['message'])
                else:
                    st.info(alert['message'])
            
            # Generate and show structured explanation
            explanation = generate_explanation(row, alerts)
            st.markdown(explanation)