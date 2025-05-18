# utils/helpers.py
import os
import json
import uuid
import logging
import shutil
from datetime import datetime
# Import necessary functions from calendar_generator directly
# Adjust based on actual functions needed by these helpers
from .calendar_generator import generate_calendar_days, calculate_department_counts

# Define Constants relative to this file's location
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTILS_DIR) # Project root (/app)
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROJECTS_DIR = os.path.join(DATA_DIR, 'projects')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
VERSIONS_FILE = 'versions.json'
WORKSPACE_FILE = 'workspace.json'
VERSION_DATA_DIR = 'versions'

# Setup logger for helpers
logger = logging.getLogger(__name__)

# --- Helper Functions ---

def get_projects():
    """Get all projects"""
    projects = []
    try:
        if os.path.exists(PROJECTS_DIR):
            for project_id in os.listdir(PROJECTS_DIR):
                project_dir = os.path.join(PROJECTS_DIR, project_id)
                if os.path.isdir(project_dir):
                    main_file = os.path.join(project_dir, 'main.json')
                    if os.path.exists(main_file):
                        try:
                            with open(main_file, 'r', encoding='utf-8') as f:
                                project = json.load(f)
                                projects.append(project)
                        except json.JSONDecodeError:
                            logger.error(f"Error decoding JSON for project {project_id}")
                        except Exception as inner_e:
                             logger.error(f"Error reading main.json for project {project_id}: {str(inner_e)}")

        return sorted(projects, key=lambda x: x.get('updated', ''), reverse=True)
    except Exception as e:
        logger.error(f"Error listing projects directory: {str(e)}")
        return []

