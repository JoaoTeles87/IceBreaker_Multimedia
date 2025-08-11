from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models.database import create_db_and_tables
from models.models import Question, Answer, Session, Vote # Import models
from routes import questions, votes # Import routes


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
frontend_dist_path = os.path.join(BASE_DIR, "frontend", "dist")
print(f"Frontend dist path: {frontend_dist_path}")


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(votes.router, prefix="/votes", tags=["votes"])

app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="frontend")