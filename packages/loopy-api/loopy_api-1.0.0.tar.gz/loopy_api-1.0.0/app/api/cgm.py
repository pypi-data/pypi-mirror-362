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
    period: str
) -> Dict[str, Any]:
    """Get analysis for a specific time period.
    
    Args:
        period: Analysis period (24h, week, or month)
        
    Returns:
        Analysis data for the specified period
    """
    try:
        # Validate period parameter
        valid_periods = {"24h": 24, "week": 168, "month": 720}
        if period not in valid_periods:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period '{period}'. Must be one of: {', '.join(valid_periods.keys())}"
            )
        
        hours = valid_periods[period]
        
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