# routes/main.py
import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, request, session

from utils.decorators import viewer_required
from utils.helpers import get_project, get_project_calendar, DATA_DIR, logger, get_projects, get_project_versions
from utils.calendar_generator import calculate_department_counts, calculate_location_counts

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def welcome():
    """Welcome page - no authentication required"""
    return render_template('welcome.html')

@main_bp.route('/dashboard')
@viewer_required
def dashboard():
    """Project dashboard - renamed from index"""
    projects = get_projects()
    return render_template('dashboard.html', projects=projects)

@main_bp.route('/viewer/<project_id>')
# @viewer_required # Apply decorator if viewer needs to be logged in
def viewer(project_id):
    """Calendar viewer"""
    user_id = session.get('user_id')  # Extract user_id for proper project scoping
    project = get_project(project_id, user_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('main.dashboard'))

    version_id = request.args.get('version')
    
    # Check if project is versioned
    if project.get('isVersioned'):
        versions = get_project_versions(project_id, user_id)
        
        # Get specific version if requested
        if version_id:
            version = next((v for v in versions if v['id'] == version_id), None)
            
            if version:
                calendar_data = version.get('calendarData', {"days": []})
            else:
                flash('Version not found', 'error')
                return redirect(url_for('main.viewer', project_id=project_id))
        else:
            # Get the latest published version
            published_version = next(
                (v for v in versions if v.get('isLatestPublished')), 
                None
            )
            
            if published_version:
                calendar_data = published_version.get('calendarData', {"days": []})
                version_id = published_version['id']
            else:
                # No published version yet
                return render_template('viewer.html', 
                    project=project, 
                    calendar=None,
                    no_published_version=True,
                    versions=[],
                    locations=[]
                )
    else:
        # Fallback to existing behavior for non-versioned projects
        calendar_data = get_project_calendar(project_id, user_id)

    # --- Load supporting data ---
    departments = []
    departments_file = os.path.join(DATA_DIR, 'departments.json')
    if os.path.exists(departments_file):
        try:
            with open(departments_file, 'r') as f:
                departments = json.load(f)
        except Exception as e:
            logger.error(f"Error loading departments: {str(e)}")

    locations = []
    locations_file = os.path.join(DATA_DIR, 'locations.json')
    if os.path.exists(locations_file):
        try:
            with open(locations_file, 'r') as f:
                locations = json.load(f)
        except Exception as e:
            logger.error(f"Error loading locations: {str(e)}")

    areas = []
    areas_file = os.path.join(DATA_DIR, 'areas.json')
    if os.path.exists(areas_file):
        try:
            with open(areas_file, 'r') as f:
                areas = json.load(f)
        except Exception as e:
            logger.error(f"Error loading areas in viewer route: {str(e)}")
    # --- End Load supporting data ---

    # Ensure the latest supporting data is available in the calendar_data object
    calendar_data['departments'] = departments
    calendar_data['locationAreas'] = areas # Add/overwrite with the fresh list

    # Calculate counts and sun times
    calendar_data = calculate_department_counts(calendar_data)
    calendar_data = calculate_location_counts(calendar_data)
    
    # Calculate sun times for days with locations
    from utils.calendar_generator import calculate_sun_times_for_calendar
    calendar_data = calculate_sun_times_for_calendar(calendar_data)

    # Get all versions for the dropdown (only published ones)
    all_versions = []
    if project.get('isVersioned'):
        all_versions = [v for v in versions if v.get('isPublished')]
        # Sort by version number
        all_versions.sort(key=lambda v: v.get('versionNumber', '0.0'))

    return render_template('viewer.html', 
        project=project, 
        calendar=calendar_data, 
        locations=locations,
        versions=all_versions,
        current_version_id=version_id
    )

@main_bp.route('/help')
def help():
    """Help and about page"""
    return render_template('help.html')

@main_bp.route('/health')
# @viewer_required # Apply if needed
def health():
    """Health check endpoint"""
    # This route might not belong in 'main', consider a separate 'utility' blueprint later
    from flask import jsonify # Import jsonify locally if only used here
    return jsonify({"status": "ok", "version": "1.0.0"}), 200

# Static files route - can stay in app.py or move here if preferred
# If moved here, change url_for('static', ...) to url_for('main.serve_static', ...)
# @main_bp.route('/static/<path:path>')
# def serve_static(path):
#    return send_from_directory('static', path) # Adjust path if needed ('../static')