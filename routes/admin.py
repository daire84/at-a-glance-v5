# routes/admin.py
import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from utils.decorators import admin_required
from utils.helpers import (
    get_projects, get_project, save_project, get_project_calendar, 
    save_project_calendar, generate_calendar, DATA_DIR, logger, 
    recalculate_shoot_days, save_project_workspace, get_project_workspace,
    update_day_from_form
)
from utils.calendar_generator import calculate_department_counts, calculate_location_counts
from utils.access_manager import ProjectAccessManager

# Define Blueprint: Set url_prefix and template_folder
admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates/admin')

# Initialize access manager
access_manager = ProjectAccessManager()

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    user_id = session.get('user_id')
    projects = get_projects(user_id)
    # Renders 'admin/dashboard.html' because of template_folder
    return render_template('dashboard.html', projects=projects)

@admin_bp.route('/project/<project_id>', methods=['GET', 'POST'])
@admin_required
def admin_project(project_id):
    """Project details editor"""
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            if project_id != 'new':
                project = get_project(project_id, user_id)
                if not project:
                    flash('Project not found', 'error')
                    return redirect(url_for('admin.admin_dashboard'))
                original_dates = { # Store original dates
                    'prepStartDate': project.get('prepStartDate'),
                    'shootStartDate': project.get('shootStartDate'),
                    'wrapDate': project.get('wrapDate')
                }
            else:
                import uuid # Import uuid locally
                project = {'id': str(uuid.uuid4())}
                original_dates = {}

            for key, value in form_data.items():
                project[key] = value

            save_project(project, user_id) # Save the updated project data

            dates_changed = (
                project_id == 'new' or
                original_dates.get('prepStartDate') != project.get('prepStartDate') or
                original_dates.get('shootStartDate') != project.get('shootStartDate') or
                original_dates.get('wrapDate') != project.get('wrapDate')
            )

            if project_id == 'new':
                generate_calendar(project)
                flash('Project created and calendar generated successfully', 'success')
            elif dates_changed and request.form.get('regenerate_calendar') == 'yes':
                generate_calendar(project)
                flash('Project updated and calendar regenerated successfully', 'success')
            else:
                 flash('Project updated successfully', 'success')

            # Redirect to the admin calendar view for this project
            return redirect(url_for('admin.admin_calendar', project_id=project['id']))

        except Exception as e:
            logger.error(f"Error saving project: {str(e)}")
            flash(f'Error saving project: {str(e)}', 'error')
            # Fall through to render the form again

    # GET request or if POST had an error
    project = get_project(project_id, user_id) if project_id != 'new' else {}
    # Renders 'admin/project.html'
    return render_template('project.html', project=project)


