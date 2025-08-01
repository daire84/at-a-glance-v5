# Film Scheduler v6 - User ID Bug Fix Session
**Date**: August 1, 2025  
**Status**: PARTIALLY RESOLVED - Still debugging versioning migration issue

## 🐛 Original Problems Identified

### 1. Calendar Generation Failing (FIXED ✅)
- **Error**: "Failed to regenerate calendar" with 404 errors
- **Root Cause**: API endpoint `/api/projects/{id}/calendar/generate` wasn't passing `user_id` parameter
- **Impact**: Projects couldn't generate calendars after user registration system was implemented

### 2. Versioning Migration Failing (PARTIALLY FIXED ⚠️)
- **Error**: "Failed to migrate project" when clicking "Enable Versioning"
- **Root Cause**: Migration function wasn't finding projects in user-specific directories
- **Current Status**: Migration runs but loses calendar data

## 🔧 Comprehensive Fixes Applied

### API Routes Fixed (`/routes/api.py`)
- `api_generate_calendar()` - Added user_id parameter extraction and passing
- `api_project()` - Fixed GET/PUT methods to use user_id  
- `api_project_calendar()` - Fixed calendar retrieval with user_id
- `api_calendar_day()` - Fixed day editing with user_id
- `api_move_calendar_day()` - Fixed day moving with user_id
- `api_get_workspace()` / `api_update_workspace()` - Fixed workspace operations
- `api_projects()` - Fixed project listing and creation
- `api_migrate_project()` - Added user_id parameter to migration call

### Route Handlers Fixed (`/routes/main.py`, `/routes/admin.py`)
- `viewer()` function - Added user_id extraction for project viewing
- `admin_day()` function - Added user_id for project and calendar operations
- All `get_project()`, `get_project_calendar()`, `save_project_calendar()` calls updated

### Migration Function Fixed (`/utils/helpers.py`)
- `migrate_project_to_versioned_structure()` - Added user_id parameter support  
- Updated to check user-specific directories with fallback to legacy
- **LATEST FIX**: Added fallback to retrieve existing calendar data via `get_project_calendar()`

## 🎯 Root Cause Analysis

The user registration system moved projects from:
- **Legacy**: `/data/projects/{project_id}/`  
- **New**: `/data/users/{user_id}/projects/{project_id}/`

However, **15+ API functions** weren't updated to handle this new structure, causing:
- Projects not found (404 errors)
- Calendar generation failures  
- Versioning migration failures
- Potential cross-user data exposure

## 📊 Current Status

### ✅ WORKING
- Calendar generation (`/api/projects/{id}/calendar/generate`)
- Project access and editing
- Day editing and calendar updates
- Workspace operations
- API project operations

### ⚠️ PARTIALLY WORKING  
- **Versioning migration** - Migration completes but calendar data is lost

### 🔍 CURRENT ISSUE: Calendar Data Loss During Migration

**Problem**: When "Enable Versioning" is clicked:
1. Migration function runs successfully
2. Project becomes versioned (`"isVersioned": true`)
3. But `workspace.json` shows `"calendarData": {}`
4. User sees "No calendar data available for this project"

**Suspected Cause**: 
- Migration function looks for legacy `calendar.json` file that doesn't exist
- Fallback to `get_project_calendar()` may not be working properly  
- Calendar data might be stored differently than expected

**Project State**:
- Project ID: `b0316fac-1f4d-43b6-b0c8-4e5d24f2c6ba`
- User ID: `06f25d7b-1e14-454c-89e5-d742020c10a8` 
- Current workspace version: `2366155f-e9cd-4501-80b8-696ea06494d5`
- `isVersioned`: true
- Workspace calendar data: empty `{}`

## 🔧 Next Steps to Complete Fix

### Immediate Actions Needed:
1. **Debug calendar data storage** - Determine where calendar data is actually stored for this project
2. **Test calendar generation** - Try generating calendar in versioned project state
3. **Fix migration calendar retrieval** - Ensure migration captures existing calendar data properly

### Investigation Points:
1. Check if calendar data exists in database/file system before migration
2. Verify `get_project_calendar()` function works with versioned projects  
3. Test if regenerating calendar in versioned state populates workspace properly
4. Consider if migration should happen AFTER calendar generation, not before

### Files Modified During This Session:
- `/routes/api.py` - Multiple endpoint fixes for user_id
- `/routes/main.py` - Viewer route user_id fix
- `/routes/admin.py` - Admin day editor user_id fixes  
- `/utils/helpers.py` - Migration function user_id support + calendar data fallback

### Container Status:
- Last rebuild: Complete clean rebuild with no cache
- All fixes applied and active
- Ready for continued debugging

## 📝 Test Scenarios for Next Session

1. **Generate Calendar Test**: Click "Generate Calendar" on versioned project
2. **Migration Test**: Test migration on a project with existing calendar data
3. **Data Persistence Test**: Verify calendar data persists through versioning workflow

---
**Note**: This represents a major architectural fix addressing the user registration system's impact on project file structure. The core user_id issues are resolved, but the versioning migration calendar data transfer needs final debugging.