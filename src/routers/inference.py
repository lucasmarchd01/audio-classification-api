from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import aiofiles
import os
from pathlib import Path
import logging
from ..utils.config import Settings
from ..models.model_loader import ModelManager

logger = logging.getLogger(__name__)
router = APIRouter()

# Get model manager from app state
def get_model_manager():
    from ..app import model_manager
    if not model_manager:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return model_manager

@router.post("/inference", response_model=dict)
async def predict_audio(
    file: UploadFile = File(...),
    model_manager: ModelManager = Depends(get_model_manager)
):
    """
    Classify music genre from uploaded audio file
    
    - **file**: Audio file (mp3, wav, flac, m4a)
    - Returns genre predictions with confidence scores
    """
    settings = Settings()
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_extension} not supported. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Read file content
    try:
        content = await file.read()
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Perform inference
        results = await model_manager.predict(content)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "filename": file.filename,
                "file_size": len(content),
                "results": results
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/batch-inference", response_model=dict)
async def batch_predict_audio(
    files: List[UploadFile] = File(...),
    model_manager: ModelManager = Depends(get_model_manager)
):
    """
    Batch classify multiple audio files
    
    - **files**: List of audio files
    - Returns list of predictions for each file
    """
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files per batch")
    
    results = []
    
    for file in files:
        try:
            content = await file.read()
            prediction = await model_manager.predict(content)
            
            results.append({
                "filename": file.filename,
                "status": "success",
                "results": prediction
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "error": str(e)
            })
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "batch_size": len(files),
            "results": results
        }
    )

@router.get("/models/info")
async def get_model_info():
    """Get information about the loaded model"""
    settings = Settings()
    return {
        "model_name": settings.MODEL_NAME,
        "device": settings.DEVICE,
        "supported_formats": settings.ALLOWED_EXTENSIONS,
        "max_file_size_mb": settings.MAX_FILE_SIZE / 1024 / 1024
    }