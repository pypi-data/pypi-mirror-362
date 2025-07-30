from loopy.data.cgm import CGMDataAccess
from datetime import datetime, timedelta
from typing import Dict, Any
import logging
import numpy as np

logger = logging.getLogger(__name__)


def convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):  # Other numpy scalars
        return obj.item()
    elif hasattr(obj, '__class__') and obj.__class__.__name__ == 'ObjectId':
        return str(obj)
    else:
        return obj


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
                
                # Prepare the response
                response = {
                    "data": data_records,
                    "analysis": analysis,
                    "last_updated": datetime.now().isoformat(),
                    "time_range": {
                        "start": start_time.isoformat(),
                        "end": end_time.isoformat(),
                        "hours": hours
                    }
                }
                
                # Convert all numpy types and ObjectIds recursively
                return convert_numpy_types(response)
                
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