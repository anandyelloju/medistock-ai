import streamlit as st
from src.core.action_manager import generate_purchase_order
from src.core.email_manager import send_purchase_order_email
from src.data.database_manager import DatabaseManager
from src.core.data_processing import process_data
from src.core.decision_engine import evaluate_row
from src.core.llm_explainer import generate_explanation
from src.core.medicine_suggester import suggest_alternatives, explain_alternatives

st.set_page_config(page_title="Inventory Center", layout="wide", page_icon="📦")

st.title("📦 Inventory Action Center")
st.markdown("*Detailed analysis and action plans for each item*")

# Initialize Database Manager
db = DatabaseManager()
df_raw = db.get_all_inventory()
df = process_data(df_raw)

# Get automation setting from session
automation_on = st.session_state.get('automation_mode', False)

# Sidebar filter
show_critical_only = st.sidebar.checkbox("Show Only Critical Alerts", value=False)

# Evaluate all items
df['execution_context'] = df.apply(lambda row: evaluate_row(row, automation_enabled=automation_on), axis=1)
df['alerts'] = df['execution_context'].apply(lambda ctx: ctx.get_all_alerts())

# Display items
displayed_count = 0
for _, row in df.iterrows():
    alerts = row['alerts']
    
    # Apply sidebar filter
    if show_critical_only:
        alerts = [a for a in alerts if a['priority'] == 1]
    
    if alerts:
        displayed_count += 1
        full_ctx = row['execution_context']
        primary_alert = sorted(alerts, key=lambda x: x['priority'])[0]
        header = f"{row['Item_Name']} — {primary_alert['type']}"
        
        with st.expander(header):
            # --- WORKFLOW VISUALIZATION ---
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

            # --- CONTEXTUAL INFO SECTION ---
            ctx = full_ctx.domain_knowledge
            ccol1, ccol2 = st.columns(2)
            ccol1.write(f"📂 **Category**: {ctx.get('category', 'N/A')}")
            
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

            # --- EXECUTION PLAN SECTION ---
            exec_plan = next((a for a in alerts if a['type'] == 'EXECUTION_PLAN'), None)
            if exec_plan:
                st.markdown("### 📦 Procurement Plan")
                pcol1, pcol2 = st.columns(2)
                pcol1.metric("Order Quantity", f"{exec_plan['reorder_qty']} units")
                pcol2.info(f"**Urgency**: {exec_plan['urgency']}")
                st.divider()

            # --- ACTION EXECUTION LOG SECTION ---
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
                        st.rerun()
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
                        st.rerun()
                elif action_log and action_log['status'] == 'EXECUTED':
                    st.button("✅ Order Processed", key=f"done_{row['Item_ID']}", disabled=True)
                else:
                    st.button(f"Mark {row['Item_Name']} for Review", key=f"btn_{row['Item_ID']}")
            else:
                st.button(f"Mark {row['Item_Name']} for Review", key=f"btn_{row['Item_ID']}")

if displayed_count == 0:
    st.info("No items to display based on current filters.")
