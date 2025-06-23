#!/usr/bin/env python3
"""
Data Migration Script: Single-Admin to Multi-User System
Run this script once to migrate existing project data to user-based structure.

CRITICAL: Backup your data directory before running this script!
"""

import os
import json
import shutil
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash

# Configuration
DATA_DIR = 'data'
BACKUP_SUFFIX = '_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_EMAIL = 'admin@scheduler.local'
DEFAULT_ADMIN_PASSWORD = 'change_me_immediately'  # MUST be changed!

class MigrationError(Exception):
    """Custom exception for migration errors"""
    pass

def verify_preconditions():
    """Verify system is ready for migration"""
    print("🔍 Verifying pre-migration conditions...")
    
    # Check if data directory exists
    if not os.path.exists(DATA_DIR):
        raise MigrationError(f"Data directory {DATA_DIR} not found")
    
    # Check if projects directory exists
    projects_dir = os.path.join(DATA_DIR, 'projects')
    if not os.path.exists(projects_dir):
        print("ℹ️  No existing projects directory found - clean installation")
        return True
    
    # Check for existing user structure (prevent double migration)
    users_dir = os.path.join(DATA_DIR, 'users')
    if os.path.exists(users_dir):
        raise MigrationError("Users directory already exists! Migration may have already been run.")
    
    # Verify projects are readable
    project_count = 0
    for item in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, item)
        if os.path.isdir(project_path):
            main_json = os.path.join(project_path, 'main.json')
            if os.path.exists(main_json):
                try:
                    with open(main_json, 'r') as f:
                        json.load(f)
                    project_count += 1
                except json.JSONDecodeError:
                    print(f"⚠️  Warning: Corrupted project file: {main_json}")
    
    print(f"✅ Found {project_count} valid projects to migrate")
    return True

def create_backup():
    """Create backup of entire data directory"""
    print("📦 Creating backup...")
    
    backup_dir = DATA_DIR + BACKUP_SUFFIX
    
    try:
        shutil.copytree(DATA_DIR, backup_dir)
        print(f"✅ Backup created: {backup_dir}")
        
        # Verify backup
        if not os.path.exists(backup_dir):
            raise MigrationError("Backup creation failed")
        
        return backup_dir
    except Exception as e:
        raise MigrationError(f"Backup failed: {str(e)}")

def create_user_structure():
    """Create user directory structure"""
    print("📁 Creating user directory structure...")
    
    users_dir = os.path.join(DATA_DIR, 'users')
    os.makedirs(users_dir, exist_ok=True)
    
    # Create users.json file
    users_file = os.path.join(DATA_DIR, 'users.json')
    if not os.path.exists(users_file):
        with open(users_file, 'w') as f:
            json.dump({}, f)
    
    print("✅ User structure created")

def create_admin_user():
    """Create default admin user account"""
    print("👤 Creating default admin user...")
    
    admin_id = str(uuid.uuid4())
    admin_data = {
        'id': admin_id,
        'username': DEFAULT_ADMIN_USERNAME,
        'email': DEFAULT_ADMIN_EMAIL,
        'password_hash': generate_password_hash(DEFAULT_ADMIN_PASSWORD),
        'role': 'admin',
        'created': datetime.utcnow().isoformat() + 'Z',
        'active': True
    }
    
    # Save to users.json
    users_file = os.path.join(DATA_DIR, 'users.json')
    with open(users_file, 'r') as f:
        users = json.load(f)
    
    users[admin_id] = admin_data
    
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    # Create user directory
    user_dir = os.path.join(DATA_DIR, 'users', admin_id)
    os.makedirs(user_dir, exist_ok=True)
    
    # Create user profile
    profile_data = {
        'user_id': admin_id,
        'username': DEFAULT_ADMIN_USERNAME,
        'email': DEFAULT_ADMIN_EMAIL,
        'preferences': {
            'theme': 'light',
            'default_view': 'calendar'
        }
    }
    
    with open(os.path.join(user_dir, 'profile.json'), 'w') as f:
        json.dump(profile_data, f, indent=2)
    
    print(f"✅ Admin user created with ID: {admin_id}")
    return admin_id

