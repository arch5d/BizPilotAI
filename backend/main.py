"""
Entry point for BizPilotAI FastAPI application.
Sets up middleware, routers, and startup/shutdown events.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import API_HOST, API_PORT, CORS_ORIGINS
from database.db import connect_to_mongo, disconnect_from_mongo
from core.ai_client import initialize_ai, shutdown_ai

from routes.business_routes import router as business_router
from routes.report_routes import router as report_router
from routes.agent_routes import router as agent_router


app = FastAPI(title="BizPilotAI", version="1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    await initialize_ai()


@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_from_mongo()
    await shutdown_ai()


# include routers
app.include_router(business_router)
app.include_router(report_router)
app.include_router(agent_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
