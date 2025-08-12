from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from models.models import Answer, Vote, Question, Session as SessionModel
from database import get_session

router = APIRouter()

@router.get("/sessions/{session_code}/questions/{question_id}/results")
def get_results(*, db_session: Session = Depends(get_session), session_code: str, question_id: int):
    statement_session = select(SessionModel).where(SessionModel.code == session_code)
    session_obj = db_session.exec(statement_session).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session with this code not found")

    question = db_session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    vote_count_subquery = (
        select(Vote.answer_id, func.count(Vote.id).label("vote_count"))
        .where(Vote.question_id == question_id)
        .where(Vote.session_id == session_obj.id)
        .group_by(Vote.answer_id)
        .subquery()
    )

    statement = (
        select(Answer.id, Answer.text, func.coalesce(vote_count_subquery.c.vote_count, 0).label("votes"))
        .select_from(Answer)
        .join(vote_count_subquery, Answer.id == vote_count_subquery.c.answer_id, isouter=True)
        .where(Answer.question_id == question_id)
        .order_by(func.coalesce(vote_count_subquery.c.vote_count, 0).desc())
    )
    results = db_session.exec(statement).all()
    return [{"answer_id": r.id, "text": r.text, "votes": r.votes} for r in results]