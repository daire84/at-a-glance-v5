#!/usr/bin/env python3

"""
Debug script to test route generation and identify issues
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, '/mnt/user/appdata/film-scheduler-v6')

try:
    from app import app
    
    with app.app_context():
        from flask import url_for
        
        print("=== ROUTE DEBUGGING ===")
        
        # Test URL generation
        try:
            dashboard_url = url_for('admin.admin_dashboard')
            print(f"✅ Admin dashboard URL: {dashboard_url}")
        except Exception as e:
            print(f"❌ Admin dashboard URL generation failed: {e}")
        
        try:
            new_project_url = url_for('admin.admin_project', project_id='new')
            print(f"✅ New project URL: {new_project_url}")
        except Exception as e:
            print(f"❌ New project URL generation failed: {e}")
        
        # List all admin routes
        print("\n=== ALL ADMIN ROUTES ===")
        for rule in app.url_map.iter_rules():
            if rule.endpoint and rule.endpoint.startswith('admin.'):
                print(f"  {rule.endpoint}: {rule.rule}")
        
        print("\n=== ALL ROUTES ===")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.endpoint}: {rule.rule}")
            
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
except Exception as e:
    print(f"❌ Error: {e}")