@admin_bp.route('/calendar/<project_id>')
@admin_required # Apply decorator
def admin_calendar(project_id):
    """Calendar editor"""
    user_id = session.get('user_id')
    
    try:
        project = get_project(project_id, user_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin.admin_dashboard'))

        # Ensure project has isVersioned property
        if 'isVersioned' not in project:
            project['isVersioned'] = False
            
            # Also save this change back to the file
            try:
                save_project(project, user_id)
                logger.info(f"Added missing isVersioned property to project {project_id}")
            except Exception as e:
                logger.error(f"Failed to save updated project with isVersioned: {str(e)}")

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
                departments = []  # Ensure departments is always a list

        locations = []
        locations_file = os.path.join(DATA_DIR, 'locations.json')
        if os.path.exists(locations_file):
            try:
                with open(locations_file, 'r') as f:
                    locations = json.load(f)
            except Exception as e:
                logger.error(f"Error loading locations: {str(e)}")
                locations = []  # Ensure locations is always a list

        areas = []
        areas_file = os.path.join(DATA_DIR, 'areas.json')
        if os.path.exists(areas_file):
            try:
                with open(areas_file, 'r') as f:
                    areas = json.load(f)
            except Exception as e:
                logger.error(f"Error loading areas in admin_calendar route: {str(e)}")
                areas = []  # Ensure areas is always a list
        # --- End Load supporting data ---

        # Ensure calendar_data is properly structured
        if not isinstance(calendar_data, dict):
            calendar_data = {"days": []}
        if "days" not in calendar_data:
            calendar_data["days"] = []

        # Ensure the latest supporting data is available in the calendar_data object
        calendar_data['departments'] = departments
        calendar_data['locationAreas'] = areas # Add/overwrite with the fresh list

        # Calculate counts safely
        try:
            calendar_data = calculate_department_counts(calendar_data)
            calendar_data = calculate_location_counts(calendar_data)
        except Exception as e:
            logger.error(f"Error calculating counts: {str(e)}")

        # Renders 'admin/calendar.html' - Corrected template path!
        return render_template('admin/calendar.html', project=project, calendar=calendar_data, locations=locations)
    
    except Exception as e:
        logger.error(f"Error in admin_calendar for project {project_id}: {str(e)}")
        flash(f'Error loading calendar: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))

# Update to routes/admin.py - Replace the existing admin_day function

@admin_bp.route('/day/<project_id>/<date>', methods=['GET', 'POST'])
@admin_required
def admin_day(project_id, date):
    """Enhanced day editor with navigation"""
    from utils.helpers import update_day_from_form, save_project_workspace, get_project_workspace
    from utils.calendar_generator import update_calendar_with_location_areas

    user_id = session.get('user_id')  # Extract user_id for proper project scoping
    project = get_project(project_id, user_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('admin.admin_dashboard'))

    calendar_data = get_project_calendar(project_id, user_id)
    day_index = next((i for i, d in enumerate(calendar_data.get('days', [])) if d.get('date') == date), None)

    if day_index is None:
        flash('Day not found', 'error')
        return redirect(url_for('admin.admin_calendar', project_id=project_id))

    day = calendar_data['days'][day_index]

    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()

            # Check if this is an AJAX save request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

            # --- Update locationArea based on selected location ---
            if 'location' in form_data and form_data['location']:
                selected_location_name = form_data['location']
                # Load locations and areas to find the area ID and name
                locations_list = []
                loc_file = os.path.join(DATA_DIR, 'locations.json')
                if os.path.exists(loc_file):
                    with open(loc_file, 'r') as f: 
                        locations_list = json.load(f)

                areas_list = []
                area_file = os.path.join(DATA_DIR, 'areas.json')
                if os.path.exists(area_file):
                     with open(area_file, 'r') as f: 
                         areas_list = json.load(f)

                area_id_found = None
                for loc in locations_list:
                    if loc['name'] == selected_location_name:
                        area_id_found = loc.get('areaId')
                        break

                if area_id_found:
                    area_name_found = None
                    for area in areas_list:
                        if area['id'] == area_id_found:
                            area_name_found = area.get('name')
                            break
                    if area_name_found:
                         form_data['locationArea'] = area_name_found
                         form_data['locationAreaId'] = area_id_found
                    else:
                         form_data['locationArea'] = None
                         form_data['locationAreaId'] = None
                else:
                     form_data['locationArea'] = None
                     form_data['locationAreaId'] = None
            else:
                form_data['locationArea'] = None
                form_data['locationAreaId'] = None
            # --- End Update locationArea ---

            # Update the day object using the helper function
            calendar_data['days'][day_index] = update_day_from_form(day, form_data)
            updated_day = calendar_data['days'][day_index]

            # Check if day type needs updating (e.g., Prep -> Shoot)
            if updated_day.get('isPrep', False) and not updated_day.get('isShootDay', False):
                shoot_start_date = datetime.strptime(project['shootStartDate'], "%Y-%m-%d").date()
                current_day_date = datetime.strptime(updated_day['date'], "%Y-%m-%d").date()
                is_shoot_period = current_day_date >= shoot_start_date

                if is_shoot_period and (updated_day.get('mainUnit') or updated_day.get('sequence')):
                    updated_day['isPrep'] = False
                    updated_day['isShootDay'] = True
                    calendar_data['days'] = recalculate_shoot_days(calendar_data['days'])

            # Recalculate counts and sun times before saving
            calendar_data = calculate_department_counts(calendar_data)
            calendar_data = calculate_location_counts(calendar_data)
            
            # Calculate sun times for days with locations
            from utils.calendar_generator import calculate_sun_times_for_calendar
            calendar_data = calculate_sun_times_for_calendar(calendar_data)

            # Save the calendar
            if project.get('isVersioned'):
                workspace = get_project_workspace(project_id, user_id)
                if workspace:
                    workspace['calendarData'] = calendar_data
                    save_project_workspace(project_id, workspace, user_id)
                    logger.info(f"Saved calendar to workspace for versioned project {project_id}")
                else:
                    logger.warning(f"Workspace not found for versioned project {project_id}, using regular save")
                    save_project_calendar(project_id, calendar_data, user_id)
            else:
                save_project_calendar(project_id, calendar_data, user_id)
                logger.info(f"Saved calendar for non-versioned project {project_id}")

            # For AJAX requests, return JSON response
            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': 'Day updated successfully',
                    'day': updated_day
                })
            else:
                # For regular form submissions, check if it's save & exit
                if 'save_exit' in request.form:
                    flash('Day updated successfully', 'success')
                    # Redirect back to calendar with anchor
                    return redirect(url_for('admin.admin_calendar', project_id=project_id) + f'#day-{date}')
                else:
                    # Stay on the same page for "save & stay"
                    flash('Day updated successfully', 'success')
                    return redirect(url_for('admin.admin_day', project_id=project_id, date=date))

        except Exception as e:
            logger.error(f"Error updating day {date} for project {project_id}: {str(e)}")
            
            # For AJAX requests, return error JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': f'Error updating day: {str(e)}'
                }), 500
            else:
                flash(f'Error updating day: {str(e)}', 'error')
                # Fall through to render form again

    # GET request or POST error - render the enhanced day editor
    # Pass calendar data for navigation
    return render_template('admin/day.html', 
                         project=project, 
                         day=day,
                         calendar_data=calendar_data)

