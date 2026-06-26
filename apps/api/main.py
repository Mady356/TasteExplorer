"""
TasteExplorer API - FastAPI application entry point.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Load environment variables - try apps/api/.env first, then root .env
api_env_path = Path(__file__).parent / '.env'
root_env_path = Path(__file__).parent.parent.parent / '.env'

if api_env_path.exists():
    load_dotenv(api_env_path)
    logger = logging.getLogger(__name__)
    print(f"Loaded environment from: {api_env_path}")
elif root_env_path.exists():
    load_dotenv(root_env_path)
    logger = logging.getLogger(__name__)
    print(f"Loaded environment from: {root_env_path}")
else:
    # Try loading from current directory
    load_dotenv()
    print("Loaded environment from current directory or system env")

from database.database import init_db
from auth.routes import router as auth_router
from user.routes import router as user_router
from spotify.routes import router as spotify_router
from demo.routes import router as demo_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting TasteExplorer API")
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down TasteExplorer API")


# Create FastAPI app
app = FastAPI(
    title="TasteExplorer API",
    description="Intelligent music discovery platform powered by custom graph-based recommendations",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware - allow frontend to connect
# In production, set CORS_ORIGINS env var to your deployed frontend URL
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
logger.info(f"CORS enabled for origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(spotify_router, prefix="/spotify", tags=["spotify"])
app.include_router(demo_router, prefix="/demo", tags=["demo"])


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "name": "TasteExplorer API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """
    Health check endpoint.

    Used by deployment platforms (Render, Railway, etc.) to verify service health.
    """
    return {
        "status": "healthy",
        "service": "tasteexplorer-api",
        "version": "0.1.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
