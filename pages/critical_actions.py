import streamlit as st
from src.data.database_manager import DatabaseManager
from src.core.data_processing import process_data
from src.core.decision_engine import evaluate_row
from src.core.medicine_suggester import suggest_alternatives, explain_alternatives

st.set_page_config(page_title="Critical Actions", layout="wide", page_icon="🚨")

st.title("🚨 Critical Actions")
st.markdown("*Items requiring immediate attention*")

# Initialize Database Manager
db = DatabaseManager()
df_raw = db.get_all_inventory()
df = process_data(df_raw)

# Get automation setting from session
automation_on = st.session_state.get('automation_mode', False)

# Evaluate all items
df['execution_context'] = df.apply(lambda row: evaluate_row(row, automation_enabled=automation_on), axis=1)
df['alerts'] = df['execution_context'].apply(lambda ctx: ctx.get_all_alerts())

# Get critical items
critical_df = df[df['alerts'].apply(lambda x: any(a['priority'] == 1 for a in x))]

if critical_df.empty:
    st.info("✅ No critical actions required at this time.")
else:
    st.warning(f"⚠️ {len(critical_df)} items require critical attention")
    st.divider()
    
    for _, item in critical_df.iterrows():
        p1_alerts = [a for a in item['alerts'] if a['priority'] == 1]
        
        with st.expander(f"🔴 {item['Item_Name']} - {item['Category']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Stock", f"{item['Stock_Quantity']} units")
                st.metric("Min Required", f"{item['Min_Stock_Level']} units")
            
            with col2:
                st.metric("Days to Stockout", f"{item['Days_Until_Stockout']:.1f} days")
                st.metric("Avg Daily Usage", f"{item['Avg_Daily_Usage']:.2f} units")
            
            with col3:
                st.metric("Expiry Date", item['Expiry_Date'].strftime('%Y-%m-%d'))
                st.metric("Supplier", item['Supplier_Name'])
            
            st.divider()
            
            st.subheader("Alert Details")
            for alert in p1_alerts:
                st.error(f"**{alert['type']}**: {alert['message']}")
            
            st.divider()
            st.subheader("Recommended Actions")
            for i, alert in enumerate(p1_alerts, 1):
                st.write(f"{i}. {alert['message']}")
            
            # Suggest Alternative Button
            if st.button("💡 Suggest Alternative", key=f"alt_{item['Item_ID']}"):
                alt_result = suggest_alternatives(item['Item_Name'])
                if alt_result['found']:
                    st.success(f"**Composition**: {alt_result['composition']}")
                    st.info(f"**Alternatives**: {', '.join(alt_result['alternatives'])}")
                    explanation_text = explain_alternatives(
                        item['Item_Name'], 
                        alt_result['alternatives'], 
                        alt_result['composition']
                    )
                    st.markdown(f"**Explanation**:\n{explanation_text}")
                else:
                    st.warning("No alternatives found for this medicine.")
