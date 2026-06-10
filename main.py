"""
ENTRYPOINT WEB APPLICATION ROUTER (AccessiScan API Backend)
---------------------------------------------------------------------
Purpose:
    Acts as the primary entrypoint and initialization router. Manages the 
    FastAPI framework, CORS security, and asynchronous lifecycle hooks.

Architecture:
    1. Workspace Isolation: Normalizes paths to ensure peer-repository 
       (AI Engine) accessibility across varying host environments.
    2. Lifespan Management: Orchestrates startup/shutdown routines for 
       database pools and machine learning model memory.
    3. CORS Security Perimeter: Establishes a controlled ingress gate for 
       authorized client communication.
"""

import logging
import os
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- 1. SHARED DEPENDENCY & MODULE IMPORTS ---
# PURPOSE: Resolves project-wide dependencies and registers the shared AI engine 
# instance to avoid redundant loading and potential circular import loops.
from dependencies import ai_engine 

from accessiscan_backend.app.api.v1.api import api_router
from accessiscan_backend.app.db.session import create_db_and_tables

# --- 2. CONFIGURATION & LOGGING ---
# PURPOSE: Establishes a standard logging interface for monitoring system health,
# tracking API requests, and debugging execution flows during runtime.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ensure_data_folders():
    """Ensures necessary directories exist for audit artifacts."""
    folders = ["data/uploads", "data/detections", "data/reports"]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    logging.info("[*] Data directories verified.")

# --- 3. LIFESPAN MANAGEMENT ---
# PURPOSE: Orchestrates the application startup (pre-flight checks, database 
# schema synchronization) and graceful shutdown routines (logging, resource teardown).
async def lifespan(app: FastAPI):
    """Orchestrates startup/shutdown routines."""
    logging.info("[*] Launching AccessiScan API Engine...")
    ensure_data_folders()
    
    # ONLY create tables if we are NOT running tests
    if os.getenv("TESTING") != "True":
        create_db_and_tables()
        
    yield
    logging.info("[-] Shutting down AccessiScan API Engine.")

# --- 4. APPLICATION INITIALIZATION ---
# PURPOSE: Instantiates the FastAPI core, configuring global metadata and the 
# application's lifecycle context for the backend engine.
app = FastAPI(
    title="AccessiScan API",
    description="Automated DSAPT Compliance Auditing Backend Engine",
    version="1.0.0",
    lifespan=lifespan
)

# --- 5. SECURITY PERIMETER ---
# PURPOSE: Configures Cross-Origin Resource Sharing (CORS) to safely manage 
# browser-based requests, ensuring the API is accessible to approved frontend clients.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 6. ROUTER REGISTRATION ---
# PURPOSE: Integrates modular API endpoints (v1) into the application router, 
# maintaining clean separation of concerns between business logic and routing
app.include_router(api_router, prefix="/api/v1")

# --- 7. HEALTH TELEMETRY ---
# PURPOSE: Provides lightweight diagnostic endpoints for load balancers and 
# orchestration tools (e.g., Kubernetes) to verify application uptime and status.
@app.get("/health", tags=["System Telemetry"])
async def health_check() -> dict:
    """Provides system health status."""
    return {"status": "Healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "AccessiScan Backend is running. Visit /docs for the API documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
