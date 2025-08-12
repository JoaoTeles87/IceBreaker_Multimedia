from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter()

# Mock questions — later will come from the database
questions = [
    {"id": 1, "text": "What is the capital of France?", "category": "Geography", "difficulty": "Easy", "correct_answer": "Paris"},
    {"id": 2, "text": "Who painted the Mona Lisa?", "category": "Art", "difficulty": "Medium", "correct_answer": "Leonardo da Vinci"},
    {"id": 3, "text": "What is the chemical symbol for water?", "category": "Science", "difficulty": "Easy", "correct_answer": "H2O"},
]

# Model for receiving player's answer
class SubmitAnswerBody(BaseModel):
    player: str
    question_id: int
    answer: str

@router.get("/random")
def get_random_question():
    # In the future: fetch from the database instead of a fixed list
    q = random.choice(questions)
    return {k: q[k] for k in q if k != "correct_answer"}  # do not send the correct answer to the player

@router.post("/submit")
def submit_answer(body: SubmitAnswerBody):
    question = next((q for q in questions if q["id"] == body.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    is_correct = (body.answer.strip().lower() == question["correct_answer"].strip().lower())
    return {"question_id": body.question_id, "player": body.player, "is_correct": is_correct}
