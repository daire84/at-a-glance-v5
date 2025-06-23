# Migration Guide: Legacy to User-Based System

This guide helps you migrate from the legacy project system to the new user-based authentication system.

## Overview

The new system introduces:
- **User Authentication**: Individual user accounts with roles
- **User-Scoped Projects**: Each user has their own project workspace
- **Public Sharing**: Generate access codes for crew members
- **Enhanced Security**: Project isolation and access control

## Migration Steps

### 1. Backup Your Data
```bash
cp -r data/ data_backup/
```

### 2. Create User Accounts

Update `data/users.json` with your user accounts:
```json
[
    {
        "id": "your-admin-user-id",
        "username": "admin",
        "email": "admin@yourproduction.com",
        "password_hash": "$2b$12$[generated_hash]",
        "role": "admin",
        "created_at": "2025-01-01T00:00:00Z",
        "last_login": null,
        "is_active": true
    }
]
```

### 3. Migrate Projects

**Option A: Automatic Migration**
Use the provided migration script:
```bash
python migrate_to_users.py
```

**Option B: Manual Migration**
1. Create user directory: `data/users/[user-id]/`
2. Create user profile: `data/users/[user-id]/profile.json`
3. Move projects: `data/projects/[project-id]/` → `data/users/[user-id]/projects/[project-id]/`
4. Add `user_id` field to project `main.json` files

### 4. Directory Structure Changes

**Old Structure:**
```
data/
├── departments.json
├── locations.json
├── areas.json
└── projects/
    └── [project-id]/
        ├── main.json
        ├── holidays.json
        └── ...
```

**New Structure:**
```
data/
├── departments.json
├── locations.json
├── areas.json
├── users.json
├── users/
│   └── [user-id]/
│       ├── profile.json
│       └── projects/
│           └── [project-id]/
│               ├── main.json
│               ├── special_dates.json
│               └── ...
└── public/
    ├── access_registry.json
    └── [access-code]/
        └── calendar.json
```

### 5. Update Custom Code

If you have custom code that directly accesses project files:

**Old:**
```python
with open(f'data/projects/{project_id}/main.json') as f:
    project = json.load(f)
```

**New:**
```python
with open(f'data/users/{user_id}/projects/{project_id}/main.json') as f:
    project = json.load(f)
```

### 6. New Features Setup

#### Public Sharing
- Access codes are automatically generated when publishing calendars
- No additional setup required

#### Version Management
- Versions are now stored per project in `versions.json`
- Publishing creates snapshots in the public directory

## Breaking Changes

1. **File Paths**: All project files now include user ID in path
2. **Authentication Required**: All routes now require user authentication
3. **Project Isolation**: Users can only access their own projects (unless admin)
4. **New File Structure**: Some files have been reorganized (e.g., `special_dates.json`)

## New Features

### User Authentication
- Login/logout functionality
- Role-based access control
- User profiles and preferences

### Public Sharing
- Generate 8-character access codes (e.g., "HAMLET24")
- Shareable links for direct calendar access
- Usage statistics and access control
- No account required for viewers

### Enhanced Version Management
- Named versions with notes
- Published vs working versions
- Snapshot-based public sharing

## Troubleshooting

### Common Issues

1. **Projects Not Showing**: Ensure projects are in user-specific directories
2. **Authentication Errors**: Check users.json format and password hashes
3. **File Not Found**: Update file paths to include user ID
4. **Permission Issues**: Verify user roles and project ownership

### Getting Help

1. Check the main README.md for updated documentation
2. Review the data-templates for correct file structures
3. Use the migration script for automatic conversion
4. Ensure all dependencies are up to date

## Rollback Plan

If you need to revert to the old system:

1. Restore from backup: `cp -r data_backup/ data/`
2. Checkout previous Git commit before user system
3. Update dependencies if needed

## Benefits of New System

- **Security**: User isolation and access control
- **Scalability**: Support for multiple users and projects
- **Flexibility**: Public sharing without account requirements
- **Professional**: Enhanced version management and publishing
- **Modern**: Industry-standard authentication patterns