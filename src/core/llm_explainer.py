import os
from groq import Groq
from ..data.database_manager import DatabaseManager
from .config import Config

# Initialize Database Manager
db = DatabaseManager()

# Initialize Groq client using centralized config
client = Groq(api_key=Config.GROQ_API_KEY)

def generate_explanation(row, alerts, context=None):
    """
    Generates a structured, actionable explanation using Groq (Llama 3.1).
    Enriched with domain context and historical performance feedback.
    """
    if not alerts:
        return ""

    # Prepare context for the LLM
    item_name = row.get('Item_Name', 'Unknown Item')
    stock = row.get('Stock_Quantity', 0)
    stockout_days = row.get('Days_Until_Stockout', 'N/A')
    alert_info = "\n".join([f"- {a['type']}: {a['message']}" for a in alerts])
    
    # Domain Knowledge Enrichment
    category = context.get('category', 'General') if context else 'General'
    criticality = context.get('criticality', 'Medium') if context else 'Medium'
    seasonal = context.get('seasonal_info', 'Steady') if context else 'Steady'

    # Performance History Enrichment
    history = db.get_performance_history(item_name, limit=3)
    history_str = "No past data available."
    if not history.empty:
        history_str = "\n".join([f"- {row['eval_timestamp']}: {row['score']}" for _, row in history.iterrows()])

    prompt = f"""
    You are an expert Pharmacy Inventory Intelligence Agent. 
    Analyze these inventory alerts for '{item_name}':
    - Category: {category}
    - Criticality: {criticality}
    - Seasonal Demand: {seasonal}
    - Current Stock: {stock} units
    - Predicted Stockout: {stockout_days} days
    - Historical Performance (Past 3 Evaluations):
    {history_str}

    - Active Alerts:
    {alert_info}

    Tasks:
    1. **Situation**: Summarize the data-driven insight (1 line).
    2. **Risk**: Describe the business and clinical impact, considering the medicine's criticality.
    3. **Action**: Provide a clear next step. If historical performance was 'POOR', explain how this recommendation is more robust (e.g., increased safety buffer).
    4. **Confidence**: Assign a confidence level (High/Medium/Low).

    Format:
    **Situation**: [Insight]
    **Risk**: [Impact]
    **Action**: [Next Step + Performance Adjustment Note]
    **Confidence**: [Level]
    """

    try:
        # Check if API key exists
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found. Please add it to your .env file.")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional inventory management consultant. Keep responses concise and focused on action."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.1
        )
        return response.choices[0].message.content

    except Exception as e:
        # Return a robust fallback if API call fails
        return _generate_fallback_explanation(row, alerts, error=str(e))

def _generate_fallback_explanation(row, alerts, error):
    """Fallback logic using rule-based templates if LLM fails."""
    # Simplified fallback to match the new 3-section structure
    primary_alert = alerts[0]
    
    if primary_alert['type'] == 'REORDER':
        sit = "Stock levels are below the required minimum threshold."
        risk = "Potential inability to fulfill immediate patient prescriptions."
        act = f"Initiate reorder from {row.get('Supplier_Name', 'supplier')}."
    elif primary_alert['type'] == 'SMART_REORDER':
        sit = f"Current consumption rate predicts a stockout in {row.get('Days_Until_Stockout', '?')} days."
        risk = "Consumption is outpacing standard supply replenishment cycles."
        act = "Increase order volume immediately to cover the predicted gap."
    elif primary_alert['type'] == 'EXPIRY':
        sit = f"Item is approaching its expiration date ({row.get('Expiry_Date', '?')})."
        risk = "Risk of total inventory value loss and disposal compliance issues."
        act = "Move to front-of-shelf or contact supplier for return options."
    else:
        sit = primary_alert['message']
        risk = "General inventory risk detected."
        act = "Manual review required."

    return (
        f"⚠️ *Note: AI Analysis Offline ({error[:40]}...)*\n\n"
        f"**Situation**: {sit}\n"
        f"**Risk**: {risk}\n"
        f"**Action**: {act}\n"
        f"**Confidence**: Medium (Rule-based)"
    )