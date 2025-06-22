"""
Optimized sun calculation utilities for sunrise and sunset times
Uses native Python astral library for fast, accurate calculations with caching
"""

import os
from datetime import datetime, date
from typing import Optional, Dict, Any
import logging
import pytz
from astral import LocationInfo
from astral.sun import sun

logger = logging.getLogger(__name__)

# Cache for repeated calculations - stores results for same date/location
_sun_times_cache = {}

def get_sun_times(latitude: float, longitude: float, date_input: datetime) -> Optional[Dict[str, str]]:
    """
    Calculate sunrise and sunset times for given coordinates and date
    
    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)  
        date_input: Date for calculation (datetime object)
        
    Returns:
        Dictionary with 'sunrise' and 'sunset' times in HH:MM format (Dublin timezone)
        Returns None if calculation fails
    """
    try:
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            logger.error(f"Invalid latitude: {latitude}. Must be between -90 and 90")
            return None
            
        if not (-180 <= longitude <= 180):
            logger.error(f"Invalid longitude: {longitude}. Must be between -180 and 180")
            return None
        
        # Create cache key
        date_str = date_input.strftime('%Y-%m-%d')
        cache_key = f"{latitude:.4f},{longitude:.4f},{date_str}"
        
        # Check cache first
        if cache_key in _sun_times_cache:
            logger.debug(f"Using cached sun times for {cache_key}")
            return _sun_times_cache[cache_key]
        
        # Set up location and timezone
        dublin_tz = pytz.timezone('Europe/Dublin')
        location = LocationInfo(latitude=latitude, longitude=longitude)
        
        # Convert datetime to date if needed
        if isinstance(date_input, datetime):
            calculation_date = date_input.date()
        else:
            calculation_date = date_input
        
        # Calculate sun times for the date
        sun_times = sun(location.observer, date=calculation_date, tzinfo=dublin_tz)
        
        # Format times as HH:MM strings
        result = {
            'sunrise': sun_times['sunrise'].strftime('%H:%M'),
            'sunset': sun_times['sunset'].strftime('%H:%M')
        }
        
        # Cache the result
        _sun_times_cache[cache_key] = result
        logger.debug(f"Calculated sun times for {cache_key}: {result}")
        
        return result
                
    except Exception as e:
        logger.error(f"Error calculating sun times for lat={latitude}, lng={longitude}, date={date_input}: {str(e)}")
        return None

def get_sun_times_for_location(location_data: Dict[str, Any], date_input: datetime) -> Optional[Dict[str, str]]:
    """
    Calculate sunrise and sunset for a location with coordinate data
    
    Args:
        location_data: Location dictionary with 'latitude' and 'longitude' keys
        date_input: Date for calculation
        
    Returns:
        Dictionary with 'sunrise' and 'sunset' times in HH:MM format
        Returns None if location has no coordinates or calculation fails
    """
    if not location_data:
        return None
        
    latitude = location_data.get('latitude')
    longitude = location_data.get('longitude')
    
    if latitude is None or longitude is None:
        logger.debug(f"Location '{location_data.get('name', 'Unknown')}' has no coordinates")
        return None
        
    return get_sun_times(latitude, longitude, date_input)

def format_sun_times_display(sun_times: Optional[Dict[str, str]]) -> str:
    """
    Format sun times for display in calendar
    
    Args:
        sun_times: Dictionary with sunrise/sunset times
        
    Returns:
        Formatted string like "06:30 - 18:45" or empty string if no times
    """
    if not sun_times or not sun_times.get('sunrise') or not sun_times.get('sunset'):
        return ""
        
    return f"{sun_times['sunrise']} - {sun_times['sunset']}"

def get_enhanced_sun_times(latitude: float, longitude: float, date_input: datetime) -> Optional[Dict[str, str]]:
    """
    Calculate enhanced sun times including golden hour information
    
    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)  
        date_input: Date for calculation
        
    Returns:
        Dictionary with sunrise, sunset, dawn, dusk, golden hour times
        Returns None if calculation fails
    """
    try:
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return None
        
        # Create cache key for enhanced times
        date_str = date_input.strftime('%Y-%m-%d')
        cache_key = f"enhanced_{latitude:.4f},{longitude:.4f},{date_str}"
        
        # Check cache first
        if cache_key in _sun_times_cache:
            return _sun_times_cache[cache_key]
        
        # Set up location and timezone
        dublin_tz = pytz.timezone('Europe/Dublin')
        location = LocationInfo(latitude=latitude, longitude=longitude)
        
        # Convert datetime to date if needed
        calculation_date = date_input.date() if isinstance(date_input, datetime) else date_input
        
        # Calculate all sun times
        sun_times = sun(location.observer, date=calculation_date, tzinfo=dublin_tz)
        
        # Format enhanced times
        result = {
            'sunrise': sun_times['sunrise'].strftime('%H:%M'),
            'sunset': sun_times['sunset'].strftime('%H:%M'),
            'dawn': sun_times['dawn'].strftime('%H:%M'),
            'dusk': sun_times['dusk'].strftime('%H:%M'),
            'solar_noon': sun_times['noon'].strftime('%H:%M')
        }
        
        # Calculate golden hour times (approximately 1 hour after sunrise and 1 hour before sunset)
        from datetime import timedelta
        golden_hour_morning = sun_times['sunrise'] + timedelta(hours=1)
        golden_hour_evening = sun_times['sunset'] - timedelta(hours=1)
        
        result.update({
            'golden_hour_morning_end': golden_hour_morning.strftime('%H:%M'),
            'golden_hour_evening_start': golden_hour_evening.strftime('%H:%M')
        })
        
        # Cache the result
        _sun_times_cache[cache_key] = result
        
        return result
                
    except Exception as e:
        logger.error(f"Error calculating enhanced sun times: {str(e)}")
        return None

def clear_sun_times_cache():
    """Clear the sun times cache - useful for memory management"""
    global _sun_times_cache
    _sun_times_cache.clear()
    logger.info("Sun times cache cleared")

def get_cache_size():
    """Get current cache size for monitoring"""
    return len(_sun_times_cache)

def validate_sun_calculation_requirements() -> tuple[bool, str]:
    """
    Check if system has requirements for sun calculations
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check if pytz is available
        import pytz
        
        # Check if astral is available
        from astral import LocationInfo
        from astral.sun import sun
        
        # Test basic functionality
        dublin_tz = pytz.timezone('Europe/Dublin')
        test_location = LocationInfo(latitude=53.3498, longitude=-6.2603)
        test_date = datetime.now().date()
        
        # Try a calculation
        sun_times = sun(test_location.observer, date=test_date, tzinfo=dublin_tz)
        
        return True, ""
        
    except ImportError as e:
        return False, f"Missing required library: {str(e)}"
    except Exception as e:
        return False, f"Error testing sun calculation requirements: {str(e)}"