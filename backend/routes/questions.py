from fastapi import APIRouter, HTTPException
from typing import List
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