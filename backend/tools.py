import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = None
if GROQ_API_KEY:
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=GROQ_API_KEY
        )
    except Exception:
        llm = None


def summarize_interaction_tool(text: str) -> str:
    text_lower = text.lower()

    topic = "General medical discussion"

    if "diabetes" in text_lower:
        topic = "Discussion about diabetes medication"
    elif "hypertension" in text_lower:
        topic = "Discussion about hypertension treatment"
    elif "cholesterol" in text_lower:
        topic = "Discussion about cholesterol medication"
    elif "cardiology" in text_lower:
        topic = "Discussion about cardiology treatment"
    elif "drug" in text_lower or "medicine" in text_lower or "therapy" in text_lower:
        topic = "Discussion about pharmaceutical treatment"

    if "brochure" in text_lower:
        topic += " and product brochure shared"

    if "clinical" in text_lower or "trial" in text_lower:
        topic += " and clinical trial data requested"

    return topic


def sentiment_analysis_tool(text: str) -> str:
    text_lower = text.lower()

    positive_words = [
        "positive",
        "interested",
        "interest",
        "liked",
        "good response",
        "agreed",
        "appreciated"
    ]

    negative_words = [
        "negative",
        "not interested",
        "declined",
        "rejected",
        "unhappy",
        "refused"
    ]

    if any(word in text_lower for word in negative_words):
        return "Negative"

    if any(word in text_lower for word in positive_words):
        return "Positive"

    return "Neutral"


def followup_suggestion_tool(text: str) -> str:
    text_lower = text.lower()

    if "clinical" in text_lower or "trial" in text_lower:
        return "Share clinical trial data"

    if "brochure" in text_lower:
        return "Send product brochure"

    if "demo" in text_lower or "demonstration" in text_lower:
        return "Schedule product demonstration"

    if "sample" in text_lower or "samples" in text_lower:
        return "Arrange product samples"

    return "Follow up during next doctor visit"


def log_interaction_tool(data: dict):
    return data


def edit_interaction_tool(current_data: dict, update: dict):
    current_data.update(update)
    return current_data