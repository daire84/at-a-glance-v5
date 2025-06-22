"""
Geocoding utilities for converting addresses to coordinates
Supports multiple geocoding services with fallbacks
"""

import requests
import logging
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Cache for geocoding results to avoid API spam
_geocoding_cache = {}
_cache_expiry = {}

class GeocodingResult:
    """Represents a geocoding result with formatted data"""
    def __init__(self, display_name: str, latitude: float, longitude: float, 
                 city: str = "", country: str = "", formatted_address: str = ""):
        self.display_name = display_name
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.country = country
        self.formatted_address = formatted_address

def geocode_address(query: str, limit: int = 5) -> List[GeocodingResult]:
    """
    Geocode an address using multiple services with fallbacks
    
    Args:
        query: Address or place name to search for
        limit: Maximum number of results to return
        
    Returns:
        List of GeocodingResult objects
    """
    # Check cache first
    cache_key = f"{query.lower()}:{limit}"
    if cache_key in _geocoding_cache:
        if datetime.now() < _cache_expiry.get(cache_key, datetime.now()):
            logger.debug(f"Using cached geocoding result for: {query}")
            return _geocoding_cache[cache_key]
    
    results = []
    
    # Try Nominatim (OpenStreetMap) first - free and reliable
    try:
        results = _geocode_nominatim(query, limit)
        if results:
            logger.info(f"Geocoded '{query}' using Nominatim: {len(results)} results")
    except Exception as e:
        logger.warning(f"Nominatim geocoding failed for '{query}': {e}")
    
    # If Nominatim fails, try other services
    if not results:
        try:
            results = _geocode_fallback(query, limit)
            if results:
                logger.info(f"Geocoded '{query}' using fallback service: {len(results)} results")
        except Exception as e:
            logger.warning(f"Fallback geocoding failed for '{query}': {e}")
    
    # Cache results for 24 hours
    if results:
        _geocoding_cache[cache_key] = results
        _cache_expiry[cache_key] = datetime.now() + timedelta(hours=24)
    
    return results

def _geocode_nominatim(query: str, limit: int) -> List[GeocodingResult]:
    """Geocode using Nominatim (OpenStreetMap)"""
    
    # Add bias for Ireland/UK for film production locations
    ireland_bias = "&countrycodes=ie,gb"
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': limit,
        'addressdetails': 1,
        'extratags': 1,
        'namedetails': 1
    }
    
    headers = {
        'User-Agent': 'FilmProductionCalendar/1.0 (contact@filmcalendar.example)'
    }
    
    # Try with Ireland/UK bias first
    response = requests.get(url + ireland_bias, params=params, headers=headers, timeout=10)
    
    if response.status_code != 200:
        # Try without bias
        response = requests.get(url, params=params, headers=headers, timeout=10)
    
    response.raise_for_status()
    data = response.json()
    
    results = []
    for item in data:
        try:
            lat = float(item['lat'])
            lng = float(item['lon'])
            
            # Extract address components
            address = item.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village') or ""
            country = address.get('country', "")
            
            # Create display name prioritizing important info
            display_parts = []
            if item.get('display_name'):
                # Clean up the display name
                display_name = item['display_name']
                if len(display_name) > 80:
                    # Truncate long addresses
                    parts = display_name.split(', ')
                    if len(parts) > 3:
                        display_name = ', '.join(parts[:3]) + f", {country}"
            else:
                display_name = query
            
            result = GeocodingResult(
                display_name=display_name,
                latitude=lat,
                longitude=lng,
                city=city,
                country=country,
                formatted_address=item.get('display_name', '')
            )
            
            results.append(result)
            
        except (KeyError, ValueError, TypeError) as e:
            logger.debug(f"Skipping invalid geocoding result: {e}")
            continue
    
    return results

