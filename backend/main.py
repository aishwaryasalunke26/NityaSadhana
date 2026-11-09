
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import engine

from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router
from app.routers.japa import router as japa_router
from app.routers.reading import router as reading_router
from app.routers.seva import router as seva_router

app = FastAPI(
    title="NityaSadhana API",
    description="ISKCON Sadhana Report Management System",
    version="1.0.0"
)


# Frontend connection
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


# Authentication routes
app.include_router(auth_router)

# Devotee profile routes
app.include_router(profile_router)

# Japa tracking routes
app.include_router(japa_router)

app.include_router(reading_router)

app.include_router(seva_router)


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


@app.get("/api/models-health")
def models_health():
    try:
        tables = inspect(engine).get_table_names()

        expected_tables = [
            "users",
            "devotee_profiles",
            "japa_records",
            "book_reading",
            "hearing_records",
            "seva_records",
            "daily_reports",
        ]

        found_tables = [
            table for table in expected_tables
            if table in tables
        ]

        return {
            "status": "success" if len(found_tables) == 7 else "incomplete",
            "models_registered": 7,
            "tables_found": len(found_tables),
            "tables": found_tables,
            "message": "NityaSadhana database models verification completed"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database model verification failed"
        )
