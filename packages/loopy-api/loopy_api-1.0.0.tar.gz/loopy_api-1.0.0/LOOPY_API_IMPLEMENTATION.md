# Loopy API - Backend Implementation Guide

## Overview

**loopy-api** is a FastAPI-based backend service that provides a REST API for accessing CGM (Continuous Glucose Monitor) data from a MongoDB database. Built on the `loopy-basic` package, it's designed for DIY diabetes monitoring setups.

## Architecture

### Key Features
- ✅ **FastAPI Framework** - Modern, fast web framework with automatic API documentation
- ✅ **MongoDB Integration** - Uses loopy-basic package for data access
- ✅ **Environment Configuration** - MongoDB credentials via environment variables
- ✅ **Type Safety** - Full type hints and Pydantic models
- ✅ **Docker Ready** - Container deployment with minimal configuration
- ✅ **CORS Enabled** - Frontend integration ready

### Repository Structure

```
loopy-api/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── cgm.py            # CGM data endpoints
│   │   └── health.py         # Health check endpoints
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py         # Environment configuration
│   │   └── cors.py           # CORS settings
│   ├── models/                # Pydantic response models
│   │   ├── __init__.py
│   │   └── cgm.py            # CGM data models
│   └── services/              # Business logic
│       ├── __init__.py
│       └── cgm_service.py    # Uses loopy-basic package
├── Dockerfile
├── docker-compose.yml
├── .env.example              # Example environment variables
└── README.md                 # Setup instructions
```

## Implementation Steps

### Phase 1: Project Setup

#### 1.1 Create Repository Structure
```bash
# Create new repository
git init loopy-api
cd loopy-api

# Create directory structure
mkdir -p app/{api,core,models,services}
touch app/__init__.py app/main.py
touch app/api/{__init__.py,cgm.py,health.py}
touch app/core/{__init__.py,config.py,cors.py}
touch app/models/{__init__.py,cgm.py}
touch app/services/{__init__.py,cgm_service.py}
```

#### 1.2 Install Dependencies
```bash
# Add dependencies using uv
uv add fastapi uvicorn loopy-basic python-dotenv pydantic-settings

# Or install from PyPI once loopy-basic is published:
# uv add fastapi uvicorn loopy-basic python-dotenv pydantic-settings
```

### Phase 2: Core Implementation

#### 2.1 Main FastAPI Application

**app/main.py**
```python
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
```

#### 2.2 Configuration Management

**app/core/config.py**
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # MongoDB connection (from environment variables)
    mongodb_username: str
    mongodb_password: str  
    mongodb_uri: str
    mongodb_database: str = "myCGMitc"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    
    # CORS settings
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

#### 2.3 CGM Service Layer