def get_project(project_id):
    """Get a specific project"""
    if not project_id or project_id == 'new': # Handle 'new' case explicitly
        return None
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        main_file = os.path.join(project_dir, 'main.json')
        if os.path.exists(main_file):
            with open(main_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        logger.warning(f"Project main.json not found for ID: {project_id}")
        return None
    except Exception as e:
        logger.error(f"Error getting project {project_id}: {str(e)}")
        return None

def save_project(project):
    """Save a project"""
    try:
        project_id = project.get('id')
        if not project_id:
            project_id = str(uuid.uuid4())
            project['id'] = project_id

        # Always set isVersioned to true for all projects
        project['isVersioned'] = True

        # Rest of the function remains the same...
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        os.makedirs(project_dir, exist_ok=True)

        now = datetime.utcnow().isoformat() + 'Z'
        if 'created' not in project or not project['created']:
            project['created'] = now
        project['updated'] = now

        main_file = os.path.join(project_dir, 'main.json')
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(project, f, indent=2, ensure_ascii=False)

        logger.info(f"Project {project_id} saved successfully")
        return project
    except Exception as e:
        logger.error(f"Error saving project {project.get('id', 'N/A')}: {str(e)}")
        raise # Re-raise the exception so route can handle it

# Update the existing get_project_calendar function to use workspace
def get_project_calendar(project_id):
    """
    Get calendar data for a project (from workspace)
    """
    workspace = get_project_workspace(project_id)
    if workspace:
        return workspace.get('calendarData', {"days": []})
    else:
        # Fallback to existing behavior for non-versioned projects
        try:
            project_dir = os.path.join(PROJECTS_DIR, project_id)
            calendar_file = os.path.join(project_dir, 'calendar.json')

            if os.path.exists(calendar_file):
                with open(calendar_file, 'r') as f:
                    return json.load(f)
            return {"days": []}
        except Exception as e:
            logger.error(f"Error getting calendar for project {project_id}: {str(e)}")
            return {"days": []}

# Update the save_project_calendar function to save to workspace
def save_project_calendar(project_id, calendar_data):
    """Save calendar data for a project (to workspace)"""
    if not project_id:
        raise ValueError("Project ID is required to save calendar")
    try:
        # Check if project is versioned
        project = get_project(project_id)
        if project and project.get('isVersioned'):
            # Save to workspace
            workspace = get_project_workspace(project_id)
            if workspace:
                workspace['calendarData'] = calendar_data
                save_project_workspace(project_id, workspace)
                logger.info(f"Calendar data for project {project_id} saved to workspace")
                return calendar_data
        else:
            # Fallback to existing behavior for non-versioned projects
            project_dir = os.path.join(PROJECTS_DIR, project_id)
            os.makedirs(project_dir, exist_ok=True)
            calendar_file = os.path.join(project_dir, 'calendar.json')

            with open(calendar_file, 'w', encoding='utf-8') as f:
                json.dump(calendar_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Calendar data for project {project_id} saved successfully")
            return calendar_data
    except Exception as e:
        logger.error(f"Error saving calendar data for project {project_id}: {str(e)}")
        raise

def generate_calendar(project):
    """Generate calendar days based on project dates, preserving existing data"""
    if not project or not project.get('id'):
        logger.error("Cannot generate calendar, invalid project data provided.")
        return {"days": [], "error": "Invalid project data"}
    try:
        project_id = project['id']
        existing_calendar = get_project_calendar(project_id)
        # generate_calendar_days is imported from .calendar_generator
        calendar_data = generate_calendar_days(project, existing_calendar)
        # Todo: Enhance generate_calendar_days to robustly merge/update area info
        return save_project_calendar(project_id, calendar_data)
    except Exception as e:
        logger.error(f"Error generating calendar for project {project.get('id', 'N/A')}: {str(e)}")
        return {"days": [], "error": f"Failed to generate calendar: {str(e)}"}


def update_day_from_form(day, form_data):
    """
    Update a day object with data from the submitted form (used by admin_day route)
    """
    if not isinstance(day, dict) or not isinstance(form_data, dict):
         logger.error("Invalid input for update_day_from_form")
         return day # Or raise error

    try:
        # Update string fields safely using .get()
        for field in ['mainUnit', 'sequence', 'location', 'locationArea', 'notes', 'secondUnit', 'secondUnitLocation']:
            day[field] = form_data.get(field, day.get(field)) # Keep old value if not in form

        # Handle numeric fields safely
        for field in ['extras', 'featuredExtras']:
            value_str = form_data.get(field)
            if value_str is not None: # Check if key exists in form
                 try:
                      day[field] = int(value_str) if value_str else 0
                 except (ValueError, TypeError):
                      day[field] = 0 # Default to 0 if conversion fails
                      logger.warning(f"Could not convert {field} value '{value_str}' to int.")

        # Handle departments list
        if 'departments' in form_data:
            dept_str = form_data.get('departments', '')
            if isinstance(dept_str, str):
                day['departments'] = [d.strip() for d in dept_str.split(',') if d.strip()]
            elif isinstance(dept_str, list): # Already a list?
                 day['departments'] = [str(d).strip() for d in dept_str if str(d).strip()]
            else:
                 day['departments'] = []
        # Only update if key doesn't exist, otherwise keep current
        elif 'departments' not in day:
             day['departments'] = []


        # Add locationAreaId if it was calculated in the route
        # Use .get() to avoid KeyError if not passed
        day['locationAreaId'] = form_data.get('locationAreaId', day.get('locationAreaId'))

        return day

    except Exception as e:
        logger.error(f"Error updating day object from form: {str(e)}")
        return day # Return original day on error


def save_day_changes(project_id, date, form_data):
    """
    Save changes to a calendar day - DEPRECATED?
    Logic seems covered by admin_day route which calls save_project_calendar
    """
    logger.warning("save_day_changes helper function called - check if necessary.")
    try:
        calendar_data = get_project_calendar(project_id)
        day_index = next((i for i, d in enumerate(calendar_data.get('days', [])) if d.get('date') == date), None)
        if day_index is None:
            logger.error(f"Day not found for saving via helper: {date}")
            return False
        # Assume day object was already updated before calling this
        save_project_calendar(project_id, calendar_data)
        return True
    except Exception as e:
        logger.error(f"Error in save_day_changes helper for {date}: {str(e)}")
        return False

def recalculate_shoot_days(days):
    """
    Recalculate shoot day numbers based on chronological order
    """
    if not isinstance(days, list): return [] # Handle invalid input
    try:
        # Ensure dates are valid before sorting
        valid_days = []
        for d in days:
            if d.get('date'):
                 try:
                      datetime.strptime(d['date'], '%Y-%m-%d') # Validate format
                      valid_days.append(d)
                 except ValueError:
                      logger.warning(f"Invalid date format skipped in recalculate_shoot_days: {d.get('date')}")
            else:
                 logger.warning("Day missing date skipped in recalculate_shoot_days")

        valid_days.sort(key=lambda d: d['date'])

        shoot_day = 0
        for day in valid_days:
            # Ensure isShootDay exists and is boolean-like
            is_shoot = day.get('isShootDay', False)
            if is_shoot: # Check for truthiness
                shoot_day += 1
                day['shootDay'] = shoot_day
            else:
                day['shootDay'] = None # Use None instead of empty string or 0

        return valid_days # Return the sorted, updated list
    except Exception as e:
        logger.error(f"Error recalculating shoot days: {str(e)}")
        return days # Return original list on error

def update_all_projects_department_counts():
    """Update department counts in all project calendars"""
    try:
        projects = get_projects()
        for project in projects:
            project_id = project.get('id')
            if project_id:
                calendar_data = get_project_calendar(project_id)
                if calendar_data and 'days' in calendar_data:
                    # calculate_department_counts is imported from .calendar_generator
                    calendar_data = calculate_department_counts(calendar_data)
                    save_project_calendar(project_id, calendar_data)
                    logger.info(f"Updated department counts for project {project_id}")
    except Exception as e:
        logger.error(f"Error updating all department counts: {str(e)}")

# --- Global Data Loaders (Example for locations/areas/departments) ---
# Consider placing these here or in a dedicated data_loader util file

def load_global_data(filename, default=[]):
    """Helper to load global JSON data like areas.json, locations.json"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading global data file {filename}: {e}")
    return default

def save_global_data(filename, data):
    """Helper to save global JSON data"""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Global data file {filename} saved successfully.")
    except Exception as e:
        logger.error(f"Error saving global data file {filename}: {e}")
        raise # Re-raise exception

def migrate_project_to_versioned_structure(project_id):
    """
    Migrate an existing project to the new versioned structure
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        if not os.path.exists(project_dir):
            logger.error(f"Project directory not found: {project_id}")
            return False
            
        # Load existing project data
        main_file = os.path.join(project_dir, 'main.json')
        calendar_file = os.path.join(project_dir, 'calendar.json')
        
        if not os.path.exists(main_file):
            logger.error(f"Project main.json not found: {project_id}")
            return False
            
        with open(main_file, 'r') as f:
            project_data = json.load(f)
            
        # Load existing calendar data if it exists
        calendar_data = {}
        if os.path.exists(calendar_file):
            with open(calendar_file, 'r') as f:
                calendar_data = json.load(f)
                
        # Create version structure
        version_id = str(uuid.uuid4())
        version_data = {
            "id": version_id,
            "versionNumber": "1.0",
            "notes": "Initial version (migrated from v4)",
            "createdAt": datetime.utcnow().isoformat() + 'Z',
            "publishedAt": datetime.utcnow().isoformat() + 'Z',
            "isPublished": True,
            "isLatestPublished": True
        }
        
        # Create versions file
        versions_file = os.path.join(project_dir, 'versions.json')
        versions_data = {
            "versions": [
                {
                    **version_data,
                    "calendarData": calendar_data
                }
            ],
            "latestPublishedId": version_id
        }
        
        with open(versions_file, 'w') as f:
            json.dump(versions_data, f, indent=2)
            
        # Create workspace file from current calendar data
        workspace_file = os.path.join(project_dir, 'workspace.json')
        workspace_data = {
            "baseVersionId": version_id,
            "lastModified": datetime.utcnow().isoformat() + 'Z',
            "calendarData": calendar_data,
            "isDraft": False
        }
        
        with open(workspace_file, 'w') as f:
            json.dump(workspace_data, f, indent=2)
            
        # Update project metadata to indicate versioned structure
        project_data['isVersioned'] = True
        project_data['currentWorkspaceVersion'] = version_id
        
        with open(main_file, 'w') as f:
            json.dump(project_data, f, indent=2)
            
        logger.info(f"Successfully migrated project {project_id} to versioned structure")
        return True
        
    except Exception as e:
        logger.error(f"Error migrating project {project_id}: {str(e)}")
        return False


def get_project_versions(project_id):
    """
    Get all versions for a project
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        versions_file = os.path.join(project_dir, 'versions.json')
        
        if not os.path.exists(versions_file):
            return []
            
        with open(versions_file, 'r') as f:
            data = json.load(f)
            
        return data.get('versions', [])
        
    except Exception as e:
        logger.error(f"Error getting versions for project {project_id}: {str(e)}")
        return []


def get_project_workspace(project_id):
    """
    Get the current workspace for a project
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        workspace_file = os.path.join(project_dir, 'workspace.json')
        
        if not os.path.exists(workspace_file):
            # If no workspace exists, try to create one from calendar.json
            calendar_file = os.path.join(project_dir, 'calendar.json')
            if os.path.exists(calendar_file):
                with open(calendar_file, 'r') as f:
                    calendar_data = json.load(f)
                    
                workspace_data = {
                    "baseVersionId": None,
                    "lastModified": datetime.utcnow().isoformat() + 'Z',
                    "calendarData": calendar_data,
                    "isDraft": True
                }
                
                with open(workspace_file, 'w') as f:
                    json.dump(workspace_data, f, indent=2)
                    
                return workspace_data
            else:
                return {
                    "baseVersionId": None,
                    "lastModified": datetime.utcnow().isoformat() + 'Z',
                    "calendarData": {"days": []},
                    "isDraft": True
                }
                
        with open(workspace_file, 'r') as f:
            return json.load(f)
            
    except Exception as e:
        logger.error(f"Error getting workspace for project {project_id}: {str(e)}")
        return None


def save_project_workspace(project_id, workspace_data):
    """
    Save the workspace for a project
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        workspace_file = os.path.join(project_dir, 'workspace.json')
        
        # Update last modified timestamp
        workspace_data['lastModified'] = datetime.utcnow().isoformat() + 'Z'
        workspace_data['isDraft'] = True
        
        with open(workspace_file, 'w') as f:
            json.dump(workspace_data, f, indent=2)
            
        logger.info(f"Saved workspace for project {project_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving workspace for project {project_id}: {str(e)}")
        return False


def create_project_version(project_id, version_number, notes=None):
    """
    Create a new version from the current workspace
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        versions_file = os.path.join(project_dir, 'versions.json')
        workspace_file = os.path.join(project_dir, 'workspace.json')
        
        # Get current workspace
        if not os.path.exists(workspace_file):
            logger.error(f"No workspace found for project {project_id}")
            return None
            
        with open(workspace_file, 'r') as f:
            workspace_data = json.load(f)
            
        # Get existing versions
        versions_data = {"versions": [], "latestPublishedId": None}
        if os.path.exists(versions_file):
            with open(versions_file, 'r') as f:
                versions_data = json.load(f)
                
        # Check if version number already exists
        for version in versions_data['versions']:
            if version.get('versionNumber') == version_number:
                logger.error(f"Version {version_number} already exists for project {project_id}")
                return None
                
        # Create new version
        version_id = str(uuid.uuid4())
        new_version = {
            "id": version_id,
            "versionNumber": version_number,
            "notes": notes or "",
            "createdAt": datetime.utcnow().isoformat() + 'Z',
            "publishedAt": None,
            "isPublished": False,
            "isLatestPublished": False,
            "calendarData": workspace_data.get('calendarData', {})
        }
        
        # Add to versions list
        versions_data['versions'].append(new_version)
        
        # Save versions file
        with open(versions_file, 'w') as f:
            json.dump(versions_data, f, indent=2)
            
        # Update workspace to reference this version
        workspace_data['baseVersionId'] = version_id
        workspace_data['isDraft'] = False
        save_project_workspace(project_id, workspace_data)
        
        logger.info(f"Created version {version_number} for project {project_id}")
        return new_version
        
    except Exception as e:
        logger.error(f"Error creating version for project {project_id}: {str(e)}")
        return None

def publish_project_version(project_id, version_id):
    """
    Publish a specific version of a project
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        versions_file = os.path.join(project_dir, 'versions.json')
        
        if not os.path.exists(versions_file):
            logger.error(f"No versions file found for project {project_id}")
            return False
            
        with open(versions_file, 'r') as f:
            versions_data = json.load(f)
            
        # Find the version to publish
        version_to_publish = None
        for version in versions_data['versions']:
            # Unpublish any currently published version
            if version['isLatestPublished']:
                version['isLatestPublished'] = False
                
            # Find the version to publish
            if version['id'] == version_id:
                version_to_publish = version
                
        if not version_to_publish:
            logger.error(f"Version {version_id} not found for project {project_id}")
            return False
            
        # Mark version as published
        version_to_publish['isPublished'] = True
        version_to_publish['isLatestPublished'] = True
        version_to_publish['publishedAt'] = datetime.utcnow().isoformat() + 'Z'
        
        # Update latest published ID
        versions_data['latestPublishedId'] = version_id
        
        # Save updated versions
        with open(versions_file, 'w') as f:
            json.dump(versions_data, f, indent=2)
            
        logger.info(f"Published version {version_id} for project {project_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error publishing version for project {project_id}: {str(e)}")
        return False

# Add these functions to your helpers.py file

def check_workspace_changes(project_id):
    """
    Check if workspace has unsaved changes compared to latest version
    """
    try:
        workspace = get_project_workspace(project_id)
        if not workspace:
            return False
            
        versions = get_project_versions(project_id)
        if not versions:
            return True  # No versions means workspace has changes
            
        # Get latest version
        latest_version = sorted(versions, key=lambda x: x.get('createdAt', ''), reverse=True)[0]
        
        # Compare calendar data
        workspace_calendar = workspace.get('calendarData', {})
        version_calendar = latest_version.get('calendarData', {})
        
        # Simple comparison - could be made more sophisticated
        return json.dumps(workspace_calendar, sort_keys=True) != json.dumps(version_calendar, sort_keys=True)
        
    except Exception as e:
        logger.error(f"Error checking workspace changes: {str(e)}")
        return False


def get_published_versions(project_id):
    """
    Get only published versions for a project (for viewer)
    """
    try:
        all_versions = get_project_versions(project_id)
        published_versions = [v for v in all_versions if v.get('isPublished', False)]
        
        # Sort by publish date, most recent first
        published_versions.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
        
        return published_versions
        
    except Exception as e:
        logger.error(f"Error getting published versions for project {project_id}: {str(e)}")
        return []


def get_latest_published_version(project_id):
    """
    Get the latest published version for a project
    """
    try:
        project_dir = os.path.join(PROJECTS_DIR, project_id)
        versions_file = os.path.join(project_dir, 'versions.json')
        
        if not os.path.exists(versions_file):
            return None
            
        with open(versions_file, 'r') as f:
            versions_data = json.load(f)
            
        latest_published_id = versions_data.get('latestPublishedId')
        if not latest_published_id:
            return None
            
        # Find the version
        for version in versions_data.get('versions', []):
            if version['id'] == latest_published_id:
                return version
                
        return None
        
    except Exception as e:
        logger.error(f"Error getting latest published version for project {project_id}: {str(e)}")
        return None

