import random
import string
from fastapi import APIRouter, Depends
from sqlmodel import Session as SQLModelSession
from models.models import Session
from database import get_session

router = APIRouter()

def generate_session_code(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

@router.post("/sessions/", response_model=Session)
def create_session(db_session: SQLModelSession = Depends(get_session)):
    while True:
        code = generate_session_code()
        existing_session = db_session.query(Session).filter(Session.code == code).first()
        if not existing_session:
            break
    new_session = Session(code=code)
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)
    return new_session