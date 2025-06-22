"""
Sun calculation utilities for sunrise and sunset times
Uses JavaScript execution to leverage SunCalc.js library
"""

import json
import subprocess
import tempfile
import os
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Dublin timezone offset (UTC+0 in winter, UTC+1 in summer)
DUBLIN_TIMEZONE = "Europe/Dublin"

def get_sun_times(latitude: float, longitude: float, date: datetime) -> Optional[Dict[str, str]]:
    """
    Calculate sunrise and sunset times for given coordinates and date
    
    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)  
        date: Date for calculation
        
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
        
        # Create JavaScript code to calculate sun times
        js_code = f"""
        // Load SunCalc library (simulate browser environment)
        const {{ execSync }} = require('child_process');
        const fs = require('fs');
        const path = require('path');

        // Read SunCalc.js library
        const suncalcPath = path.join(__dirname, '../static/js/suncalc.js');
        const suncalcCode = fs.readFileSync(suncalcPath, 'utf8');
        
        // Create a minimal browser-like environment
        global.window = {{}};
        
        // Execute SunCalc library
        eval(suncalcCode);
        const SunCalc = global.window.SunCalc;
        
        // Calculate sun times
        const date = new Date('{date.strftime('%Y-%m-%d')}');
        const times = SunCalc.getTimes(date, {latitude}, {longitude});
        
        // Format times for Dublin timezone
        const dublinOffset = getDublinOffset(date);
        
        function getDublinOffset(date) {{
            // Simple approximation: UTC+0 (winter) or UTC+1 (summer)
            // DST typically runs from last Sunday in March to last Sunday in October
            const year = date.getFullYear();
            const month = date.getMonth(); // 0-11
            
            // Rough DST calculation (March-October)
            if (month >= 2 && month <= 9) {{
                // March to October - might be DST
                if (month >= 3 && month <= 8) return 1; // Definitely DST
                
                // March or October - need to check specific dates
                if (month === 2) {{ // March
                    const lastSunday = getLastSunday(year, 2);
                    return date.getDate() >= lastSunday ? 1 : 0;
                }}
                if (month === 9) {{ // October  
                    const lastSunday = getLastSunday(year, 9);
                    return date.getDate() < lastSunday ? 1 : 0;
                }}
            }}
            return 0; // Standard time (UTC+0)
        }}
        
        function getLastSunday(year, month) {{
            const date = new Date(year, month + 1, 0); // Last day of month
            const day = date.getDay();
            return date.getDate() - day;
        }}
        
        function formatTime(date, offset) {{
            if (!date || isNaN(date.getTime())) return null;
            
            // Apply Dublin timezone offset
            const localTime = new Date(date.getTime() + offset * 60 * 60 * 1000);
            const hours = localTime.getUTCHours().toString().padStart(2, '0');
            const minutes = localTime.getUTCMinutes().toString().padStart(2, '0');
            return hours + ':' + minutes;
        }}
        
        const offset = getDublinOffset(date);
        const result = {{
            sunrise: formatTime(times.sunrise, offset),
            sunset: formatTime(times.sunset, offset),
            solarNoon: formatTime(times.solarNoon, offset),
            dawn: formatTime(times.dawn, offset),
            dusk: formatTime(times.dusk, offset)
        }};
        
        console.log(JSON.stringify(result));
        """
        
        # Write JavaScript to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(js_code)
            js_file = f.name
            
        try:
            # Execute JavaScript using Node.js
            result = subprocess.run(
                ['node', js_file],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse JSON response
                sun_times = json.loads(result.stdout.strip())
                
                # Filter out None values and return only sunrise/sunset
                filtered_times = {{
                    'sunrise': sun_times.get('sunrise'),
                    'sunset': sun_times.get('sunset')
                }}
                
                # Validate that we got valid times
                if filtered_times['sunrise'] and filtered_times['sunset']:
                    return filtered_times
                else:
                    logger.warning(f"Invalid sun times calculated for lat={latitude}, lng={longitude}, date={date}")
                    return None
            else:
                logger.error(f"JavaScript execution failed: {result.stderr}")
                return None
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(js_file)
            except OSError:
                pass
                
    except Exception as e:
        logger.error(f"Error calculating sun times: {str(e)}")
        return None

def get_sun_times_for_location(location_data: Dict[str, Any], date: datetime) -> Optional[Dict[str, str]]:
    """
    Calculate sunrise and sunset for a location with coordinate data
    
    Args:
        location_data: Location dictionary with 'latitude' and 'longitude' keys
        date: Date for calculation
        
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
        
    return get_sun_times(latitude, longitude, date)

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

def validate_sun_calculation_requirements() -> Tuple[bool, str]:
    """
    Check if system has requirements for sun calculations
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check if Node.js is available
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return False, "Node.js is not installed or not available in PATH"
            
        # Check if SunCalc.js file exists
        suncalc_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'js', 'suncalc.js'
        )
        
        if not os.path.exists(suncalc_path):
            return False, f"SunCalc.js library not found at {suncalc_path}"
            
        return True, ""
        
    except Exception as e:
        return False, f"Error checking sun calculation requirements: {str(e)}"