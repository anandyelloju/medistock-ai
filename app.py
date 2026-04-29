import streamlit as st

st.set_page_config(page_title="MediStock AI - Home", layout="wide", page_icon="💊")

# --- CUSTOM CSS FOR PREMIUM LOOK - DARK MODE AWARE ---
st.markdown("""
    <style>
    /* Light Mode Styles */
    @media (prefers-color-scheme: light) {
        .main {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            color: #333333;
        }
    }
    
    /* Dark Mode Styles */
    @media (prefers-color-scheme: dark) {
        .main {
            background-color: #0e1117;
        }
        .stMetric {
            background-color: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            color: #e8eaed;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.title("💊 MediStock AI Dashboard")
    st.markdown("### Smart Inventory Management & Auto-Ordering")
    st.markdown("*Smart automation for pharmacy inventory*")

st.divider()

# --- WELCOME SECTION ---
st.markdown("""
Welcome to **MediStock AI**, a cutting-edge pharmacy inventory management system powered by 
multi-agent AI. Navigate through the pages using the **sidebar menu** to explore different features.
""")

st.divider()

# --- QUICK NAVIGATION ---
st.subheader("📍 Quick Navigation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 📊 Dashboard
    View key performance indicators and inventory health overview
    """)
    if st.button("Go to Dashboard", key="btn_dash", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    st.markdown("""
    ### 🚨 Critical Actions
    Review items requiring immediate attention
    """)
    if st.button("View Critical Items", key="btn_crit", use_container_width=True):
        st.switch_page("pages/critical_actions.py")

with col3:
    st.markdown("""
    ### 📦 Inventory Center
    Detailed analysis for each item
    """)
    if st.button("Manage Inventory", key="btn_inv", use_container_width=True):
        st.switch_page("pages/inventory_center.py")

with col4:
    st.markdown("""
    ### 💬 Medicine Chat
    Ask questions about medicines
    """)
    if st.button("Chat About Medicine", key="btn_chat", use_container_width=True):
        st.switch_page("pages/medicine_chat.py")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📈 Analytics
    System performance and decision history
    """)
    if st.button("View Analytics", key="btn_ana", use_container_width=True):
        st.switch_page("pages/analytics.py")

with col2:
    st.markdown("""
    ### ⚙️ Settings
    Configure automation and preferences
    """)
    if st.button("Go to Settings", key="btn_set", use_container_width=True):
        st.switch_page("pages/settings.py")

st.divider()

# --- KEY FEATURES ---
st.subheader("✨ Key Features")

feature_cols = st.columns(3)

with feature_cols[0]:
    st.markdown("""
    **🔍 Real-time Analysis**
    - Continuous inventory monitoring
    - Automated risk detection
    - Expiry tracking
    """)

with feature_cols[1]:
    st.markdown("""
    **🧠 Smart Suggestions**
    - Predictive stockout alerts
    - Optimal reorder quantities
    - Adaptive learning
    """)

with feature_cols[2]:
    st.markdown("""
    **📦 Automated Procurement**
    - Smart supplier selection
    - Automatic PO generation
    - Email notifications
    """)

st.divider()

# --- SYSTEM COMPONENTS ---
st.subheader("🤖 Smart Automation System")

with st.expander("Learn about our agents"):
    st.markdown("""
    **Expiry Monitor** 🗓️
    - Monitors expiration dates
    - Flags items approaching expiry
    - Prioritizes disposal planning
    
    **Slow Stock Alert** 📦
    - Identifies slow-moving inventory
    - Analyzes historical usage patterns
    - Suggests promotional strategies
    
    **Stock Predictor** 🧠
    - Predicts stockout risks
    - Calculates safety buffers
    - Recommends reorder volumes
    
    **Auto Reorder** 🎯
    - Creates detailed procurement plans
    - Determines urgency levels
    - Adapts to historical performance
    
    **Supplier Picker** 🏭
    - Evaluates delivery times
    - Compares pricing
    - Prioritizes reliability
    
    **Order Processing** ⚡
    - Generates purchase orders
    - Sends supplier notifications
    - Logs all actions
    
    **System Logic** 🎪
    - Orchestrates all agents
    - Manages dependencies
    - Ensures workflow integrity
    """)

st.divider()

# --- GETTING STARTED ---
st.subheader("🚀 Getting Started")

with st.expander("First-time setup guide", expanded=False):
    st.markdown("""
    1. **Review Dashboard** - Check overall inventory health
    2. **Check Critical Items** - Address items needing attention
    3. **Configure Settings** - Enable automation if preferred
    4. **Monitor Analytics** - Track system performance
    5. **Manage Inventory** - Generate POs and track actions
    """)

st.divider()

st.markdown("""
---
**MediStock AI v1.0** | Production Ready ✅  
Navigate using the **sidebar menu** on the left to access all sections.
""")
import streamlit as st
import pandas as pd
from src.data.database_manager import DatabaseManager
from src.core.action_manager import generate_purchase_order
from src.core.data_processing import process_data
from src.core.decision_engine import evaluate_row
from src.core.email_manager import send_purchase_order_email
from src.core.llm_explainer import generate_explanation
from src.data.knowledge_base import kb
from src.core.medicine_suggester import suggest_alternatives, explain_alternatives

st.set_page_config(page_title="MediStock AI - Dashboard", layout="wide", page_icon="💊")

# --- CUSTOM CSS FOR PREMIUM LOOK - DARK MODE AWARE ---
st.markdown("""
    <style>
    /* Light Mode Styles */
    @media (prefers-color-scheme: light) {
        .main {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            color: #333333;
        }
        .critical-banner {
            padding: 15px;
            background-color: #ffebee;
            border-left: 5px solid #d32f2f;
            color: #b71c1c;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .info-banner {
            padding: 15px;
            background-color: #e3f2fd;
            border-left: 5px solid #1976d2;
            color: #0d47a1;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    }
    
    /* Dark Mode Styles */
    @media (prefers-color-scheme: dark) {
        .main {
            background-color: #0e1117;
        }
        .stMetric {
            background-color: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            color: #e8eaed;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
        .critical-banner {
            padding: 15px;
            background-color: rgba(211, 47, 47, 0.15);
            border-left: 5px solid #ef5350;
            color: #ff8a80;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .info-banner {
            padding: 15px;
            background-color: rgba(25, 118, 210, 0.15);
            border-left: 5px solid #42a5f5;
            color: #90caf9;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    }
    
    /* Expander and Container Styling */
    .stExpander {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Database Manager
db = DatabaseManager()

# Pull data from SQLite
df_raw = db.get_all_inventory()

# Process data to calculate derived metrics (Days_To_Expiry, etc.)
df = process_data(df_raw)

# Sidebar Configuration
st.sidebar.header("🛠️ Settings")
show_critical_only = st.sidebar.checkbox("Show Only Critical Alerts", value=False)
automation_on = st.sidebar.toggle("🤖 Automation Mode", value=False, help="When ON, system will auto-generate and email Purchase Orders.")

st.sidebar.divider()
st.sidebar.subheader("📈 System Learning")
success_rate = db.get_success_rate()
st.sidebar.metric("AI Accuracy", f"{success_rate:.1f}%", delta="Adaptive")

try:
    perf_logs = db.get_all_performance_logs(limit=3)
    if not perf_logs.empty:
        for _, log in perf_logs.iterrows():
            score_icon = "🟢" if log['score'] == "GOOD" else "🟡" if log['score'] == "AVERAGE" else "🔴"
            st.sidebar.caption(f"{score_icon} **{log['medicine_name']}**: {log['score']}")
    else:
        st.sidebar.caption("System gathering feedback...")
except Exception:
    st.sidebar.caption("Evaluation layer starting...")

st.sidebar.divider()
st.sidebar.subheader("📜 Recent Activity")
try:
    recent_logs = db.get_action_logs(limit=5)
    if not recent_logs.empty:
        for _, log in recent_logs.iterrows():
            status_icon = "✅" if log['status'] == "SUCCESS" else "❌"
            st.sidebar.caption(f"{status_icon} **{log['medicine_name']}**")
            st.sidebar.caption(f"Qty: {log['quantity']} | {log['timestamp']}")
    else:
        st.sidebar.info("No recent actions logged.")
except Exception:
    st.sidebar.info("Logging system initializing...")

# --- HEADER SECTION ---
hcol1, hcol2 = st.columns([0.8, 0.2])
with hcol1:
    st.title("💊 MediStock AI Dashboard")
    st.markdown("##### *Smart Inventory Management & Auto-Ordering*")
with hcol2:
    if st.button("🔄 Refresh Data", type="secondary", use_container_width=True):
        st.rerun()

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

# KPI Calculations
total_value = (df['Stock_Quantity'] * df['Cost_Per_Unit']).sum()

# Pre-evaluate context for all rows to calculate KPIs
df['execution_context'] = df.apply(lambda row: evaluate_row(row, automation_enabled=automation_on), axis=1)
df['alerts'] = df['execution_context'].apply(lambda ctx: ctx.get_all_alerts())

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

# --- NEW: CRITICAL ACTIONS SECTION ---
critical_df = df[df['alerts'].apply(lambda x: any(a['priority'] == 1 for a in x))]
if not critical_df.empty:
    st.subheader("🚨 Critical Actions")
    for _, item in critical_df.iterrows():
        # Get the primary critical alert message
        p1_alert = [a for a in item['alerts'] if a['priority'] == 1][0]
        st.warning(f"**{item['Item_Name']}**: {p1_alert['message']}")
    st.divider()

# Display Alerts with Priority
st.subheader("Inventory Action Center")

for _, row in df.iterrows():
    alerts = row['alerts']
    
    # Apply Sidebar Filter
    if show_critical_only:
        alerts = [a for a in alerts if a['priority'] == 1]
    
    if alerts:
        # Get execution context
        full_ctx = row['execution_context']
        
        # Determine Primary Risk for Header
        primary_alert = sorted(alerts, key=lambda x: x['priority'])[0]
        header = f"{row['Item_Name']} — {primary_alert['type']}"
        
        with st.expander(header):
            # --- NEW: WORKFLOW VISUALIZATION ---
            st.caption("🤖 **System Workflow**")
            w1, w2, w3 = st.columns(3)
            
            with w1:
                st.markdown("🔍 **Risk Check**")
                for a in full_ctx.risk_flags.values():
                    st.caption(f"• {a['type']}")
            with w2:
                if full_ctx.decisions:
                    st.markdown("🧠 **Smart Suggestions**")
                    for a in full_ctx.decisions.values():
                        st.caption(f"• {a['type']}")
                else:
                    st.caption("*(Skipped)*")
            with w3:
                if full_ctx.actions:
                    st.markdown("⚡ **Auto Actions**")
                    for a in full_ctx.actions.values():
                        st.caption(f"• {a['status']}")
                else:
                    st.caption("*(Skipped)*")
            
            st.divider()

            # Domain knowledge from context
            ctx = full_ctx.domain_knowledge

            # --- CONTEXTUAL INFO SECTION ---
            ccol1, ccol2 = st.columns(2)
            ccol1.write(f"📂 **Category**: {ctx.get('category', 'N/A')}")
            
            # Highlight criticality levels
            crit_val = ctx.get('criticality', 'Medium')
            if crit_val == 'Critical':
                ccol2.write(f"⚖️ **Criticality**: 🔴 `{crit_val}`")
            elif crit_val == 'High':
                ccol2.write(f"⚖️ **Criticality**: 🟠 `{crit_val}`")
            else:
                ccol2.write(f"⚖️ **Criticality**: 🔵 `{crit_val}`")
            
            st.divider()

            # Display Priority Status
            if primary_alert['priority'] == 1:
                st.error("Status: CRITICAL RISK")
            elif primary_alert['priority'] == 2:
                st.warning("Status: ACTION REQUIRED")
            else:
                st.info("Status: MONITORING")

            # --- NEW: EXECUTION PLAN SECTION ---
            exec_plan = next((a for a in alerts if a['type'] == 'EXECUTION_PLAN'), None)
            if exec_plan:
                st.markdown("### 📦 Procurement Plan")
                pcol1, pcol2 = st.columns(2)
                pcol1.metric("Order Quantity", f"{exec_plan['reorder_qty']} units")
                pcol2.info(f"**Urgency**: {exec_plan['urgency']}")
                st.divider()

            # --- NEW: ACTION EXECUTION LOG SECTION ---
            action_log = next((a for a in alerts if a['type'] == 'ACTION_LOG'), None)
            if action_log:
                if action_log['status'] == 'EXECUTED':
                    st.success(action_log['message'])
                    st.caption(f"💾 Saved to: {action_log['file_path']}")
                elif action_log['status'] == 'FAILED':
                    st.error(action_log['message'])
                elif action_log['status'] == 'PENDING':
                    st.warning(action_log['message'])
                    st.caption("⏳ Status: PENDING - manual Purchase Order generation required.")
                else:
                    st.info(action_log['message'])
                st.divider()

            # Generate and show structured explanation
            explanation = generate_explanation(row, alerts, context=ctx)
            st.markdown(explanation)
            
            # Suggest Alternative Button
            if st.button("💡 Suggest Alternative", key=f"alt_{row['Item_ID']}"):
                alt_result = suggest_alternatives(row['Item_Name'])
                if alt_result['found']:
                    st.success(f"**Composition**: {alt_result['composition']}")
                    st.info(f"**Alternatives**: {', '.join(alt_result['alternatives'])}")
                    explanation_text = explain_alternatives(
                        row['Item_Name'], 
                        alt_result['alternatives'], 
                        alt_result['composition']
                    )
                    st.markdown(f"**Explanation**:\n{explanation_text}")
                else:
                    st.warning("No alternatives found for this medicine.")
            
            # Action Buttons
            if exec_plan:
                if action_log and action_log['status'] == 'PENDING':
                    if st.button("📄 Generate Purchase Order", key=f"po_{row['Item_ID']}", type="primary"):
                        po_plan = {
                            "medicine": row['Item_Name'],
                            "reorder_qty": exec_plan['reorder_qty'],
                            "urgency": exec_plan['urgency'],
                            "supplier": full_ctx.decisions.get('SUPPLIER_SELECTION', {}).get('supplier', 'Unknown Supplier')
                        }
                        file_path = generate_purchase_order(po_plan)
                        email_status = send_purchase_order_email(file_path) if file_path else False
                        db.log_action(
                            medicine_name=row['Item_Name'],
                            quantity=exec_plan['reorder_qty'],
                            action_type="PO_GENERATION",
                            status="SUCCESS" if file_path else "FAILURE",
                            details=f"Supplier: {po_plan['supplier']} | File: {file_path} | Email: {email_status}"
                        )
                        st.experimental_rerun()
                elif not action_log:
                    if st.button("📄 Generate Purchase Order", key=f"po_{row['Item_ID']}", type="primary"):
                        po_plan = {
                            "medicine": row['Item_Name'],
                            "reorder_qty": exec_plan['reorder_qty'],
                            "urgency": exec_plan['urgency'],
                            "supplier": full_ctx.decisions.get('SUPPLIER_SELECTION', {}).get('supplier', 'Unknown Supplier')
                        }
                        file_path = generate_purchase_order(po_plan)
                        email_status = send_purchase_order_email(file_path) if file_path else False
                        db.log_action(
                            medicine_name=row['Item_Name'],
                            quantity=exec_plan['reorder_qty'],
                            action_type="PO_GENERATION",
                            status="SUCCESS" if file_path else "FAILURE",
                            details=f"Supplier: {po_plan['supplier']} | File: {file_path} | Email: {email_status}"
                        )
                        st.experimental_rerun()
                elif action_log and action_log['status'] == 'EXECUTED':
                    st.button("✅ Order Processed", key=f"done_{row['Item_ID']}", disabled=True)
                else:
                    st.button(f"Mark {row['Item_Name']} for Review", key=f"btn_{row['Item_ID']}")
            else:
                st.button(f"Mark {row['Item_Name']} for Review", key=f"btn_{row['Item_ID']}")