@admin_bp.route('/locations')
@admin_required
def admin_locations():
    """Location management page"""
    # Renders 'admin/locations.html'
    # Data is loaded client-side via API calls in the template's JS
    return render_template('locations.html')

@admin_bp.route('/departments')
@admin_required
def admin_departments():
    """Department management page"""
    # Renders 'admin/departments.html'
    # Data is loaded client-side via API calls in the template's JS
    return render_template('departments.html')

@admin_bp.route('/dates')
@admin_bp.route('/dates/<project_id>')
@admin_required
def admin_dates(project_id=None):
    """Special dates management page"""
    user_id = session.get('user_id')  # <-- ADD THIS LINE
    projects = get_projects(user_id)  # <-- ADD user_id parameter
    # Renders 'admin/dates.html'
    return render_template('dates.html', projects=projects, project_id=project_id)

@admin_bp.route('/help')
@admin_required
def admin_help():
    """Help and documentation page"""
    # Renders unified help page instead of admin-specific one
    return render_template('help.html')

# === PUBLIC SHARING ROUTES ===

@admin_bp.route('/project/<project_id>/publish', methods=['POST'])
@admin_required
def publish_project(project_id):
    """Publish project calendar with public access generation"""
    user_id = session.get('user_id')
    
    try:
        # Get project and calendar data
        project = get_project(project_id, user_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin.admin_dashboard'))
        
        # Get calendar data - check if versioned
        if project.get('isVersioned'):
            workspace = get_project_workspace(project_id, user_id)
            if not workspace or 'calendarData' not in workspace:
                flash('No calendar data found in workspace', 'error')
                return redirect(url_for('admin.admin_calendar', project_id=project_id))
            calendar_data = workspace['calendarData']
        else:
            calendar_data = get_project_calendar(project_id, user_id)
            if not calendar_data:
                flash('No calendar data found', 'error')
                return redirect(url_for('admin.admin_calendar', project_id=project_id))
        
        # Get version info from form
        version_number = request.form.get('version_number', '1.0')
        version_notes = request.form.get('notes', '')
        
        # Create and publish version if versioned project
        if project.get('isVersioned'):
            from utils.helpers import create_project_version, publish_project_version
            
            # Create new version from workspace
            new_version = create_project_version(project_id, version_number, version_notes, user_id)
            if new_version:
                # Publish the newly created version
                publish_success = publish_project_version(project_id, new_version['id'], user_id)
                if not publish_success:
                    flash('Version created but failed to publish', 'warning')
            else:
                flash('Failed to create version', 'error')
                return redirect(url_for('admin.admin_calendar', project_id=project_id))
        
        # Publish calendar with public access
        access_info = access_manager.publish_calendar_with_access(
            user_id, project_id, calendar_data, project
        )
        
        flash('Calendar published successfully!', 'success')
        return render_template('admin/publish_success.html',
                             project=project,
                             access_info=access_info,
                             version_number=version_number)
    
    except Exception as e:
        logger.error(f"Error publishing project {project_id}: {str(e)}")
        flash(f'Error publishing calendar: {str(e)}', 'error')
        return redirect(url_for('admin.admin_calendar', project_id=project_id))

@admin_bp.route('/project/<project_id>/access')
@admin_required
def manage_project_access(project_id):
    """Manage public access settings for project"""
    user_id = session.get('user_id')
    
    try:
        project = get_project(project_id, user_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin.admin_dashboard'))
        
        # Get access information
        access_info = access_manager.get_project_access_info(user_id, project_id)
        
        return render_template('admin/project_access.html',
                             project=project,
                             access_info=access_info)
    
    except Exception as e:
        logger.error(f"Error managing access for project {project_id}: {str(e)}")
        flash(f'Error loading access settings: {str(e)}', 'error')
        return redirect(url_for('admin.admin_calendar', project_id=project_id))

@admin_bp.route('/project/<project_id>/access/revoke', methods=['POST'])
@admin_required
def revoke_project_access(project_id):
    """Revoke public access for project"""
    user_id = session.get('user_id')
    
    try:
        project = get_project(project_id, user_id)
        if not project:
            flash('Project not found', 'error')
            return redirect(url_for('admin.admin_dashboard'))
        
        # Revoke access
        success = access_manager.revoke_access(user_id, project_id)
        
        if success:
            flash('Public access revoked successfully', 'success')
        else:
            flash('No public access found to revoke', 'warning')
        
        return redirect(url_for('admin.manage_project_access', project_id=project_id))
    
    except Exception as e:
        logger.error(f"Error revoking access for project {project_id}: {str(e)}")
        flash(f'Error revoking access: {str(e)}', 'error')
        return redirect(url_for('admin.manage_project_access', project_id=project_id))

@admin_bp.route('/access/stats')
@admin_required
def access_statistics():
    """View access statistics for user's projects"""
    user_id = session.get('user_id')
    
    try:
        stats = access_manager.get_access_statistics(user_id)
        return render_template('admin/access_stats.html', stats=stats)
    
    except Exception as e:
        logger.error(f"Error loading access statistics: {str(e)}")
        flash(f'Error loading statistics: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))