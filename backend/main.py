from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agent import process_interaction
from backend.database import save_interaction, get_interactions, update_interaction

app = FastAPI(title="AI CRM HCP Interaction Logger API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InteractionRequest(BaseModel):
    text: str


class InteractionUpdate(BaseModel):
    doctor_name: str
    date: str
    time: str
    interaction_type: str
    topics: str
    sentiment: str
    followup: str


current_interaction_id = None


@app.get("/")
def root():
    return {"message": "AI CRM Backend Running"}


@app.post("/process")
def process_interaction_api(request: InteractionRequest):
    global current_interaction_id

    text_lower = request.text.lower().strip()
    data = process_interaction(request.text)

    is_correction = (
        text_lower.startswith("sorry")
        or text_lower.startswith("name")
        or "name is" in text_lower
        or text_lower.startswith("time")
        or "time is" in text_lower
        or text_lower.startswith("date")
        or "date is" in text_lower
    )

    if current_interaction_id is None:
        interaction_id = save_interaction(data)
        current_interaction_id = interaction_id
        data["id"] = interaction_id
        return data

    if is_correction:
        update_interaction(
            current_interaction_id,
            data.get("doctor_name", ""),
            data.get("date", ""),
            data.get("time", ""),
            data.get("interaction_type", ""),
            data.get("topics", ""),
            data.get("sentiment", ""),
            data.get("followup", "")
        )
        data["id"] = current_interaction_id
        return data

    data["id"] = current_interaction_id
    return data


@app.get("/interactions")
def get_all_interactions():
    return get_interactions()


@app.put("/update/{interaction_id}")
def update_interaction_api(interaction_id: int, update: InteractionUpdate):
    update_interaction(
        interaction_id,
        update.doctor_name,
        update.date,
        update.time,
        update.interaction_type,
        update.topics,
        update.sentiment,
        update.followup
    )

    return {"message": "Interaction updated"}