from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import cgm, health
from app.core.config import settings

app = FastAPI(
    title="Loopy API",
    description="CGM Data Access API for DIY Diabetes Monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(cgm.router, prefix="/api/cgm", tags=["cgm"])

@app.get("/")
async def root():
    return {
        "message": "Loopy API - CGM Data Access Service",
        "status": "running",
        "docs": "/docs"
    }