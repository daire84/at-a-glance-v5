# routes/api.py
import os
import json
import uuid
import shutil
from flask import Blueprint, jsonify, request # <-- Ensure this line is correct

from utils.decorators import admin_required # Absolute import
from utils.helpers import get_projects, get_project, save_project, get_project_calendar, save_project_calendar, generate_calendar, DATA_DIR, PROJECTS_DIR, logger, update_all_projects_department_counts, recalculate_shoot_days, get_project_versions, create_project_version, publish_project_version, get_project_workspace, save_project_workspace, migrate_project_to_versioned_structure # Absolute import
from utils.geocoding import geocode_address, get_popular_film_locations # Absolute import

api_bp = Blueprint('api', __name__, url_prefix='/api')

# --- Project API Routes ---
@api_bp.route('/projects', methods=['GET', 'POST'])
@admin_required
def api_projects():
    """List or create projects"""
    if request.method == 'GET':
        from flask import session
        user_id = session.get('user_id')
        return jsonify(get_projects(user_id))
    elif request.method == 'POST':
        try:
            project = request.get_json()
            from flask import session
            user_id = session.get('user_id')
            result = save_project(project, user_id)
            # Optionally generate calendar for new project here if desired
            # generate_calendar(result)
            return jsonify(result), 201
        except Exception as e:
             logger.error(f"API Error creating project: {e}")
             return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_project(project_id):
    """Get, update or delete a project"""
    from flask import session
    user_id = session.get('user_id')
    if request.method == 'GET':
        project = get_project(project_id, user_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(project)
    elif request.method == 'PUT':
        try:
            project_data = request.get_json()
            # Ensure ID from URL is used, not potentially from payload
            project_data['id'] = project_id
            result = save_project(project_data, user_id)
            return jsonify(result)
        except Exception as e:
             logger.error(f"API Error updating project {project_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            project_dir = os.path.join(PROJECTS_DIR, project_id)
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
                logger.info(f"Project {project_id} deleted via API.")
                return jsonify({'success': True})
            else:
                 return jsonify({'error': 'Project not found'}), 404
        except Exception as e:
             logger.error(f"API Error deleting project {project_id}: {e}")
             return jsonify({'error': str(e)}), 500

# --- Calendar API Routes ---
@api_bp.route('/projects/<project_id>/calendar', methods=['GET', 'POST'])
@admin_required
def api_project_calendar(project_id):
    """Get or update project calendar"""
    if request.method == 'GET':
        # Check if project is versioned
        from flask import session
        user_id = session.get('user_id')
        project = get_project(project_id, user_id)
        if project and project.get('isVersioned'):
            workspace = get_project_workspace(project_id, user_id)
            if workspace:
                return jsonify(workspace.get('calendarData', {"days": []}))
        
        # Fallback to existing behavior
        calendar_data = get_project_calendar(project_id, user_id)
        return jsonify(calendar_data)
    elif request.method == 'POST':
        try:
            calendar_data = request.get_json()
            
            # Check if project is versioned
            from flask import session
            user_id = session.get('user_id')
            project = get_project(project_id, user_id)
            if project and project.get('isVersioned'):
                # Save to workspace
                workspace = get_project_workspace(project_id, user_id)
                if workspace:
                    workspace['calendarData'] = calendar_data
                    save_project_workspace(project_id, workspace, user_id)
                    return jsonify(calendar_data)
            
            # Fallback to existing behavior
            result = save_project_calendar(project_id, calendar_data, user_id)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error saving calendar for {project_id}: {e}")
            return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>/calendar/generate', methods=['POST'])
@admin_required
def api_generate_calendar(project_id):
    """Generate calendar for project"""
    from flask import session
    user_id = session.get('user_id')
    project = get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    try:
        calendar_data = generate_calendar(project, user_id)
        return jsonify(calendar_data)
    except Exception as e:
        logger.error(f"API Error generating calendar for {project_id}: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>/calendar/day/<date>', methods=['GET', 'PUT'])
@admin_required
def api_calendar_day(project_id, date):
    """Get or update a specific calendar day"""
    # This duplicates logic from admin_day PUT. Consider refactoring later.
    from flask import session
    user_id = session.get('user_id')
    calendar_data = get_project_calendar(project_id, user_id)
    day_index = next((i for i, d in enumerate(calendar_data.get('days', [])) if d.get('date') == date), None)

    if day_index is None:
        return jsonify({'error': 'Day not found'}), 404

    if request.method == 'GET':
        return jsonify(calendar_data['days'][day_index])
    elif request.method == 'PUT':
        try:
            day_data = request.get_json()
            # Basic update - might need more complex logic like in admin_day
            calendar_data['days'][day_index].update(day_data)
            save_project_calendar(project_id, calendar_data, user_id)
            # Recalculate counts after API update? Might be needed.
            # calendar_data = calculate_department_counts(calendar_data)
            # calendar_data = calculate_location_counts(calendar_data)
            # save_project_calendar(project_id, calendar_data)
            return jsonify(calendar_data['days'][day_index])
        except Exception as e:
             logger.error(f"API Error updating day {date} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/calendar/move-day', methods=['POST'])
@admin_required
def api_move_calendar_day(project_id):
    """Move a shoot day"""
    try:
        from flask import session
        user_id = session.get('user_id')
        move_data = request.get_json()
        from_date = move_data.get('fromDate')
        to_date = move_data.get('toDate')
        mode = move_data.get('mode', 'swap')

        logger.info(f"API Move day request: from {from_date} to {to_date} using mode {mode}")

        if not from_date or not to_date:
            return jsonify({'error': 'Missing source or target date'}), 400

        calendar_data = get_project_calendar(project_id, user_id)
        if not calendar_data or 'days' not in calendar_data:
            return jsonify({'error': 'Calendar data not found or invalid'}), 404

        days = calendar_data.get('days', [])
        from_day_index = next((i for i, d in enumerate(days) if d.get('date') == from_date), None)
        to_day_index = next((i for i, d in enumerate(days) if d.get('date') == to_date), None)

        if from_day_index is None or to_day_index is None:
            return jsonify({'error': 'Source or destination day not found in calendar'}), 404

        from_day = days[from_day_index]
        to_day = days[to_day_index]

        # --- Validation ---
        if not from_day.get('isShootDay', False):
             return jsonify({'error': 'Can only move shoot days'}), 400
        # Check target day validity (using .get safely)
        if to_day.get('isHiatus') or \
           (to_day.get('isHoliday') and not to_day.get('isWorking', False)) or \
           (to_day.get('isWeekend') and not to_day.get('isWorkingWeekend', False)):
             return jsonify({'error': 'Cannot move to a non-working day (holiday, hiatus, or non-working weekend)'}), 400
        # --- End Validation ---


        original_shoot_day = from_day.get('shootDay') # Before modification
        target_shoot_day = to_day.get('shootDay') # Before modification


        if mode == 'swap':
            # Preserve date-specific info
            to_date_info = {k: to_day.get(k) for k in ['date', 'dayOfWeek', 'monthName', 'day', 'month', 'year', 'isPrep', 'isWeekend', 'isHoliday', 'isHiatus', 'isWorkingWeekend', 'dayType']}
            from_date_info = {k: from_day.get(k) for k in ['date', 'dayOfWeek', 'monthName', 'day', 'month', 'year', 'isPrep', 'isWeekend', 'isHoliday', 'isHiatus', 'isWorkingWeekend', 'dayType']}

            new_to_day = from_day.copy()
            new_from_day = to_day.copy()

            new_to_day.update(to_date_info)
            new_from_day.update(from_date_info)

            # Ensure shoot day status is correct after swap
            new_to_day['isShootDay'] = True
            if not to_day.get('isShootDay'): # If target wasn't a shoot day
                new_from_day['isShootDay'] = False
                new_from_day['shootDay'] = None
                # Potentially reset other shoot-specific fields on new_from_day if needed

            days[from_day_index] = new_from_day
            days[to_day_index] = new_to_day

        else: # Add other modes like 'insert' later if needed
            return jsonify({'error': 'Unsupported move mode'}), 400

        # Recalculate shoot day numbers after any move
        calendar_data['days'] = recalculate_shoot_days(days)
        save_project_calendar(project_id, calendar_data, user_id)

        return jsonify({
            'success': True,
            'message': f'Day {original_shoot_day} swapped with {to_date}',
            'originalDay': original_shoot_day,
            'targetDay': target_shoot_day,
            'mode': mode
        }), 200

    except Exception as e:
        logger.error(f"API Error moving calendar day for {project_id}: {str(e)}")
        return jsonify({'error': f'Error moving calendar day: {str(e)}'}), 500


# --- Helper Functions for Location Data ---
def validate_coordinates(latitude, longitude):
    """Validate coordinate values and consistency"""
    has_lat = latitude is not None and str(latitude).strip() != ''
    has_lng = longitude is not None and str(longitude).strip() != ''
    
    # Both coordinates must be provided together or both must be empty
    if has_lat != has_lng:
        return False, "Both latitude and longitude must be provided together, or both must be empty"
    
    if has_lat and has_lng:
        try:
            lat_val = float(latitude)
            lng_val = float(longitude)
            
            # Validate coordinate ranges
            if not (-90 <= lat_val <= 90):
                return False, "Latitude must be between -90 and 90 degrees"
            if not (-180 <= lng_val <= 180):
                return False, "Longitude must be between -180 and 180 degrees"
                
        except (ValueError, TypeError):
            return False, "Coordinates must be valid decimal numbers"
    
    return True, None

def normalize_location_data(location):
    """Ensure location has all required fields with proper defaults"""
    normalized = {
        'id': location.get('id'),
        'name': location.get('name', ''),
        'areaId': location.get('areaId', ''),
        'address': location.get('address', ''),
        'notes': location.get('notes', ''),
        'latitude': location.get('latitude'),
        'longitude': location.get('longitude')
    }
    
    # Ensure coordinates are properly typed
    if normalized['latitude'] is not None:
        try:
            normalized['latitude'] = float(normalized['latitude'])
        except (ValueError, TypeError):
            normalized['latitude'] = None
    
    if normalized['longitude'] is not None:
        try:
            normalized['longitude'] = float(normalized['longitude'])
        except (ValueError, TypeError):
            normalized['longitude'] = None
    
    return normalized

# --- Location API Routes ---
@api_bp.route('/locations', methods=['GET', 'POST'])
@admin_required
def api_locations():
    """List or create locations"""
    # Refactor to use helper?
    locations_file = os.path.join(DATA_DIR, 'locations.json')
    if request.method == 'GET':
        locations = []
        if os.path.exists(locations_file):
            try:
                with open(locations_file, 'r') as f: 
                    raw_locations = json.load(f)
                    # Normalize all locations to ensure consistent data structure
                    locations = [normalize_location_data(loc) for loc in raw_locations]
            except Exception as e: logger.error(f"API Error reading locations: {e}")
        return jsonify(locations)
    elif request.method == 'POST':
        try:
            location_data = request.get_json()
            if 'id' not in location_data or not location_data['id']:
                location_data['id'] = str(uuid.uuid4())
            
            # Validate coordinates before processing
            is_valid, error_msg = validate_coordinates(
                location_data.get('latitude'), 
                location_data.get('longitude')
            )
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            # Normalize the location data
            location_data = normalize_location_data(location_data)

            locations = []
            if os.path.exists(locations_file):
                 with open(locations_file, 'r') as f: locations = json.load(f)
            locations.append(location_data)
            with open(locations_file, 'w') as f: json.dump(locations, f, indent=2)
            return jsonify(location_data), 201
        except Exception as e:
             logger.error(f"API Error creating location: {e}")
             return jsonify({'error': str(e)}), 500


@api_bp.route('/locations/<location_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_location(location_id):
    """Get, update or delete a location"""
    locations_file = os.path.join(DATA_DIR, 'locations.json')
    if not os.path.exists(locations_file): return jsonify({'error': 'Locations file not found'}), 404
    try:
        with open(locations_file, 'r') as f: locations = json.load(f)
    except Exception as e:
        logger.error(f"API Error reading locations file: {e}")
        return jsonify({'error': 'Could not read locations data'}), 500

    location_index = next((i for i, loc in enumerate(locations) if loc.get('id') == location_id), None)
    if location_index is None: return jsonify({'error': 'Location not found'}), 404

    if request.method == 'GET':
        return jsonify(normalize_location_data(locations[location_index]))
    elif request.method == 'PUT':
        try:
            location_data = request.get_json()
            location_data['id'] = location_id # Ensure ID consistency
            
            # Validate coordinates before processing
            is_valid, error_msg = validate_coordinates(
                location_data.get('latitude'), 
                location_data.get('longitude')
            )
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            # Normalize the location data
            location_data = normalize_location_data(location_data)
            
            locations[location_index] = location_data
            with open(locations_file, 'w') as f: json.dump(locations, f, indent=2)
            return jsonify(location_data)
        except Exception as e:
             logger.error(f"API Error updating location {location_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            del locations[location_index]
            with open(locations_file, 'w') as f: json.dump(locations, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting location {location_id}: {e}")
             return jsonify({'error': str(e)}), 500


# --- Geocoding API Routes ---
@api_bp.route('/geocode', methods=['GET'])
@admin_required
def api_geocode():
    """Geocode an address or place name"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        limit = int(request.args.get('limit', 5))
        
        # Geocode the query
        results = geocode_address(query, limit)
        
        # Convert to JSON-serializable format
        response_data = []
        for result in results:
            response_data.append({
                'display_name': result.display_name,
                'latitude': result.latitude,
                'longitude': result.longitude,
                'city': result.city,
                'country': result.country,
                'formatted_address': result.formatted_address
            })
        
        return jsonify({
            'query': query,
            'results': response_data
        })
        
    except Exception as e:
        logger.error(f"Geocoding API error: {e}")
        return jsonify({'error': 'Geocoding service temporarily unavailable'}), 500

@api_bp.route('/popular-locations', methods=['GET'])
@admin_required
def api_popular_locations():
    """Get popular filming locations for quick selection"""
    try:
        locations = get_popular_film_locations()
        return jsonify(locations)
    except Exception as e:
        logger.error(f"Popular locations API error: {e}")
        return jsonify({'error': 'Could not load popular locations'}), 500


# --- Area API Routes ---
@api_bp.route('/areas', methods=['GET', 'POST'])
@admin_required
def api_areas():
    """List or create location areas"""
    areas_file = os.path.join(DATA_DIR, 'areas.json')
    if request.method == 'GET':
        areas = []
        if os.path.exists(areas_file):
             try:
                  with open(areas_file, 'r') as f: areas = json.load(f)
             except Exception as e: logger.error(f"API Error reading areas: {e}")
        return jsonify(areas)
    elif request.method == 'POST':
        try:
            area_data = request.get_json()
            if 'id' not in area_data or not area_data['id']:
                area_data['id'] = str(uuid.uuid4())
            areas = []
            if os.path.exists(areas_file):
                 with open(areas_file, 'r') as f: areas = json.load(f)
            areas.append(area_data)
            with open(areas_file, 'w') as f: json.dump(areas, f, indent=2)
            return jsonify(area_data), 201
        except Exception as e:
             logger.error(f"API Error creating area: {e}")
             return jsonify({'error': str(e)}), 500

@api_bp.route('/areas/<area_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_area(area_id):
    """Get, update or delete a location area"""
    areas_file = os.path.join(DATA_DIR, 'areas.json')
    if not os.path.exists(areas_file): return jsonify({'error': 'Areas file not found'}), 404
    try:
        with open(areas_file, 'r') as f: areas = json.load(f)
    except Exception as e:
        logger.error(f"API Error reading areas file: {e}")
        return jsonify({'error': 'Could not read areas data'}), 500

    area_index = next((i for i, area in enumerate(areas) if area.get('id') == area_id), None)
    if area_index is None: return jsonify({'error': 'Area not found'}), 404

    if request.method == 'GET':
        return jsonify(areas[area_index])
    elif request.method == 'PUT':
         try:
            area_data = request.get_json()
            area_data['id'] = area_id # Ensure ID
            areas[area_index] = area_data
            with open(areas_file, 'w') as f: json.dump(areas, f, indent=2)
            return jsonify(area_data)
         except Exception as e:
             logger.error(f"API Error updating area {area_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            # Add check: ensure area is not used by any location before deleting
            locations_file = os.path.join(DATA_DIR, 'locations.json')
            if os.path.exists(locations_file):
                 with open(locations_file, 'r') as f: locations = json.load(f)
                 if any(loc.get('areaId') == area_id for loc in locations):
                      return jsonify({'error': 'Cannot delete area, it is still assigned to locations.'}), 400

            del areas[area_index]
            with open(areas_file, 'w') as f: json.dump(areas, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting area {area_id}: {e}")
             return jsonify({'error': str(e)}), 500

# --- Department API Routes ---
@api_bp.route('/departments', methods=['GET', 'POST'])
@admin_required
def api_departments():
    """List or create departments"""
    departments_file = os.path.join(DATA_DIR, 'departments.json')
    if request.method == 'GET':
        departments = []
        if os.path.exists(departments_file):
            try:
                 with open(departments_file, 'r') as f: departments = json.load(f)
            except Exception as e: logger.error(f"API Error reading departments: {e}")
        return jsonify(departments)
    elif request.method == 'POST':
        try:
            department_data = request.get_json()
            if 'id' not in department_data or not department_data['id']:
                department_data['id'] = str(uuid.uuid4())
            departments = []
            if os.path.exists(departments_file):
                 with open(departments_file, 'r') as f: departments = json.load(f)
            departments.append(department_data)
            with open(departments_file, 'w') as f: json.dump(departments, f, indent=2)
            # Update counts across all projects
            update_all_projects_department_counts()
            return jsonify(department_data), 201
        except Exception as e:
             logger.error(f"API Error creating department: {e}")
             return jsonify({'error': str(e)}), 500

@api_bp.route('/departments/<department_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_department(department_id):
    """Get, update or delete a department"""
    departments_file = os.path.join(DATA_DIR, 'departments.json')
    if not os.path.exists(departments_file): return jsonify({'error': 'Departments file not found'}), 404
    try:
        with open(departments_file, 'r') as f: departments = json.load(f)
    except Exception as e:
        logger.error(f"API Error reading departments file: {e}")
        return jsonify({'error': 'Could not read departments data'}), 500

    department_index = next((i for i, dept in enumerate(departments) if dept.get('id') == department_id), None)
    if department_index is None: return jsonify({'error': 'Department not found'}), 404

    if request.method == 'GET':
        return jsonify(departments[department_index])
    elif request.method == 'PUT':
        try:
            department_data = request.get_json()
            department_data['id'] = department_id # Ensure ID
            departments[department_index] = department_data
            with open(departments_file, 'w') as f: json.dump(departments, f, indent=2)
            update_all_projects_department_counts()
            return jsonify(department_data)
        except Exception as e:
             logger.error(f"API Error updating department {department_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            # Add check: ensure department is not used? (More complex, involves checking all calendar.json files)
            # Skipping check for now for simplicity.
            del departments[department_index]
            with open(departments_file, 'w') as f: json.dump(departments, f, indent=2)
            update_all_projects_department_counts()
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting department {department_id}: {e}")
             return jsonify({'error': str(e)}), 500

# --- Special Dates API Routes (Weekends, Holidays, Hiatus, Other) ---
# --- Weekends ---
@api_bp.route('/projects/<project_id>/weekends', methods=['GET', 'POST'])
@admin_required
def api_weekends(project_id):
    """List or create working weekends for a project"""
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    weekends_file = os.path.join(project_dir, 'weekends.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404

    if request.method == 'GET':
        weekends = []
        if os.path.exists(weekends_file):
            try:
                 with open(weekends_file, 'r') as f: weekends = json.load(f)
            except Exception as e: logger.error(f"API Error reading weekends for {project_id}: {e}")
        return jsonify(weekends)
    elif request.method == 'POST':
        try:
            weekend_data = request.get_json()
            if not weekend_data or 'date' not in weekend_data: return jsonify({'error': 'Date is required'}), 400
            # Add validation for date format and day of week if needed
            if 'id' not in weekend_data or not weekend_data['id']: weekend_data['id'] = str(uuid.uuid4())

            weekends = []
            if os.path.exists(weekends_file):
                 with open(weekends_file, 'r') as f: weekends = json.load(f)

            # Avoid duplicates by date? Or allow multiple entries for same date? Assuming update/replace.
            existing_index = next((i for i, w in enumerate(weekends) if w.get('date') == weekend_data['date']), None)
            if existing_index is not None:
                 weekends[existing_index] = weekend_data # Update
            else:
                 weekends.append(weekend_data) # Add new

            with open(weekends_file, 'w') as f: json.dump(weekends, f, indent=2)
            # Regenerate calendar? Maybe not needed if generator checks this file.
            return jsonify(weekend_data), 201
        except Exception as e:
            logger.error(f"API Error creating weekend for {project_id}: {e}")
            return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/weekends/<weekend_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_weekend(project_id, weekend_id):
    """Get, update or delete a working weekend"""
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    weekends_file = os.path.join(project_dir, 'weekends.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if not os.path.exists(weekends_file): return jsonify({'error': 'No weekends file found'}), 404

    try:
        with open(weekends_file, 'r') as f: weekends = json.load(f)
    except Exception as e:
        logger.error(f"API Error reading weekends file for {project_id}: {e}")
        return jsonify({'error': 'Could not read weekends data'}), 500

    weekend_index = next((i for i, wknd in enumerate(weekends) if wknd.get('id') == weekend_id), None)
    if weekend_index is None: return jsonify({'error': 'Working weekend not found'}), 404

    if request.method == 'GET':
        return jsonify(weekends[weekend_index])
    elif request.method == 'PUT':
        try:
            weekend_data = request.get_json()
            weekend_data['id'] = weekend_id # Ensure ID
            weekends[weekend_index] = weekend_data
            with open(weekends_file, 'w') as f: json.dump(weekends, f, indent=2)
            return jsonify(weekend_data)
        except Exception as e:
            logger.error(f"API Error updating weekend {weekend_id} for {project_id}: {e}")
            return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            del weekends[weekend_index]
            with open(weekends_file, 'w') as f: json.dump(weekends, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting weekend {weekend_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500

# --- Holidays ---
@api_bp.route('/projects/<project_id>/holidays', methods=['GET', 'POST'])
@admin_required
def api_holidays(project_id):
    """List or create holidays"""
    # Similar structure to weekends GET/POST
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    holidays_file = os.path.join(project_dir, 'holidays.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if request.method == 'GET':
         holidays = []
         if os.path.exists(holidays_file):
              try:
                   with open(holidays_file, 'r') as f: holidays = json.load(f)
              except Exception as e: logger.error(f"API Error reading holidays for {project_id}: {e}")
         return jsonify(holidays)
    elif request.method == 'POST':
        try:
            holiday_data = request.get_json()
            if 'id' not in holiday_data or not holiday_data['id']: holiday_data['id'] = str(uuid.uuid4())
            holidays = []
            if os.path.exists(holidays_file):
                 with open(holidays_file, 'r') as f: holidays = json.load(f)
            holidays.append(holiday_data) # Assuming no duplicates check needed for simple add
            with open(holidays_file, 'w') as f: json.dump(holidays, f, indent=2)
            return jsonify(holiday_data), 201
        except Exception as e:
            logger.error(f"API Error creating holiday for {project_id}: {e}")
            return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>/holidays/<holiday_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_holiday(project_id, holiday_id):
    """Get, update, delete holiday"""
    # Similar structure to weekend GET/PUT/DELETE
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    holidays_file = os.path.join(project_dir, 'holidays.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if not os.path.exists(holidays_file): return jsonify({'error': 'No holidays file found'}), 404
    try:
        with open(holidays_file, 'r') as f: holidays = json.load(f)
    except Exception as e:
         logger.error(f"API Error reading holidays file for {project_id}: {e}")
         return jsonify({'error': 'Could not read holidays data'}), 500
    holiday_index = next((i for i, hol in enumerate(holidays) if hol.get('id') == holiday_id), None)
    if holiday_index is None: return jsonify({'error': 'Holiday not found'}), 404
    if request.method == 'GET': return jsonify(holidays[holiday_index])
    elif request.method == 'PUT':
        try:
            holiday_data = request.get_json()
            holiday_data['id'] = holiday_id
            holidays[holiday_index] = holiday_data
            with open(holidays_file, 'w') as f: json.dump(holidays, f, indent=2)
            return jsonify(holiday_data)
        except Exception as e:
             logger.error(f"API Error updating holiday {holiday_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            del holidays[holiday_index]
            with open(holidays_file, 'w') as f: json.dump(holidays, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting holiday {holiday_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500

# --- Hiatus ---
@api_bp.route('/projects/<project_id>/hiatus', methods=['GET', 'POST'])
@admin_required
def api_hiatus_periods(project_id):
    """List or create hiatus periods"""
    # Similar structure to weekends GET/POST
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    hiatus_file = os.path.join(project_dir, 'hiatus.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if request.method == 'GET':
         hiatus_periods = []
         if os.path.exists(hiatus_file):
              try:
                   with open(hiatus_file, 'r') as f: hiatus_periods = json.load(f)
              except Exception as e: logger.error(f"API Error reading hiatus for {project_id}: {e}")
         return jsonify(hiatus_periods)
    elif request.method == 'POST':
        try:
            hiatus_data = request.get_json()
            if 'id' not in hiatus_data or not hiatus_data['id']: hiatus_data['id'] = str(uuid.uuid4())
            hiatus_periods = []
            if os.path.exists(hiatus_file):
                 with open(hiatus_file, 'r') as f: hiatus_periods = json.load(f)
            hiatus_periods.append(hiatus_data)
            with open(hiatus_file, 'w') as f: json.dump(hiatus_periods, f, indent=2)
            return jsonify(hiatus_data), 201
        except Exception as e:
             logger.error(f"API Error creating hiatus for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/hiatus/<hiatus_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_hiatus_period(project_id, hiatus_id):
    """Get, update, delete hiatus"""
    # Similar structure to weekend GET/PUT/DELETE
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    hiatus_file = os.path.join(project_dir, 'hiatus.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if not os.path.exists(hiatus_file): return jsonify({'error': 'No hiatus file found'}), 404
    try:
        with open(hiatus_file, 'r') as f: hiatus_periods = json.load(f)
    except Exception as e:
        logger.error(f"API Error reading hiatus file for {project_id}: {e}")
        return jsonify({'error': 'Could not read hiatus data'}), 500
    hiatus_index = next((i for i, h in enumerate(hiatus_periods) if h.get('id') == hiatus_id), None)
    if hiatus_index is None: return jsonify({'error': 'Hiatus period not found'}), 404
    if request.method == 'GET': return jsonify(hiatus_periods[hiatus_index])
    elif request.method == 'PUT':
         try:
            hiatus_data = request.get_json()
            hiatus_data['id'] = hiatus_id
            hiatus_periods[hiatus_index] = hiatus_data
            with open(hiatus_file, 'w') as f: json.dump(hiatus_periods, f, indent=2)
            return jsonify(hiatus_data)
         except Exception as e:
             logger.error(f"API Error updating hiatus {hiatus_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            del hiatus_periods[hiatus_index]
            with open(hiatus_file, 'w') as f: json.dump(hiatus_periods, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting hiatus {hiatus_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500

# --- Other Special Dates ---
@api_bp.route('/projects/<project_id>/special-dates', methods=['GET', 'POST'])
@admin_required
def api_special_dates(project_id):
    """List or create special dates"""
    # Similar structure to weekends GET/POST
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    special_dates_file = os.path.join(project_dir, 'special_dates.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if request.method == 'GET':
         special_dates = []
         if os.path.exists(special_dates_file):
              try:
                   with open(special_dates_file, 'r') as f: special_dates = json.load(f)
              except Exception as e: logger.error(f"API Error reading special dates for {project_id}: {e}")
         return jsonify(special_dates)
    elif request.method == 'POST':
        try:
            special_date_data = request.get_json()
            if 'id' not in special_date_data or not special_date_data['id']: special_date_data['id'] = str(uuid.uuid4())
            special_dates = []
            if os.path.exists(special_dates_file):
                 with open(special_dates_file, 'r') as f: special_dates = json.load(f)
            special_dates.append(special_date_data)
            with open(special_dates_file, 'w') as f: json.dump(special_dates, f, indent=2)
            return jsonify(special_date_data), 201
        except Exception as e:
             logger.error(f"API Error creating special date for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>/special-dates/<special_date_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_special_date(project_id, special_date_id):
    """Get, update, delete special date"""
    # Similar structure to weekend GET/PUT/DELETE
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    special_dates_file = os.path.join(project_dir, 'special_dates.json')
    if not os.path.exists(project_dir): return jsonify({'error': 'Project not found'}), 404
    if not os.path.exists(special_dates_file): return jsonify({'error': 'No special dates file found'}), 404
    try:
        with open(special_dates_file, 'r') as f: special_dates = json.load(f)
    except Exception as e:
         logger.error(f"API Error reading special dates file for {project_id}: {e}")
         return jsonify({'error': 'Could not read special dates data'}), 500
    special_date_index = next((i for i, sd in enumerate(special_dates) if sd.get('id') == special_date_id), None)
    if special_date_index is None: return jsonify({'error': 'Special date not found'}), 404
    if request.method == 'GET': return jsonify(special_dates[special_date_index])
    elif request.method == 'PUT':
        try:
            special_date_data = request.get_json()
            special_date_data['id'] = special_date_id
            special_dates[special_date_index] = special_date_data
            with open(special_dates_file, 'w') as f: json.dump(special_dates, f, indent=2)
            return jsonify(special_date_data)
        except Exception as e:
             logger.error(f"API Error updating special date {special_date_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            del special_dates[special_date_index]
            with open(special_dates_file, 'w') as f: json.dump(special_dates, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
             logger.error(f"API Error deleting special date {special_date_id} for {project_id}: {e}")
             return jsonify({'error': str(e)}), 500

# Note: Serve static can stay in app.py or move to main_bp

# Add these new routes to your routes/api.py file after the existing routes

# --- Version API Routes ---
@api_bp.route('/projects/<project_id>/versions', methods=['GET'])
@admin_required
def api_project_versions(project_id):
    """List all versions for a project"""
    try:
        versions = get_project_versions(project_id)
        return jsonify(versions)
    except Exception as e:
        logger.error(f"Error getting versions for project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/versions/<version_id>', methods=['GET'])
@admin_required
def api_project_version(project_id, version_id):
    """Get a specific version"""
    try:
        versions = get_project_versions(project_id)
        version = next((v for v in versions if v['id'] == version_id), None)
        
        if not version:
            return jsonify({'error': 'Version not found'}), 404
            
        return jsonify(version)
    except Exception as e:
        logger.error(f"Error getting version {version_id} for project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/versions', methods=['POST'])
@admin_required
def api_create_project_version(project_id):
    """Create a new version from current workspace"""
    try:
        data = request.get_json()
        version_number = data.get('versionNumber')
        notes = data.get('notes', '')
        
        if not version_number:
            return jsonify({'error': 'Version number is required'}), 400
            
        # Check if version number already exists
        existing_versions = get_project_versions(project_id)
        if any(v['versionNumber'] == version_number for v in existing_versions):
            return jsonify({'error': 'Version number already exists'}), 400
            
        new_version = create_project_version(project_id, version_number, notes)
        
        if not new_version:
            return jsonify({'error': 'Failed to create version'}), 500
            
        return jsonify(new_version), 201
        
    except Exception as e:
        logger.error(f"Error creating version for project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/versions/<version_id>/publish', methods=['POST'])
@admin_required
def api_publish_project_version(project_id, version_id):
    """Publish a specific version and generate access codes"""
    try:
        from utils.access_manager import ProjectAccessManager
        
        user_id = session.get('user_id')
        
        # First publish the version using existing system
        success = publish_project_version(project_id, version_id, user_id)
        
        if not success:
            return jsonify({'error': 'Failed to publish version'}), 500
        
        # Get project and calendar data for public access
        project = get_project(project_id, user_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
            
        # Get the published calendar data
        calendar_data = get_project_calendar(project_id, user_id)
        if not calendar_data:
            return jsonify({'error': 'No calendar data found'}), 404
        
        # Generate public access codes
        access_manager = ProjectAccessManager()
        access_info = access_manager.publish_calendar_with_access(
            user_id, project_id, calendar_data, project
        )
        
        return jsonify({
            'success': True, 
            'published': True,
            'access_info': {
                'access_code': access_info['access_code'],
                'access_token': access_info['access_token'],
                'share_url': f"/calendar/{access_info['access_token']}"
            }
        })
        
    except Exception as e:
        logger.error(f"Error publishing version {version_id} for project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/workspace', methods=['GET'])
@admin_required
def api_get_workspace(project_id):
    """Get current workspace"""
    try:
        from flask import session
        user_id = session.get('user_id')
        workspace = get_project_workspace(project_id, user_id)
        
        if not workspace:
            return jsonify({'error': 'No workspace found'}), 404
            
        return jsonify(workspace)
        
    except Exception as e:
        logger.error(f"Error getting workspace for project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/workspace', methods=['PUT'])
@admin_required
def api_update_workspace(project_id):
    """Update workspace calendar data"""
    try:
        from flask import session
        user_id = session.get('user_id')
        data = request.get_json()
        workspace = get_project_workspace(project_id, user_id)
        
        if not workspace:
            return jsonify({'error': 'No workspace found'}), 404
            
        # Update only the calendar data
        workspace['calendarData'] = data
        
        success = save_project_workspace(project_id, workspace, user_id)
        
        if not success:
            return jsonify({'error': 'Failed to save workspace'}), 500
            
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error updating workspace for project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/projects/<project_id>/migrate-to-versioned', methods=['POST'])
@admin_required
def api_migrate_project(project_id):
    """Migrate a project to versioned structure"""
    try:
        from flask import session
        user_id = session.get('user_id')
        success = migrate_project_to_versioned_structure(project_id, user_id)
        
        if not success:
            return jsonify({'error': 'Failed to migrate project'}), 500
            
        return jsonify({'success': True, 'migrated': True})
        
    except Exception as e:
        logger.error(f"Error migrating project {project_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/calculate-sun-times', methods=['POST'])
@admin_required
def api_calculate_sun_times():
    """Calculate sunrise/sunset times for a location and date"""
    try:
        from utils.sun_utils_simple import get_sun_times_for_location
        from datetime import datetime
        
        data = request.get_json()
        location_name = data.get('location_name')
        date_str = data.get('date')
        
        if not location_name or not date_str:
            return jsonify({'error': 'location_name and date are required'}), 400
        
        # Load locations to find coordinates
        locations_file = os.path.join(DATA_DIR, 'locations.json')
        if not os.path.exists(locations_file):
            return jsonify({'error': 'No locations file found'}), 404
            
        with open(locations_file, 'r') as f:
            locations = json.load(f)
        
        # Find the location
        location_data = None
        for loc in locations:
            if loc.get('name') == location_name:
                location_data = loc
                break
        
        if not location_data:
            return jsonify({'error': f'Location "{location_name}" not found'}), 404
        
        # Check if location has coordinates
        if not location_data.get('latitude') or not location_data.get('longitude'):
            return jsonify({'error': f'Location "{location_name}" has no coordinates'}), 400
        
        # Parse date
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Calculate sun times
        sun_times = get_sun_times_for_location(location_data, date_obj)
        
        if sun_times:
            return jsonify({
                'success': True,
                'sunrise': sun_times.get('sunrise'),
                'sunset': sun_times.get('sunset'),
                'location': location_name,
                'date': date_str
            })
        else:
            return jsonify({'error': 'Failed to calculate sun times'}), 500
            
    except Exception as e:
        logger.error(f"Error calculating sun times: {str(e)}")
        return jsonify({'error': str(e)}), 500
