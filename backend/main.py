from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from contextlib import asynccontextmanager # New Import

# Import the database logic and routers (routers will be added next)
from .database import init_db, get_db
from .tasks import start_ingestion_scheduler, stop_ingestion_scheduler
from .routers import forecast

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events. 
    This replaces the deprecated @app.on_event("startup/shutdown").
    """
    print("INFO: Application Startup initiated.")
    
    # 1. Startup Logic
    init_db() 
    start_ingestion_scheduler()

    yield 

    print("INFO: Application Shutdown initiated.")
    stop_ingestion_scheduler()


# Initialize FastAPI application
# Pass the new lifespan handler to the FastAPI constructor
app = FastAPI(
    title="Air Quality & Allergen Projection API",
    description="Backend service for ingesting, processing, and serving hyper-local environmental forecasts.",
    version="0.1.0",
    lifespan=lifespan 
)

# --- Configuration ---

# CORS Middleware 
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(forecast.router, prefix="/api", tags=["Forecast"])
# --- Routes ---
# The health check route remains the same, confirming the DB connection is still active via the dependency.

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Air Quality API is running. Check /health for detailed status."}

@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Detailed health check to verify service connectivity, including the database.
    """
    db_status = "DOWN"
    try:
        db.execute(text("SELECT 1"))
        db_status = "UP"
    except Exception as e:
        print(f"Database health check failed: {e}")
        db_status = f"DOWN ({type(e).__name__})"
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

    return {
        "api_status": "UP",
        "database_connection": db_status,
        "ingestion_scheduler": "PENDING_IMPLEMENTATION",
        "environment": os.environ.get("ENV", "development")
    }