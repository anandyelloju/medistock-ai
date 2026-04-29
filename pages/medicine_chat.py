import streamlit as st
from groq import Groq
from src.core.medicine_suggester import suggest_alternatives, explain_alternatives
from src.core.config import Config
from src.data.database_manager import DatabaseManager

st.set_page_config(page_title="Medicine Chat", layout="wide", page_icon="💬")

# Initialize database and LLM client
db = DatabaseManager()
client = Groq(api_key=Config.GROQ_API_KEY) if Config.GROQ_API_KEY else None


# ============ HELPER FUNCTIONS ============

def extract_medicine_name(question):
    """Extract medicine name from user question"""
    question_lower = question.lower().strip()

    # Common medicine names to check for
    common_medicines = [
        "paracetamol", "amoxicillin", "insulin glargine", "atorvastatin",
        "metformin", "ibuprofen", "cetirizine", "lisinopril"
    ]

    for medicine in common_medicines:
        if medicine in question_lower:
            return medicine.title()

    # Extract words that might be medicine names
    words = question_lower.split()
    for word in words:
        if len(word) > 3 and word not in ['what', 'tell', 'about', 'used', 'for', 'how', 'does', 'work', 'take', 'medicine', 'drug', 'is']:
            return word.title()

    return None


def get_llm_medicine_info(medicine_name):
    """Get medicine information from LLM when not in database"""
    if not client:
        return None

    prompt = f"""
You are a knowledgeable pharmacy assistant. Provide information about: {medicine_name}

Return ONLY a JSON response in this exact format:
{{
    "composition": "Active ingredient and strength",
    "uses": "Primary uses/conditions",
    "dosage": "Typical adult dosage",
    "warnings": "Important warnings or precautions",
    "alternatives": ["alternative brand 1", "alternative brand 2"]
}}

Be accurate and concise. If the medicine is not a real pharmaceutical, indicate that.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional pharmacist providing accurate medicine information. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.1
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        import json
        try:
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            return None
    except Exception:
        return None


def generate_medicine_usage(medicine_name, composition):
    """Generate usage information using LLM"""
    if not client:
        return _fallback_usage_info(medicine_name, composition)

    prompt = f"""
You are a knowledgeable pharmacy assistant. Provide brief, accurate information about:

Medicine: {medicine_name}
Composition: {composition}

Format as:
**Uses**: [Primary uses]
**Dosage**: [Typical adult dose]
**Warnings**: [Important precautions]

Keep it concise and factual.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional pharmacy assistant. Keep responses concise and practical."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _fallback_usage_info(medicine_name, composition)


def _fallback_usage_info(medicine_name, composition):
    """Fallback usage information when LLM is unavailable"""
    fallbacks = {
        "Paracetamol": "**Uses**: Pain relief and fever reduction\n**Dosage**: 500-1000mg every 4-6 hours (max 4000mg/day)\n**Warnings**: Do not exceed maximum daily dose",
        "Ibuprofen": "**Uses**: Pain, inflammation, and fever\n**Dosage**: 200-400mg every 4-6 hours\n**Warnings**: Take with food; avoid with gastric ulcers",
        "Amoxicillin": "**Uses**: Bacterial infections\n**Dosage**: Varies by condition (typically 250-500mg)\n**Warnings**: Complete full course; may cause allergic reactions",
        "Cetirizine": "**Uses**: Allergy relief\n**Dosage**: 10mg once daily\n**Warnings**: May cause drowsiness in some people",
        "Metformin": "**Uses**: Type 2 diabetes management\n**Dosage**: 500mg twice daily (with meals)\n**Warnings**: Contraindicated in kidney disease",
        "Atorvastatin": "**Uses**: Cholesterol reduction\n**Dosage**: 10-20mg once daily\n**Warnings**: May interact with other medications",
        "Lisinopril": "**Uses**: High blood pressure\n**Dosage**: 10mg once daily\n**Warnings**: Can cause dizziness; monitor blood pressure",
        "Insulin Glargine": "**Uses**: Long-acting insulin for diabetes\n**Dosage**: Individualized by healthcare provider\n**Warnings**: Requires proper injection technique"
    }

    fallback = fallbacks.get(medicine_name,
        f"No specific information available. Please consult healthcare professional for {medicine_name}.")
    return fallback


