from sqlmodel import Session, select
from models.models import Vote
from models.database import get_engine
from typing import List, Optional
from fastapi import HTTPException
from datetime import datetime

def get_votes_by_session_and_question(
    session_id: int, 
    question_id: int
) -> List[Vote]:
    """
    Busca todos os votos de uma determinada sessão e questão
    """
    try:
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Vote).where(
                Vote.session_id == session_id,
                Vote.question_id == question_id
            ).order_by(Vote.date_)
            votes = session.exec(statement).all()
            return votes
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao buscar votos: {str(e)}"
        )

def get_vote_count_by_answer(
    session_id: int,
    question_id: int
) -> dict:
    """
    Retorna a contagem de votos por resposta para uma sessão e questão específicas
    """
    try:
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Vote).where(
                Vote.session_id == session_id,
                Vote.question_id == question_id
            ).order_by(Vote.date_)
            votes = session.exec(statement).all()
            
            # Conta votos por answer_id
            vote_counts = {}
            for vote in votes:
                answer_id = vote.answer_id
                if answer_id in vote_counts:
                    vote_counts[answer_id] += 1
                else:
                    vote_counts[answer_id] = 1
                    
            return vote_counts
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao contar votos: {str(e)}"
        )

def create_vote(
    session_id: int,
    question_id: int,
    answer_id: int,
    participant_id: str
) -> Vote:
    """
    Cria um novo voto
    """
    try:
        engine = get_engine()
        with Session(engine) as session:
            vote = Vote(
                session_id=session_id,
                question_id=question_id,
                answer_id=answer_id,
                participant_id=participant_id,
                date_=datetime.utcnow()
            )
            session.add(vote)
            session.commit()
            session.refresh(vote)
            return vote
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar voto: {str(e)}"
        )

def get_all_votes_by_session_grouped_by_question(
    session_id: int
) -> dict:
    """
    Retorna todos os votos de uma sessão, agrupados por questão e ordenados por data
    """
    try:
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Vote).where(
                Vote.session_id == session_id
            ).order_by(Vote.date_)
            
            votes = session.exec(statement).all()
            
            # Agrupa votos por question_id
            grouped_votes = {}
            for vote in votes:
                question_id = vote.question_id
                if question_id not in grouped_votes:
                    grouped_votes[question_id] = []
                grouped_votes[question_id].append(vote)
                    
            return grouped_votes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar votos da sessão: {str(e)}"
        )
