import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from dateutil import parser

from backend.tools import (
    summarize_interaction_tool,
    sentiment_analysis_tool,
    followup_suggestion_tool
)


class InteractionState(TypedDict):
    text: str
    summary: str
    sentiment: str
    followup: str


# -------- LANGGRAPH NODES --------

def summarize_node(state: InteractionState):
    return {"summary": summarize_interaction_tool(state["text"])}


def sentiment_node(state: InteractionState):
    return {"sentiment": sentiment_analysis_tool(state["text"])}


def followup_node(state: InteractionState):
    return {"followup": followup_suggestion_tool(state["text"])}


workflow = StateGraph(InteractionState)

workflow.add_node("summarize", summarize_node)
workflow.add_node("sentiment", sentiment_node)
workflow.add_node("followup", followup_node)

workflow.set_entry_point("summarize")

workflow.add_edge("summarize", "sentiment")
workflow.add_edge("sentiment", "followup")
workflow.add_edge("followup", END)

graph = workflow.compile()


# -------- MEMORY --------
last_interaction = {}


# -------- EXTRACTION FUNCTIONS --------

def extract_doctor(text):
    match = re.search(
        r'\b(Dr\.?\s+[A-Za-z]+(?:\s+[A-Za-z]+)?)\b(?=\s+(?:on|at|for|to|regarding)\b|[.,]|$)',
        text,
        re.IGNORECASE
    )

    if match:
        doctor = match.group(1).strip()
        doctor = doctor.replace("Dr.", "Dr")
        return doctor

    return "Unknown"


def extract_time(text):
    match = re.search(
        r'\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b',
        text,
        re.IGNORECASE
    )

    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        meridiem = match.group(3).lower()

        if meridiem == "pm" and hour != 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0

        return f"{hour:02d}:{minute:02d}"

    return ""


def extract_date(text):
    try:
        patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b',
            r'\b[A-Za-z]+\s+\d{1,2},\s*\d{4}\b'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date = parser.parse(match.group(0), dayfirst=True)
                year = date.year

                if year < 2000 or year > 2100:
                    return ""

                return date.strftime("%Y-%m-%d")

        return ""
    except:
        return ""


# -------- MAIN FUNCTION --------

def process_interaction(text: str):
    global last_interaction

    text_lower = text.lower()

    # -------- EDIT DOCTOR --------
    if "name" in text_lower and "dr" in text_lower:
        doctor = extract_doctor(text)
        last_interaction["doctor_name"] = doctor
        return last_interaction

    # -------- EDIT TIME --------
    if "time" in text_lower:
        time = extract_time(text)
        if time:
            last_interaction["time"] = time
        return last_interaction

    # -------- NEW INTERACTION --------
    result = graph.invoke({"text": text})

    doctor = extract_doctor(text)
    date = extract_date(text)
    time = extract_time(text)

    data = {
        "doctor_name": doctor,
        "date": date,
        "time": time,
        "interaction_type": "Meeting",
        "topics": result.get("summary"),
        "sentiment": result.get("sentiment"),
        "followup": result.get("followup")
    }

    last_interaction = data
    return data