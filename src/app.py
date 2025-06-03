from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager
from .models.model_loader import ModelManager
from .routers import inference, health
from .utils.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model manager
model_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model_manager
    settings = Settings()
    model_manager = ModelManager(settings.MODEL_NAME, settings.DEVICE)
    await model_manager.load_model()
    logger.info(f"Model {settings.MODEL_NAME} loaded successfully")
    
    yield
    
    # Shutdown
    if model_manager:
        model_manager.cleanup()
        logger.info("Model cleaned up")

app = FastAPI(
    title="HuggingFace Music Inference API",
    description="A scalable inference server for music genre classification using HuggingFace models",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(inference.router, prefix="/api/v1", dependencies=[])

@app.get("/")
async def root():
    return {
        "message": "HuggingFace Music Inference API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        workers=1,  # Single worker due to model loading
        reload=False
    )