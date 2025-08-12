from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from models.models import Question
from database import get_session
import random

router = APIRouter()

@router.get("/random")
def get_random_question():
    # This is a mock question generator. Replace with actual database query or external API call.
    questions = [
        {"id": 1, "text": "What is the capital of France?", "category": "Geography", "difficulty": "Easy"},
        {"id": 2, "text": "Who painted the Mona Lisa?", "category": "Art", "difficulty": "Medium"},
        {"id": 3, "text": "What is the chemical symbol for water?", "category": "Science", "difficulty": "Easy"},
    ]
    return random.choice(questions)

@router.get("/questions/", response_model=List[Question])
def list_questions(db_session: Session = Depends(get_session)):
    questions = db_session.exec(select(Question)).all()
    return questions

@router.post("/questions/", response_model=Question)
def create_question(question: Question, db_session: Session = Depends(get_session)):
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    return question