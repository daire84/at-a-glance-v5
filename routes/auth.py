# routes/auth.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.user_helpers import (
    authenticate_user, create_user, validate_password_strength, 
    initialize_user_system, get_user_by_id
)

auth_bp = Blueprint('auth', __name__)

# Initialize user system on module load
initialize_user_system()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page - supports both username and email"""
    error = None
    next_page = request.args.get('next')

    # If already logged in, redirect appropriately
    if session.get('user_id'):
        user_role = session.get('user_role', 'admin')
        if user_role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username_or_email or not password:
            error = 'Please enter both username/email and password'
        else:
            # Try to authenticate user
            user_data, auth_error = authenticate_user(username_or_email, password)
            
            if user_data:
                # Set session data
                session['user_id'] = user_data['id']
                session['user_role'] = user_data.get('role', 'admin')
                session['username'] = user_data['username']
                session.permanent = True
                
                flash(f'Welcome back, {user_data["username"]}!', 'success')
                
                # Redirect based on role
                if user_data.get('role') == 'admin':
                    return redirect(next_page or url_for('admin.admin_dashboard'))
                else:
                    return redirect(next_page or url_for('main.dashboard'))
            else:
                error = auth_error or 'Invalid credentials'

    return render_template('login.html', error=error, next=next_page)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        error = None
        if not username or not email or not password:
            error = 'All fields are required'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters long'
        elif '@' not in email or '.' not in email:
            error = 'Please enter a valid email address'
        elif password != confirm_password:
            error = 'Passwords do not match'
        else:
            # Validate password strength
            is_valid, password_error = validate_password_strength(password)
            if not is_valid:
                error = password_error
        
        if not error:
            # Try to create user
            user_data, create_error = create_user(username, email, password, role='admin')
            
            if user_data:
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                error = create_error
        
        # Re-render form with error
        return render_template('admin/register.html', error=error, 
                             username=username, email=email)
    
    return render_template('admin/register.html')

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Legacy admin login - redirects to main login"""
    return redirect(url_for('auth.login', next=request.args.get('next')))

@auth_bp.route('/logout')
def logout():
    """Logout route"""
    session.clear()  # Clear all session data
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))