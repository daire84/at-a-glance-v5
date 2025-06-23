# Quick Setup Guide

Get STRIPS Film Production Scheduler running with the new user-based system.

## New Installation

### 1. Copy Template Data
```bash
cp -r data-templates/ data/
```

### 2. Create Your Admin User

Edit `data/users.json` and replace the sample data:

```json
[
    {
        "id": "your-unique-user-id",
        "username": "your-username",
        "email": "your-email@example.com",
        "password_hash": "will-be-generated-on-first-login",
        "role": "admin",
        "created_at": "2025-01-01T00:00:00Z",
        "last_login": null,
        "is_active": true
    }
]
```

### 3. Update User Profile

Edit `data/users/sample-admin-user-id/profile.json`:
- Change directory name from `sample-admin-user-id` to your user ID
- Update profile information

### 4. Customize Project Data

Edit `data/users/[your-user-id]/projects/sample-project/main.json`:
- Update project information
- Change project ID if needed
- Update all project details

### 5. Start the Application

```bash
python app.py
```

Visit `http://localhost:5000` and:
1. Click "Admin Access" → "Admin Dashboard"
2. Create your account on first visit
3. Log in and start creating projects

## Key Features

### User Authentication
- **Admin Users**: Full access to all features
- **Regular Users**: Personal project workspaces
- **Account Management**: Login, logout, user profiles

### Public Sharing
- **Access Codes**: 8-character codes for crew access (e.g., "HAMLET24")
- **Direct Links**: Shareable URLs for instant calendar access
- **No Registration**: Crew can view schedules without creating accounts
- **Usage Tracking**: Monitor who's accessing your calendars

### Version Management
- **Named Versions**: Track changes with descriptive names
- **Publishing**: Share specific versions publicly
- **Snapshots**: Published versions are preserved
- **History**: Full version history with notes

## File Structure

```
data/
├── users.json                    # User accounts
├── departments.json              # Global departments
├── locations.json               # Global locations
├── areas.json                   # Location areas
├── users/                       # User workspaces
│   └── [user-id]/
│       ├── profile.json         # User profile
│       └── projects/
│           └── [project-id]/
│               ├── main.json           # Project details
│               ├── special_dates.json  # Holidays, weekends, hiatus
│               ├── calendar.json       # Generated calendar
│               ├── versions.json       # Version history
│               └── workspace.json      # View settings
└── public/                      # Public sharing
    ├── access_registry.json     # Active access codes
    └── [access-code]/
        └── calendar.json        # Published calendar
```

## Quick Tips

1. **First Login**: The system will guide you through account creation
2. **Project Creation**: Use "Create New Project" from the admin dashboard
3. **Calendar Access**: Publish versions to generate access codes for crew
4. **Data Safety**: Never commit the `data/` directory to version control

## Demo Data

The templates include sample data for "Lee Cronin's 'The Mummy'" to demonstrate the system. Feel free to:
- Use it as reference for data structure
- Modify it for your own projects
- Delete it and start fresh

## Need Help?

- Check `MIGRATION_GUIDE.md` if upgrading from the old system
- Review `README.md` for detailed documentation
- Examine the sample data for structure examples