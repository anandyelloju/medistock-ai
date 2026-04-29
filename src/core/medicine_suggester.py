import json
import os

from groq import Groq

from .config import Config

client = Groq(api_key=Config.GROQ_API_KEY)


def suggest_alternatives(medicine_name: str) -> dict:
    """Suggest alternative brand names for a medicine.

    Loads medicine knowledge from `database/medicine_knowledge.json` and returns
    composition and alternatives if the medicine is found.
    """
    if not isinstance(medicine_name, str):
        return {
            "found": False,
            "message": "No alternatives found"
        }

    normalized_name = medicine_name.strip().lower()
    if not normalized_name:
        return {
            "found": False,
            "message": "No alternatives found"
        }

    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "database", "medicine_knowledge.json")
    json_path = os.path.abspath(json_path)

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            medicines = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "found": False,
            "message": "No alternatives found"
        }

    for medicine in medicines:
        name = medicine.get("medicine_name", "").strip().lower()
        if name == normalized_name:
            return {
                "found": True,
                "composition": medicine.get("composition", ""),
                "alternatives": medicine.get("alternative_brands", [])
            }

    return {
        "found": False,
        "message": "No alternatives found"
    }


def explain_alternatives(medicine_name: str, alternatives: list, composition: str) -> str:
    """Explain why the listed alternatives are suitable substitutes.

    Uses the configured Groq LLM when available. If the API call fails,
    returns a deterministic fallback explanation string.
    """
    if not isinstance(medicine_name, str) or not medicine_name.strip():
        return "No explanation available for an invalid medicine name."

    medicine_name = medicine_name.strip()
    composition = composition or "Unknown composition"
    alternatives = alternatives or []

    prompt = f"""
You are a knowledgeable pharmacy assistant.
Explain why the following alternative brands are suitable substitutes for the medicine below.
Keep the response concise, factual, and easy to read.

Medicine: {medicine_name}
Composition: {composition}
Suggested Alternatives: {', '.join(alternatives) if alternatives else 'None'}

Provide:
- A brief explanation of how the alternatives match the active ingredient or therapeutic profile.
- Practical guidance on selecting the best interchangeable brand by strength and formulation.
- A short note about confirming availability or pharmacist advice.

Return plain text only.
"""

    try:
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not configured")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional pharmacy assistant. Keep responses concise and practical."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=220,
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
    except Exception as exc:
        return _generate_fallback_explanation(
            medicine_name=medicine_name,
            alternatives=alternatives,
            composition=composition,
            error=str(exc)
        )


def _generate_fallback_explanation(medicine_name: str, alternatives: list, composition: str, error: str) -> str:
    """Fallback explanation when the LLM is unavailable."""
    alternative_text = ", ".join(alternatives) if alternatives else "No alternatives were provided."

    if alternatives:
        guidance = (
            "These alternatives are listed because they share the same active ingredient or therapeutic effect. "
            "Match the dosage strength and formulation before substitution, and confirm availability with a pharmacist."
        )
    else:
        guidance = (
            "No direct alternative brands are available in the knowledge base. "
            "Consider consulting clinical guidance or a pharmacist for an equivalent formulation."
        )

    return (
        f"⚠️ Fallback explanation due to LLM error: {error}\n\n"
        f"Medicine: {medicine_name}\n"
        f"Composition: {composition}\n"
        f"Alternatives: {alternative_text}\n\n"
        f"{guidance}"
    )
