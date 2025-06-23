# User Authentication System Implementation Guide

## 🎯 OBJECTIVE
Transform the current single-admin system into a multi-user authentication system where production professionals (1st ADs, Producers, Coordinators) can create accounts and manage their own projects.

## 📋 PRE-IMPLEMENTATION CHECKLIST

- [ ] Current system is backed up
- [ ] All tests pass with existing functionality
- [ ] Understanding of current `routes/auth.py` implementation
- [ ] Understanding of current `utils/helpers.py` patterns
- [ ] Understanding of current data structure in `data/projects/`

## 🏗️ IMPLEMENTATION STEPS

### Step 1: Create User Management Utilities

**File to Create: `utils/user_helpers.py`**

```python
# This module handles all user-related operations
# Following the same patterns as utils/helpers.py
```

**Required Functions:**
- `ensure_user_structure()` - Create directory structure
- `get_users()` - Load all users (following get_projects pattern)
- `save_user(user_data)` - Save user data
- `create_user(username, email, password, role='user')` - User registration
- `authenticate_user(username, password)` - User login
- `get_user_projects_dir(user_id)` - Get user's project directory

**Critical Requirements:**
- Use werkzeug.security for password hashing
- Follow existing logging patterns from helpers.py
- Use same directory creation patterns as existing code
- Generate UUID for user IDs (consistent with project IDs)

### Step 2: Extend Existing Helper Functions

**File to Modify: `utils/helpers.py`**

**Add these imports:**
```python
from flask import session
from .user_helpers import get_user_projects_dir
```

**Add these new functions:**
```python
def get_current_user_id():
    """Get current user ID from session"""
    
def get_user_projects(user_id=None):
    """Get projects for specific user (modified from get_projects)"""
    
def get_user_project_dir(project_id, user_id=None):
    """Get project directory for specific user"""
    
def save_user_project(project, user_id=None):
    """Save project for specific user (modified from save_project)"""
```

**Modify existing functions to be user-aware:**
- `get_project(project_id, user_id=None)` - Add user parameter
- `get_project_calendar(project_id, user_id=None)` - Add user scoping
- `save_project_calendar(project_id, calendar_data, user_id=None)` - Add user scoping

**CRITICAL**: Maintain backward compatibility. Existing routes should continue working.

### Step 3: Update Authentication Decorators

**File to Modify: `utils/decorators.py`**

**Replace existing content with:**
```python
from functools import wraps
from flask import session, flash, redirect, url_for, request

def login_required(f):
    """Decorator to require user login"""
    
def admin_required(f):
    """Decorator to require admin role"""
    
# Keep existing decorators for backward compatibility
def viewer_required(f):
    """Maps to login_required for compatibility"""
    
def get_current_user_id():
    """Helper to get current user ID"""
    
def get_current_username():
    """Helper to get current username"""
```

### Step 4: Enhanced Authentication Routes

**File to Modify: `routes/auth.py`**

**Add these new routes:**
```python
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""

@auth_bp.route('/login', methods=['GET', 'POST'])  
def login():
    """Enhanced user login (replace existing)"""

@auth_bp.route('/logout')
def logout():
    """Enhanced logout (replace existing)"""

@auth_bp.route('/admin/users')
@admin_required
def admin_users():
    """User management for system admins"""
```

**Requirements:**
- Replace password-only auth with username/password
- Add proper password validation (minimum 6 characters)
- Maintain session structure for compatibility
- Add user registration with email validation
- Keep admin user management capabilities

### Step 5: Update Admin Routes for User Context

**File to Modify: `routes/admin.py`**

**Import changes needed:**
```python
from utils.helpers import get_user_projects, save_user_project, get_project
from utils.decorators import login_required
```

**Routes to update:**
- `admin_dashboard()` - Show current user's projects only
- `admin_project(project_id)` - Verify user owns project
- `new_project()` - Save to current user's space
- `save_project()` - Save to current user's space
- All calendar editing routes - Add user scoping

**Pattern for updates:**
```python
@admin_bp.route('/')
@login_required  # Changed from admin_required
def admin_dashboard():
    projects = get_user_projects()  # User-scoped
    # ... rest of function
```

### Step 6: Create Registration Template

**File to Create: `templates/auth/register.html`**

**Requirements:**
- Extend existing base.html
- Use existing form styling from login.html
- Include username, email, password, confirm password
- Client-side password validation
- Link to login page
- Flash message support

### Step 7: Update Login Template

**File to Modify: `templates/login.html`**

