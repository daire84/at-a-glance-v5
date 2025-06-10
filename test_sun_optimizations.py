#!/usr/bin/env python3
"""
Test script for optimized sun calculation functions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from utils.sun_utils import (
    get_sun_times, 
    get_sun_times_for_location, 
    format_sun_times_display,
    get_enhanced_sun_times,
    validate_sun_calculation_requirements,
    get_cache_size,
    clear_sun_times_cache
)

def test_requirements():
    """Test that all requirements are met"""
    print("=== Testing Requirements ===")
    valid, msg = validate_sun_calculation_requirements()
    print(f"Requirements valid: {valid}")
    if not valid:
        print(f"Error: {msg}")
        return False
    print("✓ All requirements met")
    return True

def test_basic_calculations():
    """Test basic sun time calculations"""
    print("\n=== Testing Basic Calculations ===")
    
    # Test Dublin coordinates
    dublin_lat, dublin_lng = 53.3498, -6.2603
    test_date = datetime(2024, 6, 21)  # Summer solstice
    
    print(f"Testing Dublin ({dublin_lat}, {dublin_lng}) on {test_date.date()}")
    
    result = get_sun_times(dublin_lat, dublin_lng, test_date)
    if result:
        print(f"✓ Sunrise: {result['sunrise']}, Sunset: {result['sunset']}")
        formatted = format_sun_times_display(result)
        print(f"✓ Formatted: {formatted}")
    else:
        print("✗ Failed to calculate sun times")
        return False
    
    return True

def test_location_calculations():
    """Test location-based calculations"""
    print("\n=== Testing Location Calculations ===")
    
    # Test location with coordinates
    location_with_coords = {
        'name': 'Trinity College',
        'latitude': 53.3444,
        'longitude': -6.2567
    }
    
    test_date = datetime(2024, 12, 21)  # Winter solstice
    
    print(f"Testing {location_with_coords['name']} on {test_date.date()}")
    
    result = get_sun_times_for_location(location_with_coords, test_date)
    if result:
        print(f"✓ Sunrise: {result['sunrise']}, Sunset: {result['sunset']}")
    else:
        print("✗ Failed to calculate sun times for location")
        return False
    
    # Test location without coordinates
    location_no_coords = {
        'name': 'Studio Without Coords'
    }
    
    result = get_sun_times_for_location(location_no_coords, test_date)
    if result is None:
        print("✓ Correctly handled location without coordinates")
    else:
        print("✗ Should have returned None for location without coordinates")
        return False
    
    return True

def test_caching():
    """Test caching functionality"""
    print("\n=== Testing Caching ===")
    
    # Clear cache first
    clear_sun_times_cache()
    print(f"Cache size after clear: {get_cache_size()}")
    
    # Make same calculation multiple times
    dublin_lat, dublin_lng = 53.3498, -6.2603
    test_date = datetime(2024, 6, 21)
    
    print("Making first calculation...")
    result1 = get_sun_times(dublin_lat, dublin_lng, test_date)
    cache_size_1 = get_cache_size()
    print(f"Cache size after first calculation: {cache_size_1}")
    
    print("Making identical calculation...")
    result2 = get_sun_times(dublin_lat, dublin_lng, test_date)
    cache_size_2 = get_cache_size()
    print(f"Cache size after second calculation: {cache_size_2}")
    
    if result1 == result2 and cache_size_1 == cache_size_2:
        print("✓ Caching working correctly")
    else:
        print("✗ Caching not working properly")
        return False
    
    return True

def test_enhanced_calculations():
    """Test enhanced sun time calculations"""
    print("\n=== Testing Enhanced Calculations ===")
    
    dublin_lat, dublin_lng = 53.3498, -6.2603
    test_date = datetime(2024, 6, 21)
    
    print(f"Testing enhanced calculations for Dublin on {test_date.date()}")
    
    result = get_enhanced_sun_times(dublin_lat, dublin_lng, test_date)
    if result:
        print(f"✓ Sunrise: {result['sunrise']}")
        print(f"✓ Sunset: {result['sunset']}")
        print(f"✓ Dawn: {result['dawn']}")
        print(f"✓ Dusk: {result['dusk']}")
        print(f"✓ Solar Noon: {result['solar_noon']}")
        print(f"✓ Golden Hour Morning End: {result['golden_hour_morning_end']}")
        print(f"✓ Golden Hour Evening Start: {result['golden_hour_evening_start']}")
    else:
        print("✗ Failed to calculate enhanced sun times")
        return False
    
    return True

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n=== Testing Edge Cases ===")
    
    # Invalid coordinates
    print("Testing invalid latitude...")
    result = get_sun_times(95.0, -6.2603, datetime(2024, 6, 21))
    if result is None:
        print("✓ Correctly handled invalid latitude")
    else:
        print("✗ Should have rejected invalid latitude")
        return False
    
    print("Testing invalid longitude...")
    result = get_sun_times(53.3498, 200.0, datetime(2024, 6, 21))
    if result is None:
        print("✓ Correctly handled invalid longitude")
    else:
        print("✗ Should have rejected invalid longitude")
        return False
    
    # Test extreme but valid coordinates
    print("Testing Arctic coordinates...")
    result = get_sun_times(80.0, 0.0, datetime(2024, 6, 21))  # Arctic summer
    if result:
        print(f"✓ Arctic summer - Sunrise: {result['sunrise']}, Sunset: {result['sunset']}")
    else:
        print("! Arctic calculations may fail in extreme conditions (this is expected)")
    
    return True

def main():
    """Run all tests"""
    print("Sun Times Optimization Test Suite")
    print("=" * 50)
    
    tests = [
        test_requirements,
        test_basic_calculations,
        test_location_calculations,
        test_caching,
        test_enhanced_calculations,
        test_edge_cases
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"✗ {test.__name__} failed")
        except Exception as e:
            print(f"✗ {test.__name__} threw exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Optimizations are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)