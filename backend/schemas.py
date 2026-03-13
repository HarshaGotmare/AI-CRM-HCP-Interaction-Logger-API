from pydantic import BaseModel


class Interaction(BaseModel):
    doctor_name: str
    interaction_type: str
    topics_discussed: str
    sentiment: str
    followup: str
    summary: str