def migrate_projects(admin_id):
    """Migrate existing projects to admin user"""
    print("📦 Migrating projects to admin user...")
    
    old_projects_dir = os.path.join(DATA_DIR, 'projects')
    new_projects_dir = os.path.join(DATA_DIR, 'users', admin_id, 'projects')
    
    if not os.path.exists(old_projects_dir):
        print("ℹ️  No projects to migrate")
        return 0
    
    # Move projects directory
    try:
        shutil.move(old_projects_dir, new_projects_dir)
        
        # Count migrated projects
        project_count = len([d for d in os.listdir(new_projects_dir) 
                           if os.path.isdir(os.path.join(new_projects_dir, d))])
        
        print(f"✅ Migrated {project_count} projects")
        return project_count
        
    except Exception as e:
        raise MigrationError(f"Project migration failed: {str(e)}")

def verify_migration(admin_id):
    """Verify migration completed successfully"""
    print("🔍 Verifying migration...")
    
    # Check user exists
    users_file = os.path.join(DATA_DIR, 'users.json')
    with open(users_file, 'r') as f:
        users = json.load(f)
    
    if admin_id not in users:
        raise MigrationError("Admin user not found in users.json")
    
    # Check user directory exists
    user_dir = os.path.join(DATA_DIR, 'users', admin_id)
    if not os.path.exists(user_dir):
        raise MigrationError("Admin user directory not found")
    
    # Check projects directory
    projects_dir = os.path.join(user_dir, 'projects')
    if os.path.exists(projects_dir):
        project_count = len([d for d in os.listdir(projects_dir) 
                           if os.path.isdir(os.path.join(projects_dir, d))])
        print(f"✅ Verified {project_count} projects in user space")
    
    # Check old projects directory is gone
    old_projects_dir = os.path.join(DATA_DIR, 'projects')
    if os.path.exists(old_projects_dir):
        raise MigrationError("Old projects directory still exists")
    
    print("✅ Migration verification passed")

def create_rollback_script(backup_dir):
    """Create rollback script for emergency recovery"""
    rollback_script = f"""#!/bin/bash
# Rollback script generated on {datetime.now().isoformat()}
# Run this script to rollback the migration

echo "🚨 Rolling back migration..."

# Remove new user structure
rm -rf {DATA_DIR}/users
rm -f {DATA_DIR}/users.json

# Restore from backup
cp -r {backup_dir}/* {DATA_DIR}/

echo "✅ Rollback complete"
echo "⚠️  Remember to restart the application"
"""
    
    with open('rollback_migration.sh', 'w') as f:
        f.write(rollback_script)
    
    os.chmod('rollback_migration.sh', 0o755)
    print("✅ Rollback script created: rollback_migration.sh")

def main():
    """Main migration function"""
    print("🚀 Starting Film Scheduler Migration")
    print("=" * 50)
    
    try:
        # Step 1: Verify preconditions
        verify_preconditions()
        
        # Step 2: Create backup
        backup_dir = create_backup()
        
        # Step 3: Create user structure
        create_user_structure()
        
        # Step 4: Create admin user
        admin_id = create_admin_user()
        
        # Step 5: Migrate projects
        project_count = migrate_projects(admin_id)
        
        # Step 6: Verify migration
        verify_migration(admin_id)
        
        # Step 7: Create rollback script
        create_rollback_script(backup_dir)
        
        # Success!
        print("=" * 50)
        print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"👤 Admin User Created:")
        print(f"   Username: {DEFAULT_ADMIN_USERNAME}")
        print(f"   Password: {DEFAULT_ADMIN_PASSWORD}")
        print(f"   Email: {DEFAULT_ADMIN_EMAIL}")
        print(f"   User ID: {admin_id}")
        print(f"📦 Projects Migrated: {project_count}")
        print(f"💾 Backup Location: {backup_dir}")
        print(f"🔄 Rollback Script: rollback_migration.sh")
        print()
        print("🚨 IMPORTANT NEXT STEPS:")
        print("1. Change the admin password immediately!")
        print("2. Test the application thoroughly")
        print("3. Update any deployment scripts")
        print("4. Archive the backup safely")
        
    except MigrationError as e:
        print(f"❌ Migration failed: {e}")
        print("💡 Check the error above and run rollback if needed")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error during migration: {e}")
        print("🚨 Manual intervention may be required")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())