# BizPilot AI

AI Business Operating System - Run AI agents to analyze business data and generate reports.

## Project Structure

```
bizpilot-ai/
├── backend/          # FastAPI + CrewAI backend
├── frontend/         # Next.js 14 dashboard
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key (for CrewAI agents)

---

## Step-by-Step Setup

### 1. Install Backend Dependencies

```bash
cd bizpilot-ai/backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# From bizpilot-ai/ root
cp .env.example .env

# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the Backend

```bash
cd bizpilot-ai/backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 4. Create & Run the Frontend

```bash
cd bizpilot-ai/frontend
npm install
npm run dev
```

- Dashboard: http://localhost:3000

### 5. Use the Dashboard

1. Open http://localhost:3000
2. Click **Run Marketing Agent**
3. Wait for the agent to generate a report (uses CrewAI + OpenAI)
4. View reports in the Reports section

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /agents/run/marketing | Run Marketing Trend Agent |
| GET | /reports | List all reports |

---

## Adding New Agents

1. Create agent in `backend/agents/` extending `BaseAgent`
2. Register in `backend/orchestrator/orchestrator.py` (`AGENT_REGISTRY`)
3. Add API route in `backend/api/routes.py`
4. Add UI in frontend

---

## Tech Stack

**Backend:** Python 3.11, FastAPI, CrewAI, SQLAlchemy, SQLite (PostgreSQL-ready)

**Frontend:** Next.js 14, React, TailwindCSS
