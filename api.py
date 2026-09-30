import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from routes.analysis_routes import router as analysis_router
from routes.resume_routes import router as resume_router

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Depends,
)


load_dotenv()

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


# FastAPI App

app = FastAPI(
    title="AI Resume Intelligence Platform",
    description=(
        "An explainable AI-powered Resume Intelligence Platform"
        "that evaluates Resume Quality, ATS Friendliness"
        "and Resume-JD Matching."
    ),
    version="1.0.0",
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    analysis_router,
    prefix="/api/v1"
)

app.include_router(
    resume_router,
    prefix="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Constants

SUPPORTED_ROLES = {
    "backend",
    "frontend",
    "software_engineer",
    "ml_engineer",
}


# Root Endpoint

@app.get("/")
def root():

    return {
        "application": "AI Resume Intelligence Platform",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }