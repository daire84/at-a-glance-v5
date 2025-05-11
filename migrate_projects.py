#!/usr/bin/env python3
"""
Migration script to convert existing projects to versioned structure
Run this script from the project root directory
"""

import os
import sys
from utils.helpers import get_projects, migrate_project_to_versioned_structure, logger

def main():
    """Main migration function"""
    print("Film Scheduler v5 - Project Migration Tool")
    print("=========================================")
    print("\nThis script will migrate existing projects to the versioned structure.")
    print("A backup of your data is recommended before proceeding.\n")
    
    # Get all projects
    projects = get_projects()
    
    if not projects:
        print("No projects found to migrate.")
        return
    
    # Filter out already versioned projects
    projects_to_migrate = []
    for project in projects:
        if not project.get('isVersioned', False):
            projects_to_migrate.append(project)
    
    if not projects_to_migrate:
        print("All projects are already using the versioned structure.")
        return
    
    print(f"Found {len(projects_to_migrate)} projects to migrate:")
    for project in projects_to_migrate:
        print(f"  - {project.get('title', 'Untitled')} (ID: {project.get('id')})")
    
    print("\nDo you want to proceed with migration? (yes/no):")
    confirm = input().strip().lower()
    
    if confirm != 'yes':
        print("Migration cancelled.")
        return
    
    # Migrate each project
    success_count = 0
    failed_count = 0
    
    for project in projects_to_migrate:
        project_id = project.get('id')
        project_title = project.get('title', 'Untitled')
        
        print(f"\nMigrating project: {project_title}...", end="")
        
        try:
            success = migrate_project_to_versioned_structure(project_id)
            if success:
                print(" SUCCESS")
                success_count += 1
            else:
                print(" FAILED")
                failed_count += 1
        except Exception as e:
            print(f" ERROR: {str(e)}")
            failed_count += 1
    
    print("\n" + "="*50)
    print(f"Migration Complete:")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {failed_count}")
    print("="*50)
    
    if failed_count > 0:
        print("\nSome projects failed to migrate. Check the logs for details.")
    else:
        print("\nAll projects migrated successfully!")


if __name__ == "__main__":
    # Add the project root to the Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    main()
