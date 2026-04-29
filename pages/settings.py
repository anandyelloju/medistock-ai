import streamlit as st
from src.data.database_manager import DatabaseManager

st.set_page_config(page_title="Settings", layout="wide", page_icon="⚙️")

st.title("⚙️ Settings")
st.markdown("*Configure system behavior and preferences*")

db = DatabaseManager()

st.subheader("🤖 Automation Settings")

# Initialize session state for automation mode
if 'automation_mode' not in st.session_state:
    st.session_state.automation_mode = False

# Automation toggle
automation_on = st.toggle(
    "🤖 Automation Mode",
    value=st.session_state.automation_mode,
    help="When ON, system will auto-generate and email Purchase Orders. When OFF, requires manual approval."
)

# Update session state
st.session_state.automation_mode = automation_on

if automation_on:
    st.success("✅ Automation Mode is ON")
    st.info("""
    **Automation enabled:** 
    - Purchase Orders will be automatically generated for critical items
    - Emails will be sent to suppliers
    - Actions are logged to the database
    """)
else:
    st.warning("⏳ Automation Mode is OFF")
    st.info("""
    **Manual mode active:**
    - Items will show as PENDING
    - Click 'Generate Purchase Order' button to create POs manually
    - You maintain full control over each action
    """)

st.divider()

st.subheader("📊 System Learning")
success_rate = db.get_success_rate()
col1, col2, col3 = st.columns(3)
col1.metric("AI Accuracy", f"{success_rate:.1f}%", delta="Adaptive")
col2.metric("Total Decisions", "Learning...", delta="In Progress")
col3.metric("System Status", "Active", delta="Operational")

st.divider()

st.subheader("📜 Recent Activity")
try:
    recent_logs = db.get_action_logs(limit=5)
    if not recent_logs.empty:
        for _, log in recent_logs.iterrows():
            status_icon = "✅" if log['status'] == "SUCCESS" else "❌"
            st.write(f"{status_icon} **{log['medicine_name']}** - {log['action_type']}")
            st.caption(f"Qty: {log['quantity']} | {log['timestamp']}")
    else:
        st.info("No recent actions logged.")
except Exception:
    st.info("Logging system initializing...")

st.divider()

st.subheader("📈 AI Accuracy Trends")
try:
    perf_logs = db.get_all_performance_logs(limit=3)
    if not perf_logs.empty:
        for _, log in perf_logs.iterrows():
            score_icon = "🟢" if log['score'] == "GOOD" else "🟡" if log['score'] == "AVERAGE" else "🔴"
            st.write(f"{score_icon} **{log['medicine_name']}**: {log['score']}")
            st.caption(f"Evaluated: {log['eval_timestamp']}")
    else:
        st.caption("System gathering feedback...")
except Exception:
    st.caption("Evaluation layer starting...")

st.divider()

st.subheader("ℹ️ About MediStock AI")
st.markdown("""
**MediStock AI Dashboard v1.0**

An autonomous inventory management system powered by multi-agent AI orchestration.

**Features:**
- 🔍 Real-time inventory analysis
- 🧠 Intelligent reorder decisions
- 📦 Automated procurement planning
- 🚀 Supplier optimization
- 📊 Performance tracking

**Agents:**
- ExpiryAgent: Monitors expiration dates
- DeadStockAgent: Identifies slow-moving inventory
- InventoryIntelligenceAgent: Predicts stockouts
- ReorderExecutionAgent: Plans reorder quantities
- SupplierSelectionAgent: Chooses optimal suppliers
- ActionExecutionAgent: Generates purchase orders
- CoordinatorAgent: Orchestrates all agents

**Status:** Production Ready ✅
""")
