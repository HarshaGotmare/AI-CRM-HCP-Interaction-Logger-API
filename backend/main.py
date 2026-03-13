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


@app.get("/")
def root():
    return {"message": "AI CRM Backend Running"}


@app.post("/process")
def process_interaction_api(request: InteractionRequest):

    data = process_interaction(request.text)

    interaction_id = save_interaction(data)

    data["id"] = interaction_id

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
        update.topics,
        update.sentiment,
        update.followup
    )

    return {"message": "Interaction updated"}