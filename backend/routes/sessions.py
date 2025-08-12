from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
import os, uuid, random, string

from models.models import Session as SessionModel, Participant
from sqlmodel import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL, echo=True)

router = APIRouter()

def generate_code(n=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

class CreateSessionBody(BaseModel):
    hostName: str

class JoinBody(BaseModel):
    name: str

@router.post("", status_code=201)
def create_session(body: CreateSessionBody):
    code = generate_code()
    with Session(engine) as db:
        while db.exec(select(SessionModel).where(SessionModel.code == code)).first():
            code = generate_code()

        session = SessionModel(code=code, started=False)
        db.add(session)
        db.commit()
        db.refresh(session)

        participant_uuid = str(uuid.uuid4())
        host = Participant(session_id=session.id, name=body.hostName, participant_uuid=participant_uuid)
        db.add(host)
        db.commit()

        return {"id": session.id, "code": session.code, "participant_id": participant_uuid}

@router.post("/{code}/join")
def join_session(code: str, body: JoinBody):
    with Session(engine) as db:
        session_obj = db.exec(select(SessionModel).where(SessionModel.code == code)).first()
        if not session_obj:
            raise HTTPException(status_code=404, detail="Session not found")
        participant_uuid = str(uuid.uuid4())
        participant = Participant(session_id=session_obj.id, name=body.name, participant_uuid=participant_uuid)
        db.add(participant)
        db.commit()
        players = db.exec(select(Participant).where(Participant.session_id == session_obj.id)).all()
        player_names = [p.name for p in players]
        return {"sessionId": session_obj.id, "code": session_obj.code, "players": player_names, "participant_id": participant_uuid}

@router.get("/{session_id}/players")
def list_players(session_id: int):
    with Session(engine) as db:
        session_obj = db.get(SessionModel, session_id)
        if not session_obj:
            raise HTTPException(status_code=404, detail="Session not found")
        players = db.exec(select(Participant).where(Participant.session_id == session_id)).all()
        return {"players": [p.name for p in players]}

@router.post("/{session_id}/start")
def start_session(session_id: int):
    with Session(engine) as db:
        session_obj = db.get(SessionModel, session_id)
        if not session_obj:
            raise HTTPException(status_code=404, detail="Session not found")
        session_obj.started = True
        db.add(session_obj)
        db.commit()
        return {"ok": True, "started": True}