**Changes needed:**
- Update form to include username field
- Change form action to updated auth.login route
- Add "Register" link
- Update labels and placeholders
- Maintain existing styling

### Step 8: Data Migration Implementation

**File to Create: `migrate_to_users.py`**

**Purpose:** One-time script to migrate existing data to user-based structure

**Requirements:**
- Create default admin user
- Move existing projects to admin user's space
- Create backup of original data
- Verify migration success
- Provide rollback capability

**Migration Steps:**
1. Create `data/users/` directory structure
2. Create `data/users.json` file
3. Create default admin user account
4. Move `data/projects/` to `data/users/{admin_id}/projects/`
5. Update any hardcoded paths in existing data
6. Verify all projects accessible to admin user

### Step 9: Update Main Routes

**File to Modify: `routes/main.py`**

**Changes needed:**
- Update `index()` to show user's projects when logged in
- Update `viewer()` to work with user-scoped projects
- Add user context to all project lookups
- Maintain public access for viewer routes

**Key consideration:** Viewer routes must work both for logged-in admins and public access (for future crew access).

## 🧪 TESTING REQUIREMENTS

### Unit Tests
- [ ] User creation and authentication
- [ ] Password hashing and verification
- [ ] User project isolation
- [ ] Migration script functionality

### Integration Tests
- [ ] Registration flow
- [ ] Login/logout flow  
- [ ] Project creation as user
- [ ] Data isolation between users
- [ ] Admin dashboard functionality

### Manual Testing
- [ ] Create new user account
- [ ] Login with new account
- [ ] Create project as new user
- [ ] Verify old admin can't see new user's projects
- [ ] Test migration with existing data
- [ ] Verify all existing functionality works

## 🔒 SECURITY CONSIDERATIONS

### Password Security
- Use werkzeug.security for hashing
- Minimum password requirements
- No password storage in plain text
- Secure session management

### Data Isolation
- Users can only access their own projects
- Proper user ID validation on all operations
- No cross-user data leakage
- Admin role can manage users but not access their projects

### Session Management
- Secure session configuration
- Proper logout functionality
- Session timeout considerations
- CSRF protection (existing Flask patterns)

## 📁 NEW DATA STRUCTURE

### Before Migration:
```
data/
├── projects/
│   ├── project-123/
│   │   ├── main.json
│   │   └── calendar.json
│   └── project-456/
└── departments.json
```

### After Migration:
```
data/
├── users.json                 # User accounts database
├── users/                     # User-specific data
│   └── {user-id}/
│       ├── profile.json       # User profile
│       └── projects/          # User's projects
│           ├── project-123/   # Migrated project
│           └── project-456/   # User's new projects
├── projects_backup/           # Backup of original structure
└── departments.json           # Global data unchanged
```

## 🚨 CRITICAL WARNINGS

### Data Safety
- **ALWAYS backup before migration**
- Test migration script with sample data first
- Verify user access after migration
- Have rollback plan ready

### Compatibility
- Existing URLs should continue working
- Don't break any current functionality
- Maintain API compatibility
- Session structure should remain similar

### Performance
- User project lookup should be fast
- Don't add unnecessary database calls
- Maintain file-based storage benefits
- Consider caching for user sessions

## ✅ COMPLETION CHECKLIST

### Implementation Complete When:
- [ ] Users can register new accounts
- [ ] Users can login with username/password
- [ ] Users see only their own projects in dashboard
- [ ] Users can create new projects in their space
- [ ] Migration script successfully moves existing data
- [ ] All existing functionality preserved
- [ ] Security testing passes
- [ ] Manual testing complete

### Ready for Phase 2 When:
- [ ] User authentication fully functional
- [ ] All tests passing
- [ ] Data migration completed successfully
- [ ] No regressions in existing features
- [ ] Code review completed
- [ ] Documentation updated

## 🔄 ROLLBACK PLAN

If implementation fails:
1. Restore `data/projects/` from `data/projects_backup/`
2. Revert auth.py changes
3. Revert decorators.py changes
4. Remove user-related files
5. Test existing functionality
6. Analyze failure points before retry

## 💡 IMPLEMENTATION TIPS

1. **Start Small**: Implement user registration first, test thoroughly
2. **Incremental**: Don't change everything at once
3. **Test Often**: Run tests after each major change
4. **Backup**: Keep multiple backup points during development
5. **Document**: Note any deviations from this guide

This user authentication system provides the foundation for the public sharing system in the next phase.