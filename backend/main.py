
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import engine, DB_NAME

app = FastAPI(
    title="NityaSadhana API",
    description="ISKCON Sadhana Report Management System",
    version="1.0.0"
)

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


@app.get("/")
def home():
    return {
        "message": "Welcome to NityaSadhana Backend",
        "status": "Running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "NityaSadhana API is working properly"
    }


@app.get("/api/db-health")
def database_health_check():
    try:
        with engine.connect() as connection:
            database_name = connection.execute(
                text("SELECT DATABASE()")
            ).scalar()

        return {
            "status": "connected",
            "database": database_name,
            "message": "MySQL connection successful"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="MySQL connection failed. Check database configuration."
        )
