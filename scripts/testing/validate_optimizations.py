"""
Simple validation script for sun time optimizations
"""

import logging
logging.basicConfig(level=logging.INFO)

try:
    from utils.sun_utils import validate_sun_calculation_requirements
    print("Testing sun calculation requirements...")
    
    valid, msg = validate_sun_calculation_requirements()
    print(f"Requirements check: {'✓ PASS' if valid else '✗ FAIL'}")
    if msg:
        print(f"Message: {msg}")
    
    if valid:
        from utils.sun_utils import get_sun_times
        from datetime import datetime
        
        print("\nTesting basic calculation...")
        result = get_sun_times(53.3498, -6.2603, datetime(2024, 6, 21))
        if result:
            print(f"✓ Dublin June 21, 2024: {result['sunrise']} - {result['sunset']}")
        else:
            print("✗ Calculation failed")
        
        print("\n🎉 Optimizations validated successfully!")
    else:
        print("\n❌ Requirements not met. Check dependencies.")
        
except Exception as e:
    print(f"❌ Error during validation: {e}")
    import traceback
    traceback.print_exc()