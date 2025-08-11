from sqlmodel import Session, select
from models.models import Vote
from typing import List, Optional
from fastapi import HTTPException

def get_votes_by_session_and_question(
    session_id: int, 
    question_id: int,
    engine
) -> List[Vote]:
    """
    Busca todos os votos de uma determinada sessão e questão
    """
    try:
        with Session(engine) as session:
            statement = select(Vote).where(
                Vote.session_id == session_id,
                Vote.question_id == question_id
            )
            votes = session.exec(statement).all()
            return votes
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao buscar votos: {str(e)}"
        )

def get_vote_count_by_answer(
    session_id: int,
    question_id: int,
    engine
) -> dict:
    """
    Retorna a contagem de votos por resposta para uma sessão e questão específicas
    """
    try:
        with Session(engine) as session:
            statement = select(Vote).where(
                Vote.session_id == session_id,
                Vote.question_id == question_id
            )
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
    participant_id: str,
    engine
) -> Vote:
    """
    Cria um novo voto
    """
    try:
        with Session(engine) as session:
            vote = Vote(
                session_id=session_id,
                question_id=question_id,
                answer_id=answer_id,
                participant_id=participant_id
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
