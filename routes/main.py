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
    user_id = session.get('user_id')  # ADD THIS LINE
    projects = get_projects(user_id)  # ADD user_id parameter
    return render_template('dashboard.html', projects=projects)

# In routes/main.py, replace the entire viewer function with this:

@main_bp.route('/viewer/<project_id>')
def viewer(project_id):
    """Calendar viewer that supports both admin (owner) and public access."""
    # --- Inputs / session ---
    user_id = session.get('user_id')
    requested_version_id = request.args.get('version')

    # --- Helpers (local to route) ---
    def _json_load(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON {path}: {e}")
            return None

    def _extract_versions(obj):
        """Accept either a raw list or a wrapper dict {'versions': [...]}."""
        if obj is None:
            return []
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            return obj.get('versions', [])
        return []

    def _find_versions_any_owner(proj_id):
        """Scan all user directories for versions.json of this project."""
        users_dir = os.path.join(DATA_DIR, 'users')
        if not os.path.exists(users_dir):
            return [], None  # no users dir -> legacy only

        try:
            for uid in os.listdir(users_dir):
                proj_vfile = os.path.join(users_dir, uid, 'projects', proj_id, 'versions.json')
                if os.path.isfile(proj_vfile):
                    data = _json_load(proj_vfile)
                    return _extract_versions(data), uid
        except Exception as e:
            logger.error(f"Error scanning users for versions: {e}")

        return [], None

    def _latest_published(versions):
        """Pick latest published by publishedAt (ISO), fallback to versionNumber."""
        pubs = [v for v in versions if v.get('isPublished')]
        if not pubs:
            return None

        def parse_vernum(s):
            parts = str(s or '0').split('.')
            try:
                return tuple(int(p) for p in parts)
            except Exception:
                return (0,)

        def sort_key(v):
            ts = v.get('publishedAt') or ''
            # ISO 8601 sorts lexicographically; if missing, use empty string
            return (ts, parse_vernum(v.get('versionNumber')))

        pubs.sort(key=sort_key)
        return pubs[-1]

    # --- Determine owner project (if logged in) ---
    project = None
    if user_id:
        project = get_project(project_id, user_id)

    # --- Load versions ---
    versions = []
    versions_owner_id = None

    # Path A: if you have a helper that returns the correct user-scoped versions (single-arg signature)
    try:
        # Your earlier code used get_project_versions(project_id) without user arg.
        versions = get_project_versions(project_id) or []
        versions_owner_id = user_id if project else None  # best-effort tagging
    except TypeError:
        # If helper signature changed or depends on session in utils, ignore and fallback
        versions = []

    # Path B: If no versions found yet (public or different owner), scan all users
    if not versions:
        versions, versions_owner_id = _find_versions_any_owner(project_id)

    # Path C: Legacy storage fallback (/app/data/projects/<proj>/versions.json)
    if not versions:
        legacy_vfile = os.path.join(DATA_DIR, 'projects', project_id, 'versions.json')
        if os.path.isfile(legacy_vfile):
            data = _json_load(legacy_vfile)
            versions = _extract_versions(data)

    # --- Public/owner branching with specific version handling ---
    calendar_data = None

    if requested_version_id:
        # Find the requested version
        version_obj = next((v for v in versions if v.get('id') == requested_version_id), None)
        if not version_obj:
            flash('Version not found', 'error')
            return redirect(url_for('main.viewer', project_id=project_id))

        # Public users can only view published versions
        if not project and not version_obj.get('isPublished'):
            flash('Version not accessible', 'error')
            return redirect(url_for('main.viewer', project_id=project_id))

        calendar_data = version_obj.get('calendarData', {"days": []})

        if not project:
            # Minimal project for template when owner metadata isn't available
            project = {
                "id": project_id,
                "title": version_obj.get("projectTitle") or "Production Calendar",
                "isVersioned": True,
            }
    else:
        # No version specified: choose latest published for public;
        # for owners on versioned projects, also prefer latest published.
        latest_pub = _latest_published(versions)
        if latest_pub:
            calendar_data = latest_pub.get('calendarData', {"days": []})
            requested_version_id = latest_pub.get('id')
            if not project:
                project = {
                    "id": project_id,
                    "title": latest_pub.get("projectTitle") or "Production Calendar",
                    "isVersioned": True,
                }
        else:
            # No published versions anywhere
            if project and not project.get('isVersioned'):
                # Legacy, non-versioned owner project
                calendar_data = get_project_calendar(project_id, user_id)
            else:
                # Nothing to show publicly
                return render_template(
                    'viewer.html',
                    project=project or {"id": project_id, "title": "Calendar Not Available"},
                    calendar=None,
                    no_published_version=True,
                    versions=[],
                    locations=[]
                )

    # --- Supporting data (unchanged) ---
    departments = []
    departments_file = os.path.join(DATA_DIR, 'departments.json')
    if os.path.exists(departments_file):
        try:
            with open(departments_file, 'r', encoding='utf-8') as f:
                departments = json.load(f)
        except Exception as e:
            logger.error(f"Error loading departments: {str(e)}")

    locations = []
    locations_file = os.path.join(DATA_DIR, 'locations.json')
    if os.path.exists(locations_file):
        try:
            with open(locations_file, 'r', encoding='utf-8') as f:
                locations = json.load(f)
        except Exception as e:
            logger.error(f"Error loading locations: {str(e)}")

    areas = []
    areas_file = os.path.join(DATA_DIR, 'areas.json')
    if os.path.exists(areas_file):
        try:
            with open(areas_file, 'r', encoding='utf-8') as f:
                areas = json.load(f)
        except Exception as e:
            logger.error(f"Error loading areas in viewer route: {str(e)}")

    # Attach supporting data & metrics
    if calendar_data is not None:
        calendar_data['departments'] = departments
        calendar_data['locationAreas'] = areas

        calendar_data = calculate_department_counts(calendar_data)
        calendar_data = calculate_location_counts(calendar_data)

        from utils.calendar_generator import calculate_sun_times_for_calendar
        calendar_data = calculate_sun_times_for_calendar(calendar_data)

    # Build versions list for selector (published only for public)
    published_versions = [v for v in versions if v.get('isPublished')]
    # Sort for UX: oldest->newest
    def _ver_sort_key(v):
        return (v.get('publishedAt') or '', v.get('versionNumber') or '0')
    published_versions.sort(key=_ver_sort_key)

    return render_template(
        'viewer.html',
        project=project,
        calendar=calendar_data,
        locations=locations,
        versions=published_versions,
        current_version_id=requested_version_id
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