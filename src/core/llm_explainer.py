import os
from groq import Groq
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()

# Initialize Groq client
# Llama-3.1-8b-instant is used for high speed and low latency
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(row, alerts):
    """
    Generates a structured, actionable explanation using Groq (Llama 3.1).
    Provides a professional fallback if the API is unavailable.
    """
    if not alerts:
        return ""

    # Prepare context for the LLM
    item_name = row.get('Item_Name', 'Unknown Item')
    stock = row.get('Stock_Quantity', 0)
    stockout_days = row.get('Days_Until_Stockout', 'N/A')
    alert_info = "\n".join([f"- {a['type']}: {a['message']}" for a in alerts])

    prompt = f"""
    You are an expert Pharmacy Inventory Intelligence Agent. 
    Analyze these inventory alerts for '{item_name}':
    - Current Stock: {stock} units
    - Predicted Stockout: {stockout_days} days
    - Active Alerts:
    {alert_info}

    Tasks:
    1. Provide a concise explanation (max 3 lines) of the operational and financial impact.
    2. Provide one highly specific, actionable recommendation.

    Format:
    **Analysis**: [Explanation]
    **Action**: [Recommendation]
    """

    try:
        # Check if API key exists
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found. Please add it to your .env file.")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional inventory management consultant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.2 # Lower temperature for more factual responses
        )
        return response.choices[0].message.content

    except Exception as e:
        # Return a robust fallback if API call fails
        return _generate_fallback_explanation(row, alerts, error=str(e))

def _generate_fallback_explanation(row, alerts, error):
    """Fallback logic using rule-based templates if LLM fails."""
    explanations = [f"⚠️ *Note: AI Analysis (Groq) Offline ({error})*"]
    
    for alert in alerts:
        if alert['type'] == 'REORDER':
            impact = "Stock is below safe minimum level."
            action = f"Reorder from {row.get('Supplier_Name', 'primary supplier')}."
        elif alert['type'] == 'EXPIRY':
            impact = "Item is nearing expiration date."
            action = "Prioritize for immediate sale or return."
        elif alert['type'] == 'SMART_REORDER':
            impact = f"Predicted stockout in {row.get('Days_Until_Stockout', '?')} days."
            action = "Increase reorder quantity to match demand spikes."
        else:
            impact = alert['message']
            action = "Review inventory levels."
            
        explanations.append(f"**{alert['type']}**: {impact} -> {action}")
        
    return "\n\n".join(explanations)