**app/services/cgm_service.py**
```python
from loopy.data.cgm import CGMDataAccess
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class CGMService:
    """Service layer for CGM data access using loopy-basic package."""
    
    @staticmethod
    def get_cgm_data(hours: int = 24) -> Dict[str, Any]:
        """Get recent CGM data using environment-configured MongoDB connection.
        
        Args:
            hours: Number of hours of data to retrieve (1-168)
            
        Returns:
            dict: CGM data with readings, analysis, and metadata
        """
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
            
            # Use loopy-basic with context manager for automatic connection handling
            with CGMDataAccess() as cgm:
                df = cgm.get_dataframe_for_period('custom', start_time, end_time)
                
                if df.empty:
                    return {
                        "data": [],
                        "analysis": None,
                        "message": f"No data found for the last {hours} hours",
                        "last_updated": datetime.now().isoformat(),
                        "time_range": {
                            "start": start_time.isoformat(),
                            "end": end_time.isoformat(),
                            "hours": hours
                        }
                    }
                
                # Perform analysis
                analysis = cgm.analyze_dataframe(df)
                
                # Convert DataFrame to JSON-serializable format
                data_records = df.to_dict('records')
                
                # Convert datetime objects to strings for JSON serialization
                for record in data_records:
                    if 'datetime' in record:
                        record['datetime'] = record['datetime'].isoformat()
                    if 'date_only' in record:
                        record['date_only'] = str(record['date_only'])
                
                return {
                    "data": data_records,
                    "analysis": analysis,
                    "last_updated": datetime.now().isoformat(),
                    "time_range": {
                        "start": start_time.isoformat(),
                        "end": end_time.isoformat(),
                        "hours": hours
                    }
                }
                
        except Exception as e:
            logger.error(f"Error retrieving CGM data: {e}")
            raise
    
    @staticmethod
    def get_current_glucose() -> Dict[str, Any]:
        """Get the most recent glucose reading.
        
        Returns:
            dict: Current glucose data with timestamp and trend information
        """
        try:
            with CGMDataAccess() as cgm:
                recent_readings = cgm.get_recent_readings(limit=1)
                
                if not recent_readings:
                    return {
                        "current_glucose": None, 
                        "message": "No recent data available"
                    }
                
                latest = recent_readings[0]
                timestamp_str = latest.get('dateString', '')
                
                # Calculate minutes since last reading
                if timestamp_str:
                    try:
                        # Handle timezone in dateString
                        timestamp_str_clean = timestamp_str.replace('Z', '+00:00')
                        latest_time = datetime.fromisoformat(timestamp_str_clean)
                        minutes_ago = (datetime.now().replace(tzinfo=latest_time.tzinfo) - latest_time).total_seconds() / 60
                    except:
                        minutes_ago = None
                else:
                    minutes_ago = None
                
                return {
                    "current_glucose": latest.get('sgv'),
                    "direction": latest.get('direction'),
                    "trend": latest.get('trend'),
                    "timestamp": timestamp_str,
                    "minutes_ago": round(minutes_ago, 1) if minutes_ago is not None else None,
                    "device": latest.get('device'),
                    "type": latest.get('type')
                }
                
        except Exception as e:
            logger.error(f"Error retrieving current glucose: {e}")
            raise
    
    @staticmethod
    def get_data_status() -> Dict[str, Any]:
        """Get data availability and connection status.
        
        Returns:
            dict: Status information about data availability
        """
        try:
            # Quick check with last hour of data
            result = CGMService.get_cgm_data(hours=1)
            data_count = len(result.get("data", []))
            
            return {
                "status": "connected" if data_count > 0 else "no_recent_data",
                "last_reading_count": data_count,
                "message": result.get("message", "Data available"),
                "last_updated": result.get("last_updated")
            }
            
        except Exception as e:
            logger.error(f"Error checking data status: {e}")
            return {
                "status": "error",
                "message": str(e),
                "last_updated": datetime.now().isoformat()
            }
```

#### 2.4 API Endpoints

**app/api/cgm.py**
```python
from fastapi import APIRouter, HTTPException, Query
from app.services.cgm_service import CGMService
from typing import Dict, Any

router = APIRouter()

@router.get("/data")
async def get_cgm_data(
    hours: int = Query(24, ge=1, le=168, description="Hours of data to retrieve (1-168)")
) -> Dict[str, Any]:
    """Get CGM data for the specified number of hours.
    
    Args:
        hours: Number of hours of data to retrieve (max 7 days)
        
    Returns:
        CGM data with readings, analysis, and metadata
    """
    try:
        return CGMService.get_cgm_data(hours=hours)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving CGM data: {str(e)}"
        )

@router.get("/current")
async def get_current_glucose() -> Dict[str, Any]:
    """Get the most recent glucose reading.
    
    Returns:
        Current glucose reading with trend information
    """
    try:
        return CGMService.get_current_glucose()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving current glucose: {str(e)}"
        )

@router.get("/status")
async def get_data_status() -> Dict[str, Any]:
    """Get data availability and connection status.
    
    Returns:
        Status information about data availability and connection health
    """
    try:
        return CGMService.get_data_status()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error checking data status: {str(e)}"
        )

@router.get("/analysis/{period}")
async def get_analysis(
    period: str = Query(..., regex="^(24h|week|month)$", description="Analysis period")
) -> Dict[str, Any]:
    """Get analysis for a specific time period.
    
    Args:
        period: Analysis period (24h, week, or month)
        
    Returns:
        Analysis data for the specified period
    """
    try:
        hours_map = {"24h": 24, "week": 168, "month": 720}
        hours = hours_map.get(period, 24)
        
        result = CGMService.get_cgm_data(hours=hours)
        
        return {
            "period": period,
            "analysis": result.get("analysis"),
            "data_points": len(result.get("data", [])),
            "time_range": result.get("time_range"),
            "last_updated": result.get("last_updated")
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error performing analysis: {str(e)}"
        )
```

