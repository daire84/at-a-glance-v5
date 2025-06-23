# Data Templates

This directory contains sample data structures for the STRIPS Film Production Scheduler.

## Usage

1. Copy these files to your actual `data/` directory
2. Modify the sample data to match your project needs
3. The application will create additional files as needed

## Structure

### Global Data
- `departments.json` - Global department definitions
- `locations.json` - Global location database  
- `areas.json` - Location area groupings
- `users.json` - User account registry

### User-Based Project System
- `users/[user-id]/` - User-specific data directory
  - `profile.json` - User profile information
  - `projects/[project-id]/` - User's project data
    - `main.json` - Project metadata
    - `holidays.json` - Bank holidays for this project
    - `weekends.json` - Working weekend definitions
    - `hiatus.json` - Production hiatus periods
    - `special_dates.json` - Combined special dates
    - `calendar.json` - Generated calendar data (created automatically)
    - `versions.json` - Version history (created automatically)
    - `workspace.json` - Current workspace (created automatically)

### Public Access System
- `public/` - Public calendar sharing data
  - `access_registry.json` - Registry of active access codes
  - `[access-code]/` - Individual access code data
    - `calendar.json` - Published calendar snapshot

## New Features (Phase 2)

### User Authentication System
- Multi-user support with individual accounts
- User-scoped project isolation
- Admin and regular user roles

### Public Sharing System
- Generate access codes for crew members
- Shareable links for calendar access
- No account required for viewing published calendars
- Usage statistics and access control

## Migration from Legacy System

If upgrading from the old system (pre-user authentication):

1. Existing projects in `data/projects/` should be migrated to `data/users/[user-id]/projects/`
2. Use the provided migration script: `migrate_to_users.py`
3. Update any direct file references in custom code

## Security Note

The actual `data/` directory should never be committed to version control as it may contain sensitive production information.

## Sample Data

The templates include realistic sample data for "Lee Cronin's 'The Mummy'" production to demonstrate the system structure and capabilities.