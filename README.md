# BizPilot AI

AI Business Operating System - Run AI agents to analyze business data and generate reports.

## Project Structure

bizpilot-ai/
├── backend/          # FastAPI + CrewAI backend
├── frontend/         # Next.js 14 dashboard
├── .env.example
└── README.md

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key (for CrewAI agents)

## Step-by-Step Setup

### 1. Install Backend Dependencies

cd bizpilot-ai/backend  
pip install -r requirements.txt  

### 2. Configure Environment

cp .env.example .env  
Add your OPENAI_API_KEY  

### 3. Run the Backend

cd bizpilot-ai/backend  
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000  

### 4. Run Frontend

cd bizpilot-ai/frontend  
npm install  
npm run dev  

## Tech Stack

Backend: FastAPI, CrewAI  
Frontend: Next.js, TailwindCSS