# utils/decorators.py
from functools import wraps
from flask import session, flash, redirect, url_for, request

def login_required(f):
    """Decorator to require user login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in (has user_id in session)
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def viewer_required(f):
    """Decorator to require viewer or admin login (legacy support)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # For backward compatibility, allow any logged-in user
        if not session.get('user_id'):
            flash('Login required to view this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and is admin
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if session.get('user_role') != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login', next=request.url))
        
        return f(*args, **kwargs)
    return decorated_function