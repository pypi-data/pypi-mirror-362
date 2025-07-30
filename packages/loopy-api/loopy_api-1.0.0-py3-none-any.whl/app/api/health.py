from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "loopy-api",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint for monitoring."""
    return {"message": "pong"}