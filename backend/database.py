from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./crm.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String)
    date = Column(String)
    time = Column(String)
    interaction_type = Column(String)
    topics = Column(String)
    sentiment = Column(String)
    followup = Column(String)


Base.metadata.create_all(bind=engine)


# -------- SAVE NEW INTERACTION --------
def save_interaction(data):
    db = SessionLocal()

    try:
        interaction = Interaction(
            doctor_name=data.get("doctor_name"),
            date=data.get("date"),
            time=data.get("time"),
            interaction_type=data.get("interaction_type"),
            topics=data.get("topics"),
            sentiment=data.get("sentiment"),
            followup=data.get("followup")
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return interaction.id

    finally:
        db.close()


# -------- UPDATE EXISTING INTERACTION --------
def update_interaction(interaction_id, doctor_name, date, time, interaction_type, topics, sentiment, followup):
    db = SessionLocal()

    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()

        if not interaction:
            return False

        interaction.doctor_name = doctor_name
        interaction.date = date
        interaction.time = time
        interaction.interaction_type = interaction_type
        interaction.topics = topics
        interaction.sentiment = sentiment
        interaction.followup = followup

        db.commit()

        return True

    finally:
        db.close()


# -------- GET ALL INTERACTIONS --------
def get_interactions():
    db = SessionLocal()

    try:
        interactions = db.query(Interaction).all()

        result = []

        for i in interactions:
            result.append({
                "id": i.id,
                "doctor_name": i.doctor_name,
                "date": i.date,
                "time": i.time,
                "interaction_type": i.interaction_type,
                "topics": i.topics,
                "sentiment": i.sentiment,
                "followup": i.followup
            })

        return result

    finally:
        db.close()