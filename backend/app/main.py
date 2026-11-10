
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    dashboard,
    hearing,
    japa,
    profile,
    reading,
    reports,
    seva,
    summary,
)

app = FastAPI(
    title="NityaSadhana API",
    description="ISKCON Sadhana Report Management System",
    version="1.0.0"
)

# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HOME
@app.get("/")
def home():
    return {
        "message": "Welcome to NityaSadhana Backend",
        "status": "Running"
    }

# HEALTH CHECK
@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "NityaSadhana API is working properly"
    }

# REGISTER ALL API ROUTERS
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(japa.router)
app.include_router(reading.router)
app.include_router(hearing.router)
app.include_router(profile.router)
app.include_router(reports.router)
app.include_router(seva.router)
app.include_router(summary.router)
