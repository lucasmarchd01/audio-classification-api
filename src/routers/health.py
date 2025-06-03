from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import psutil
import torch
from datetime import datetime
from ..models.model_loader import ModelManager

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "HuggingFace Music Inference API"
        }
    )

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": cpu_percent,
            "memory": {
                "total_gb": round(memory.total / 1024**3, 2),
                "available_gb": round(memory.available / 1024**3, 2),
                "percent_used": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / 1024**3, 2),
                "free_gb": round(disk.free / 1024**3, 2),
                "percent_used": round((disk.used / disk.total) * 100, 2)
            }
        }
    }
    
    # GPU info if available
    if torch.cuda.is_available():
        health_data["gpu"] = {
            "available": True,
            "device_count": torch.cuda.device_count(),
            "current_device": torch.cuda.current_device(),
            "device_name": torch.cuda.get_device_name(0),
            "memory_allocated_mb": round(torch.cuda.memory_allocated(0) / 1024**2, 2),
            "memory_cached_mb": round(torch.cuda.memory_reserved(0) / 1024**2, 2)
        }
    else:
        health_data["gpu"] = {"available": False}
    
    return JSONResponse(status_code=200, content=health_data)

@router.get("/ready")
async def readiness_check():
    """Kubernetes-style readiness probe"""
    try:
        from ..app import model_manager
        if model_manager and model_manager.model:
            return JSONResponse(
                status_code=200,
                content={"status": "ready", "model_loaded": True}
            )
        else:
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "model_loaded": False}
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "error": str(e)}
        )