# ============ UI SECTION ============

st.title("💬 Medicine Information Chat")
st.markdown("*Ask questions about medicines and get usage information*")

st.subheader("💊 Ask About Medicine")

# Input box
user_question = st.text_input(
    "Ask about medicine:",
    placeholder="e.g., What is Paracetamol used for? Or Tell me about Ibuprofen",
    help="Ask about medicine usage, dosage, or alternatives"
)

# Process question when user enters something
if user_question.strip():
    st.divider()

    # Try to extract medicine name from question
    medicine_name = extract_medicine_name(user_question)

    if medicine_name:
        st.subheader(f"📋 Information about: {medicine_name}")

        # First, try to get from knowledge base
        alt_result = suggest_alternatives(medicine_name)

        if alt_result['found']:
            # Medicine found in database
            st.success("✅ **Data Source**: Found in our Medicine Knowledge Base (Database)")

            # Create info cards
            with st.container(border=True):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 💊 **Composition**")
                    st.markdown(f"`{alt_result['composition']}`")

                with col2:
                    st.markdown("### 🧪 **Details**")
                    # Generate usage explanation using LLM
                    usage_info = generate_medicine_usage(medicine_name, alt_result['composition'])
                    st.markdown(usage_info)

            # Show alternatives if available
            if alt_result['alternatives']:
                st.divider()
                st.subheader("🔄 Alternative Brands Available")
                
                alternatives_str = ", ".join(alt_result['alternatives'])
                st.info(f"**Alternative Brands**: {alternatives_str}")
                
                # Show explanation for alternatives
                st.markdown("### Why These Alternatives?")
                explanation_text = explain_alternatives(
                    medicine_name,
                    alt_result['alternatives'],
                    alt_result['composition']
                )
                st.markdown(explanation_text)

        else:
            # Medicine not in database, try LLM
            st.info("🔍 **Searching...** Medicine not found in our database. Querying AI knowledge base...")

            llm_info = get_llm_medicine_info(medicine_name)

            if llm_info and 'composition' in llm_info:
                st.success("✅ **Data Source**: Found via AI Lookup (Large Language Model)")

                # Create info cards
                with st.container(border=True):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 💊 **Composition**")
                        st.markdown(f"`{llm_info.get('composition', 'N/A')}`")
                        
                        if llm_info.get('alternatives'):
                            st.markdown("### 🔄 **Alternatives Identified**")
                            alts = ", ".join(llm_info['alternatives'])
                            st.markdown(f"• {alts}")

                    with col2:
                        st.markdown("### 📖 **Medical Details**")
                        st.markdown(f"**Uses**: {llm_info.get('uses', 'N/A')}\n\n"
                                   f"**Dosage**: {llm_info.get('dosage', 'N/A')}\n\n"
                                   f"**Warnings**: {llm_info.get('warnings', 'N/A')}")

                # Show alternatives explanation if available
                if llm_info.get('alternatives'):
                    st.divider()
                    st.subheader("🔄 Why These Alternatives?")
                    explanation_text = explain_alternatives(
                        medicine_name,
                        llm_info['alternatives'],
                        llm_info.get('composition', '')
                    )
                    st.markdown(explanation_text)
                
                st.caption("💡 *Information provided by AI may need verification. Always consult a healthcare professional.*")

            else:
                st.warning(f"⚠️ **Search Result**: Could not find information about '{medicine_name}'")
                st.error("This may not be a recognized pharmaceutical. Please:")
                st.markdown("""
                - Check the spelling of the medicine name
                - Try with a more common brand name
                - Verify the medicine is currently in use
                - Consult a healthcare professional for accurate information
                """)

    else:
        st.error("❌ **Search Failed**: Could not identify a medicine name in your question")
        st.markdown("""
        Please try again with a specific medicine name. Examples:
        - "Tell me about Aspirin"
        - "What is Metformin used for?"
        - "Information on Ibuprofen"
        - "How does Amoxicillin work?"
        """)

st.divider()
st.caption("💡 **Medical Disclaimer**: This chatbot provides general informational purposes only. It is not a substitute for professional medical advice. Always consult a qualified healthcare professional before making any medical decisions.")