from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
import datetime

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    # Adicionando relacionamentos para facilitar a navegação
    questions: list["Question"] = Relationship(back_populates="session")
    votes: list["Vote"] = Relationship(back_populates="session")

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    session_id: int = Field(foreign_key="session.id")
    session: Session = Relationship(back_populates="questions")
    answers: list["Answer"] = Relationship(back_populates="question")
    votes: list["Vote"] = Relationship(back_populates="question")

class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    question_id: int = Field(foreign_key="question.id")
    question: Question = Relationship(back_populates="answers")
    votes: list["Vote"] = Relationship(back_populates="answer")

class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: str # Identificador anônimo do cliente
    date_: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    session_id: int = Field(foreign_key="session.id")
    question_id: int = Field(foreign_key="question.id")
    answer_id: int = Field(foreign_key="answer.id")
    session: Session = Relationship(back_populates="votes")
    question: Question = Relationship(back_populates="votes")
    answer: Answer = Relationship(back_populates="votes")