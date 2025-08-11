from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.services.votes_services import get_votes_by_session_and_question, get_vote_count_by_answer, create_vote
from models.models import Vote
import random

router = APIRouter()

@router.get("/votes")
def get_votes(
    session_id: int = Query(..., description="ID da sessão"),
    question_id: int = Query(..., description="ID da questão")
):
    """
    Busca todos os votos de uma determinada sessão e questão
    """
    votes = get_votes_by_session_and_question(session_id, question_id)
    return votes

@router.get("/votes/count")
def get_vote_counts(
    session_id: int = Query(..., description="ID da sessão"),
    question_id: int = Query(..., description="ID da questão")
):
    """
    Retorna a contagem de votos por resposta para uma sessão e questão específicas
    """
    vote_counts = get_vote_count_by_answer(session_id, question_id)
    return vote_counts

@router.post("/votes")
def create_new_vote(
    session_id: int = Query(..., description="ID da sessão"),
    question_id: int = Query(..., description="ID da questão"),
    answer_id: int = Query(..., description="ID da resposta"),
    participant_id: str = Query(..., description="ID do participante")
):
    """
    Cria um novo voto
    """
    vote = create_vote(session_id, question_id, answer_id, participant_id)
    return vote