def _geocode_fallback(query: str, limit: int) -> List[GeocodingResult]:
    """Fallback geocoding using built-in city database"""
    
    # Common film production locations with coordinates
    COMMON_LOCATIONS = {
        # Ireland
        'dublin': (53.3498, -6.2603, "Dublin, Ireland"),
        'cork': (51.8985, -8.4756, "Cork, Ireland"), 
        'galway': (53.2707, -9.0568, "Galway, Ireland"),
        'kilkenny': (52.6541, -7.2448, "Kilkenny, Ireland"),
        'wicklow': (52.9808, -6.0331, "Wicklow, Ireland"),
        'waterford': (52.2593, -7.1101, "Waterford, Ireland"),
        
        # UK
        'london': (51.5074, -0.1278, "London, UK"),
        'edinburgh': (55.9533, -3.1883, "Edinburgh, Scotland"),
        'cardiff': (51.4816, -3.1791, "Cardiff, Wales"),
        'belfast': (54.5973, -5.9301, "Belfast, Northern Ireland"),
        'manchester': (53.4808, -2.2426, "Manchester, UK"),
        'birmingham': (52.4862, -1.8904, "Birmingham, UK"),
        
        # Common international locations
        'paris': (48.8566, 2.3522, "Paris, France"),
        'rome': (41.9028, 12.4964, "Rome, Italy"),
        'prague': (50.0755, 14.4378, "Prague, Czech Republic"),
        'budapest': (47.4979, 19.0402, "Budapest, Hungary"),
        'barcelona': (41.3851, 2.1734, "Barcelona, Spain"),
        'amsterdam': (52.3676, 4.9041, "Amsterdam, Netherlands"),
    }
    
    query_lower = query.lower().strip()
    results = []
    
    # Exact matches first
    if query_lower in COMMON_LOCATIONS:
        lat, lng, display = COMMON_LOCATIONS[query_lower]
        city_name = display.split(',')[0]
        country_name = display.split(',')[1].strip()
        
        result = GeocodingResult(
            display_name=display,
            latitude=lat,
            longitude=lng,
            city=city_name,
            country=country_name,
            formatted_address=display
        )
        results.append(result)
    
    # Partial matches
    for location_key, (lat, lng, display) in COMMON_LOCATIONS.items():
        if query_lower in location_key or location_key in query_lower:
            if not any(r.display_name == display for r in results):  # Avoid duplicates
                city_name = display.split(',')[0]
                country_name = display.split(',')[1].strip()
                
                result = GeocodingResult(
                    display_name=display,
                    latitude=lat,
                    longitude=lng,
                    city=city_name,
                    country=country_name,
                    formatted_address=display
                )
                results.append(result)
                
                if len(results) >= limit:
                    break
    
    return results

def get_popular_film_locations() -> List[Dict]:
    """Get a list of popular filming locations for quick selection"""
    
    popular_locations = [
        # Ireland
        {"name": "Dublin City Centre", "lat": 53.3498, "lng": -6.2603, "country": "Ireland"},
        {"name": "Trinity College Dublin", "lat": 53.3444, "lng": -6.2567, "country": "Ireland"},
        {"name": "Temple Bar, Dublin", "lat": 53.3453, "lng": -6.2659, "country": "Ireland"},
        {"name": "Cliffs of Moher", "lat": 52.9715, "lng": -9.4309, "country": "Ireland"},
        {"name": "Ring of Kerry", "lat": 51.8847, "lng": -10.1239, "country": "Ireland"},
        {"name": "Giant's Causeway", "lat": 55.2408, "lng": -6.5116, "country": "Northern Ireland"},
        {"name": "Ashford Castle", "lat": 53.5451, "lng": -9.3117, "country": "Ireland"},
        {"name": "Kilmainham Gaol", "lat": 53.3420, "lng": -6.3098, "country": "Ireland"},
        
        # UK Popular Film Locations
        {"name": "Tower Bridge, London", "lat": 51.5055, "lng": -0.0754, "country": "UK"},
        {"name": "Windsor Castle", "lat": 51.4839, "lng": -0.6044, "country": "UK"},
        {"name": "Edinburgh Castle", "lat": 55.9486, "lng": -3.1999, "country": "Scotland"},
        {"name": "Stonehenge", "lat": 51.1789, "lng": -1.8262, "country": "UK"},
        {"name": "Oxford University", "lat": 51.7548, "lng": -1.2544, "country": "UK"},
        {"name": "Canterbury Cathedral", "lat": 51.2798, "lng": 1.0830, "country": "UK"},
        
        # Studio Locations
        {"name": "Ardmore Studios", "lat": 53.2034, "lng": -6.1031, "country": "Ireland"},
        {"name": "Pinewood Studios", "lat": 51.5439, "lng": -0.6769, "country": "UK"},
        {"name": "Shepperton Studios", "lat": 51.3956, "lng": -0.4535, "country": "UK"},
    ]
    
    return popular_locations

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate that coordinates are within reasonable bounds"""
    try:
        lat = float(latitude)
        lng = float(longitude)
        return -90 <= lat <= 90 and -180 <= lng <= 180
    except (ValueError, TypeError):
        return False

def clear_geocoding_cache():
    """Clear the geocoding cache"""
    global _geocoding_cache, _cache_expiry
    _geocoding_cache.clear()
    _cache_expiry.clear()
    logger.info("Geocoding cache cleared")

def get_cache_stats() -> Dict:
    """Get geocoding cache statistics"""
    return {
        'cache_size': len(_geocoding_cache),
        'cached_queries': list(_geocoding_cache.keys())
    }