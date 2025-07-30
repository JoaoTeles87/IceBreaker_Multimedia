from sqlmodel import SQLModel, Field
from typing import Optional

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    category: str
    difficulty: str

class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    text: str
    is_correct: bool

class Session(SQLModel, table=True):
    __tablename__ = "sessions"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)

class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="sessions.id")
    question_id: int = Field(foreign_key="question.id")
    answer_id: int = Field(foreign_key="answer.id")
    participant_id: str # New field for anonymous participant tracking
