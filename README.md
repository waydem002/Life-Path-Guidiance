# Life Path Guidance

Life Path Guidance is a web app for exploring numerology-inspired personal profiles and conversational guidance. Enter birth and name details to calculate core numerology numbers and request an AI-generated reading, or ask questions in the chat. Readings can be generated in English, Spanish, French, or German and exported as PDFs.

The app is presented as a reflective self-discovery tool. Its readings are interpretive and are not a substitute for professional medical, mental-health, financial, or other advice.

## Features

- Calculate Life Path, Expression, Soul Urge, Personality, and Birthday numbers.
- Generate a personalized reading with a focus such as career, relationships, personal growth, or health and energy.
- Chat with an AI guidance assistant and choose a response language.
- Export a generated reading as a PDF blueprint.
- Cache generated readings locally in SQLite.

## Technology

- **Frontend:** React, Vite, Tailwind CSS, and Lucide icons
- **Backend:** Python, FastAPI, and SQLite
- **AI:** Groq API
- **PDF export:** ReportLab

## Requirements

- Python 3.10 or later
- Node.js and npm
- A Groq API key

## Run locally

Run the backend and frontend in separate terminals from the project directory.

### 1. Configure the backend

In PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create `backend\.env` and add your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Keep this key private. `.env` files are excluded from Git.

Start the API from the `backend` directory:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI's interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Start the frontend

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open the local URL printed by Vite (by default, [http://localhost:5173](http://localhost:5173)).

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/energy-profile` | Generate or retrieve a cached profile reading |
| `POST` | `/api/generate-profile` | Alias for profile generation |
| `POST` | `/api/chat-sandbox` | Send a message to the guidance chatbot |
| `GET` | `/api/profiles-history` | Retrieve recent cached profile details |
| `GET` | `/api/download-blueprint` | Download a PDF for a cached profile |

## Local data and reference material

The backend creates its SQLite profile cache at `backend/profiles.db` when it starts. This database and generated PDF exports are local runtime data and are not tracked by Git.

Optional `.txt`, `.md`, or `.pdf` reference documents placed in `backend/data` are used as context for AI responses. PDF extraction is limited to the first 10 pages, and the combined reference context is capped at 8,000 characters. Do not add documents unless you have permission to use them.

## Development

Run the frontend linter and production build from `frontend`:

```powershell
npm run lint
npm run build
```

The frontend currently calls the backend at `http://localhost:8000`; the backend allows browser requests from `http://localhost:5173`.
