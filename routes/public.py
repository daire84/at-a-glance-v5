from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session
from utils.access_manager import ProjectAccessManager
import logging

# Create blueprint
public_bp = Blueprint('public', __name__)

# Initialize access manager
access_manager = ProjectAccessManager()

@public_bp.route('/calendar/<access_token>')
def view_calendar_by_token(access_token):
    """Direct calendar access via shareable link"""
    try:
        # Get calendar data to validate token and get project info
        calendar_data = access_manager.get_calendar_by_token(access_token)
        
        if not calendar_data:
            logging.warning(f"Invalid access token attempted: {access_token}")
            abort(404)
        
        # Extract project info
        access_info = calendar_data.get('access', {})
        project_id = access_info.get('project_id')
        
        if not project_id:
            logging.error(f"No project ID found for token {access_token}")
            abort(404)
        
        # Set session flag for public access
        session['public_access'] = True
        session['access_method'] = 'link'
        session['access_code'] = access_info.get('access_code', '')
        
        # Redirect to existing viewer page
        return redirect(url_for('main.viewer', project_id=project_id))
    
    except Exception as e:
        logging.error(f"Error accessing calendar by token {access_token}: {str(e)}")
        abort(500)

@public_bp.route('/access', methods=['GET', 'POST'])
def access_code_entry():
    """Access code entry page"""
    if request.method == 'GET':
        return render_template('public/access_entry.html')
    
    # Handle POST - code submission
    access_code = request.form.get('access_code', '').strip().upper()
    
    if not access_code:
        flash('Please enter an access code.', 'error')
        return render_template('public/access_entry.html')
    
    # Validate access code format (8 characters)
    if len(access_code) != 8:
        flash('Access code must be 8 characters.', 'error')
        return render_template('public/access_entry.html')
    
    try:
        # Get calendar data to validate code and get project info
        calendar_data = access_manager.get_calendar_by_code(access_code)
        
        if not calendar_data:
            flash('Invalid access code. Please check and try again.', 'error')
            return render_template('public/access_entry.html')
        
        # Extract project info
        access_info = calendar_data.get('access', {})
        project_id = access_info.get('project_id')
        
        if not project_id:
            flash('Invalid access code. Please try again.', 'error')
            return render_template('public/access_entry.html')
        
        # Set session flag for public access
        session['public_access'] = True
        session['access_method'] = 'code'
        session['access_code'] = access_code
        
        # Redirect to existing viewer page
        return redirect(url_for('main.viewer', project_id=project_id))
    
    except Exception as e:
        logging.error(f"Error accessing calendar by code {access_code}: {str(e)}")
        flash('An error occurred. Please try again.', 'error')
        return render_template('public/access_entry.html')

@public_bp.route('/production/<project_name>')
def production_landing(project_name):
    """Branded production landing pages (future feature)"""
    # This is a placeholder for future branded landing pages
    # For now, redirect to access code entry
    return redirect(url_for('public.access_code_entry'))

@public_bp.route('/help')
def help_page():
    """Help page for crew members"""
    return render_template('public/help.html')

# Error handling is now handled by the main app since we redirect to existing viewer