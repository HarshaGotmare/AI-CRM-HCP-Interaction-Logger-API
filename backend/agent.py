import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from dateutil import parser

from backend.tools import (
    summarize_interaction_tool,
    sentiment_analysis_tool,
    followup_suggestion_tool
)

from backend.database import save_interaction


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

    match = re.search(r"Dr\.?\s+[A-Za-z]+", text, re.IGNORECASE)

    if match:
        return match.group(0)

    return "Unknown"


def extract_time(text):

    match = re.search(r"\b\d{1,2}\s?(am|pm)\b", text.lower())

    if match:
        time_str = match.group(0)

        hour = int(re.search(r"\d+", time_str).group())

        if "pm" in time_str and hour != 12:
            hour += 12

        if "am" in time_str and hour == 12:
            hour = 0

        return f"{hour:02d}:00"

    return ""


def extract_date(text):

    try:

        date = parser.parse(text, fuzzy=True)

        return date.strftime("%Y-%m-%d")

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

    save_interaction(data)

    return data