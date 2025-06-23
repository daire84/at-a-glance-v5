# utils/user_helpers.py
import os
import json
import uuid
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Define Constants relative to this file's location
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTILS_DIR)  # Project root
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
USERS_DIR = os.path.join(DATA_DIR, 'users')

# Setup logger for user helpers
logger = logging.getLogger(__name__)

# --- User Management Functions ---

def load_users():
    """Load all users from users.json"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading users: {str(e)}")
        return {}

def save_users(users):
    """Save users to users.json"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        logger.info("Users data saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving users: {str(e)}")
        return False

def create_user(username, email, password, role='admin'):
    """Create a new user account"""
    try:
        users = load_users()
        
        # Check if username already exists
        for user_id, user_data in users.items():
            if user_data.get('username') == username:
                logger.warning(f"Username already exists: {username}")
                return None, "Username already exists"
        
        # Check if email already exists
        for user_id, user_data in users.items():
            if user_data.get('email') == email:
                logger.warning(f"Email already exists: {email}")
                return None, "Email already exists"
        
        # Generate user ID and hash password
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(password)
        
        # Create user data
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'created': datetime.utcnow().isoformat() + 'Z',
            'active': True
        }
        
        # Add user to users dict
        users[user_id] = user_data
        
        # Save users
        if not save_users(users):
            return None, "Failed to save user data"
        
        # Create user directory structure
        user_dir = os.path.join(USERS_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        # Create user projects directory
        projects_dir = os.path.join(user_dir, 'projects')
        os.makedirs(projects_dir, exist_ok=True)
        
        # Create user profile
        profile_data = {
            'user_id': user_id,
            'username': username,
            'email': email,
            'preferences': {
                'theme': 'light',
                'default_view': 'calendar'
            }
        }
        
        profile_file = os.path.join(user_dir, 'profile.json')
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"User created successfully: {username} ({user_id})")
        return user_data, None
        
    except Exception as e:
        logger.error(f"Error creating user {username}: {str(e)}")
        return None, f"Failed to create user: {str(e)}"

def authenticate_user(username_or_email, password):
    """Authenticate user by username/email and password"""
    try:
        users = load_users()
        
        # Find user by username or email
        user_data = None
        for user_id, user in users.items():
            if (user.get('username') == username_or_email or 
                user.get('email') == username_or_email):
                user_data = user
                break
        
        if not user_data:
            logger.warning(f"User not found: {username_or_email}")
            return None, "Invalid credentials"
        
        # Check if user is active
        if not user_data.get('active', True):
            logger.warning(f"Inactive user attempted login: {username_or_email}")
            return None, "Account is inactive"
        
        # Verify password
        if check_password_hash(user_data.get('password_hash', ''), password):
            logger.info(f"User authenticated successfully: {user_data.get('username')}")
            return user_data, None
        else:
            logger.warning(f"Invalid password for user: {username_or_email}")
            return None, "Invalid credentials"
            
    except Exception as e:
        logger.error(f"Error authenticating user {username_or_email}: {str(e)}")
        return None, "Authentication failed"

def get_user_by_id(user_id):
    """Get user data by ID"""
    try:
        users = load_users()
        return users.get(user_id)
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {str(e)}")
        return None

def get_user_by_username(username):
    """Get user data by username"""
    try:
        users = load_users()
        for user_id, user_data in users.items():
            if user_data.get('username') == username:
                return user_data
        return None
    except Exception as e:
        logger.error(f"Error getting user by username {username}: {str(e)}")
        return None

def update_user_password(user_id, new_password):
    """Update user password"""
    try:
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        # Hash new password
        password_hash = generate_password_hash(new_password)
        users[user_id]['password_hash'] = password_hash
        users[user_id]['updated'] = datetime.utcnow().isoformat() + 'Z'
        
        if save_users(users):
            logger.info(f"Password updated for user: {user_id}")
            return True, None
        else:
            return False, "Failed to save password"
            
    except Exception as e:
        logger.error(f"Error updating password for user {user_id}: {str(e)}")
        return False, f"Failed to update password: {str(e)}"

def update_user_profile(user_id, email=None, preferences=None):
    """Update user profile information"""
    try:
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        # Update email if provided
        if email:
            # Check if email already exists for another user
            for uid, user_data in users.items():
                if uid != user_id and user_data.get('email') == email:
                    return False, "Email already exists"
            users[user_id]['email'] = email
        
        # Update timestamp
        users[user_id]['updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Save users data
        if not save_users(users):
            return False, "Failed to save user data"
        
        # Update profile file if preferences provided
        if preferences:
            user_dir = os.path.join(USERS_DIR, user_id)
            profile_file = os.path.join(user_dir, 'profile.json')
            
            try:
                if os.path.exists(profile_file):
                    with open(profile_file, 'r', encoding='utf-8') as f:
                        profile_data = json.load(f)
                else:
                    profile_data = {
                        'user_id': user_id,
                        'username': users[user_id]['username'],
                        'email': users[user_id]['email'],
                        'preferences': {}
                    }
                
                # Update preferences
                profile_data['preferences'].update(preferences)
                if email:
                    profile_data['email'] = email
                
                with open(profile_file, 'w', encoding='utf-8') as f:
                    json.dump(profile_data, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                logger.warning(f"Failed to update profile file for user {user_id}: {str(e)}")
        
        logger.info(f"Profile updated for user: {user_id}")
        return True, None
        
    except Exception as e:
        logger.error(f"Error updating profile for user {user_id}: {str(e)}")
        return False, f"Failed to update profile: {str(e)}"

def get_user_projects_dir(user_id):
    """Get the projects directory for a user"""
    return os.path.join(USERS_DIR, user_id, 'projects')

def validate_password_strength(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Add more validation rules as needed
    return True, None

def initialize_user_system():
    """Initialize the user system (create directories, etc.)"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Create users directory if it doesn't exist
        os.makedirs(USERS_DIR, exist_ok=True)
        
        # Create users.json if it doesn't exist
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            logger.info("Created empty users.json file")
        
        return True
        
    except Exception as e:
        logger.error(f"Error initializing user system: {str(e)}")
        return False

def deactivate_user(user_id):
    """Deactivate a user account"""
    try:
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        users[user_id]['active'] = False
        users[user_id]['updated'] = datetime.utcnow().isoformat() + 'Z'
        
        if save_users(users):
            logger.info(f"User deactivated: {user_id}")
            return True, None
        else:
            return False, "Failed to save user data"
            
    except Exception as e:
        logger.error(f"Error deactivating user {user_id}: {str(e)}")
        return False, f"Failed to deactivate user: {str(e)}"

def activate_user(user_id):
    """Activate a user account"""
    try:
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        users[user_id]['active'] = True
        users[user_id]['updated'] = datetime.utcnow().isoformat() + 'Z'
        
        if save_users(users):
            logger.info(f"User activated: {user_id}")
            return True, None
        else:
            return False, "Failed to save user data"
            
    except Exception as e:
        logger.error(f"Error activating user {user_id}: {str(e)}")
        return False, f"Failed to activate user: {str(e)}"

def get_all_users():
    """Get all users (for admin purposes)"""
    try:
        users = load_users()
        # Remove password hashes for security
        safe_users = {}
        for user_id, user_data in users.items():
            safe_user = {k: v for k, v in user_data.items() if k != 'password_hash'}
            safe_users[user_id] = safe_user
        return safe_users
    except Exception as e:
        logger.error(f"Error getting all users: {str(e)}")
        return {}