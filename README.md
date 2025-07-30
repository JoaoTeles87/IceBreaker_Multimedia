# IceBreaker Multimedia - MVP

IceBreaker Multimedia is an MVP (Minimum Viable Product) of a full-stack web application designed to facilitate interactive question-and-answer sessions, ideal for ice-breaking activities or simple quizzes. It features a FastAPI backend for managing game sessions, questions, answers, and votes, and a React frontend for a dynamic user interface.

## Features

- **Game Session Management**: Create unique game sessions that participants can join.
- **Anonymous Participation**: Participants can join and interact within sessions without needing to create user accounts.
- **Dynamic Question & Answer Flow**: Present questions and allow participants to submit answers.
- **Voting System**: Enable participants to vote on submitted answers.
- **Interactive Frontend**: A responsive and intuitive user interface built with React.
- **RESTful API**: Clean and well-documented API endpoints for seamless communication between frontend and backend.
- **Database Integration**: Uses SQLModel for ORM with a SQLite database (configurable).
- **CORS Enabled**: Configured for cross-origin resource sharing to allow frontend and backend to run on different ports.
- **Static File Serving**: Serves the React frontend build directly from the FastAPI backend.

## Technologies Used

### Backend
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLModel**: A library for interacting with SQL databases from Python code, with Python objects.
- **Pydantic**: Data validation and settings management using Python type hints.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **python-dotenv**: For managing environment variables.

### Frontend
- **React**: A JavaScript library for building user interfaces.
- **Vite**: A fast build tool that provides a lightning-fast development experience.
- **TypeScript**: A typed superset of JavaScript that compiles to plain JavaScript.
- **CSS**: For styling the application.

## Recent Adjustments & MVP Database Schema

To support the core MVP functionality, the following database tables and fields have been added/modified:

-   **`Session` Table**: Manages unique game sessions.
    -   `id`: Primary key.
    -   `code`: Unique session code for participants to join.
-   **`Vote` Table**: Records votes cast by participants on answers within a session.
    -   `id`: Primary key.
    -   `session_id`: Foreign key linking to the `Session` table.
    -   `question_id`: Foreign key linking to the `Question` table.
    -   `answer_id`: Foreign key linking to the `Answer` table.
    -   `participant_id`: A string field to store a unique identifier for anonymous participants (e.g., a UUID generated on the client-side). This allows tracking individual votes without requiring user accounts.

## Setup Instructions for Developers

Follow these steps to set up the project locally for development.

### Prerequisites

- Python 3.9+
- Node.js (LTS recommended)
- npm or Yarn

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/IceBreaker_Multimedia.git
cd IceBreaker_Multimedia
```

### 2. Backend Setup

Navigate to the `backend` directory, create a virtual environment, install dependencies, and set up environment variables.

```bash
cd backend
python -m venv venv
./venv/Scripts/activate  # On Windows
source venv/bin/activate # On macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory based on `.env.example`:

```
DATABASE_URL="sqlite:///./database.db"
```

### 3. Frontend Setup

Navigate to the `frontend` directory and install dependencies.

```bash
cd ../frontend
npm install # or yarn install
```

### 4. Running the Application

#### Start the Backend Server

From the `backend` directory:

```bash
./venv/Scripts/activate  # On Windows
source venv/bin/activate # On macOS/Linux
uvicorn main:app --reload
```

The backend server will run on `http://localhost:8000`.

#### Start the Frontend Development Server

From the `frontend` directory:

```bash
npm run dev # or yarn dev
```

The frontend development server will typically run on `http://localhost:5173`.

### 5. Building the Frontend for Production

To create a production build of the frontend that can be served by the FastAPI backend:

From the `frontend` directory:

```bash
npm run build # or yarn build
```

This will create a `dist` directory inside `frontend`, which the FastAPI application is configured to serve.

## Project Structure

```
IceBreaker_Multimedia/
├── backend/
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # Database models (SQLModel)
│   │   └── models.py
│   └── routes/             # API routes/endpoints
│       └── questions.py
├── frontend/
│   ├── public/             # Static assets
│   ├── src/                # React source code
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Application pages/views
│   │   └── App.tsx         # Main React component
│   ├── index.html          # Frontend entry point
│   ├── package.json        # Frontend dependencies and scripts
│   └── vite.config.ts      # Vite configuration
├── venv/                   # Python virtual environment
└── README.md               # Project documentation
```