**app/api/health.py**
```python
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
```

### Phase 3: Deployment Configuration

#### 3.1 Environment Configuration

**.env.example**
```env
# MongoDB Atlas Configuration
MONGODB_USERNAME=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password  
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.yourcluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=myCGMitc

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# CORS Configuration (frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### 3.2 Docker Configuration

**Dockerfile**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

# Copy dependency files and install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  loopy-api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Phase 4: Development & Testing

#### 4.1 Local Development

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your MongoDB credentials

# Run development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API will be available at:
# - http://localhost:8000 (root)
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/redoc (ReDoc)
```

#### 4.2 API Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Current glucose
curl http://localhost:8000/api/cgm/current

# Last 24 hours data
curl http://localhost:8000/api/cgm/data?hours=24

# Data status
curl http://localhost:8000/api/cgm/status

# Analysis
curl http://localhost:8000/api/cgm/analysis/24h
```

### Phase 5: Deployment Options

#### 5.1 Docker Deployment
```bash
# Build and run with Docker
docker build -t loopy-api .
docker run -p 8000:8000 --env-file .env loopy-api

# Or use docker-compose
docker-compose up -d
```

#### 5.2 Cloud Deployment

**Railway/Render/Fly.io:**
- Connect GitHub repository
- Set environment variables in dashboard
- Deploy automatically on push

**DigitalOcean App Platform:**
- Create new app from GitHub
- Configure environment variables
- Deploy with automatic scaling

## API Documentation

### Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/` | Root endpoint | None |
| GET | `/api/health` | Health check | None |
| GET | `/api/ping` | Simple ping | None |
| GET | `/api/cgm/data` | Get CGM data | `hours` (1-168) |
| GET | `/api/cgm/current` | Current glucose | None |
| GET | `/api/cgm/status` | Data status | None |
| GET | `/api/cgm/analysis/{period}` | Period analysis | `period` (24h/week/month) |

### Response Examples

**Current Glucose:**
```json
{
  "current_glucose": 142,
  "direction": "Flat",
  "trend": 4,
  "timestamp": "2025-01-16T10:30:00.000Z",
  "minutes_ago": 3.2,
  "device": "share2",
  "type": "sgv"
}
```

**CGM Data:**
```json
{
  "data": [
    {
      "datetime": "2025-01-16T10:30:00.000Z",
      "sgv": 142,
      "direction": "Flat",
      "hour": 10,
      "glucose_category": "Normal"
    }
  ],
  "analysis": {
    "basic_stats": {
      "total_readings": 288,
      "avg_glucose": 145.2
    },
    "time_in_range": {
      "normal_percent": 72.5
    }
  },
  "time_range": {
    "start": "2025-01-15T10:30:00.000Z",
    "end": "2025-01-16T10:30:00.000Z",
    "hours": 24
  }
}
```

## Security Considerations

- Environment-based configuration (no hardcoded credentials)
- CORS properly configured for frontend origins
- Input validation on all endpoints
- Rate limiting can be added with slowapi
- HTTPS required in production
- Read-only database access

## Next Steps

1. Complete implementation following this guide
2. Test all endpoints thoroughly
3. Deploy to chosen platform
4. Configure environment variables
5. Test with MongoDB Atlas connection
6. Integrate with loopy-web frontend