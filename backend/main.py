from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI (
    title="Air Quality and Allergen Projection API",
    description="Backend service for ingesting, processing, and serving hyper-local environmental forecasts.",
    version="0.1.0"
) 

# 1. CORS Middleware
# Allows the Nuxt frontend (running on a different port/host) to communicate with this API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 2. Database Connection (Placeholder - actual connection logic will be in a separate file)
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("WARNING: DATABASE_URL environment variable is not set. Database operations will fail.")
else:
    print(f"INFO: Database connection string loaded: {DATABASE_URL[:20]}...")

# --- Routes ---
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Air Quality API is running. Check /health for detailed status."}

@app.get("/health", tags=['Health'])
async def health_check():
    """Detailed health check to verify service connectivity."""
    status = {
        "api_status":"UP",
        "database_connection":"PENDING_IMPLEMENTATION",
        "ingestion_scheduler":"PENDING_IMPLEMENTATION",
        "environment": os.environ.get("ENV", "development"),
    }
    return status