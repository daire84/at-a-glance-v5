import os
import json
import secrets
import string
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, List

class ProjectAccessManager:
    """Manages public access codes and tokens for calendar sharing"""
    
    def __init__(self, data_root="data"):
        self.data_root = data_root
        self.public_root = os.path.join(data_root, "public")
        self.access_registry = os.path.join(self.public_root, "access_registry.json")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories for public access"""
        os.makedirs(self.public_root, exist_ok=True)
    
    def _load_registry(self) -> Dict:
        """Load the access registry"""
        if os.path.exists(self.access_registry):
            try:
                with open(self.access_registry, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_registry(self, registry: Dict):
        """Save the access registry"""
        with open(self.access_registry, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def generate_access_code(self, length: int = 8) -> str:
        """Generate human-friendly access code like 'HAMLET24'
        
        Avoids confusing characters: 0, O, 1, I, L
        Uses uppercase letters and numbers
        """
        # Safe characters that are easily distinguishable
        safe_chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
        
        # Generate random code
        code = ''.join(secrets.choice(safe_chars) for _ in range(length))
        
        # Ensure code doesn't already exist
        registry = self._load_registry()
        while code in registry.get('codes', {}):
            code = ''.join(secrets.choice(safe_chars) for _ in range(length))
        
        return code
    
    def generate_access_token(self, length: int = 16) -> str:
        """Generate URL-safe token for direct links"""
        # URL-safe characters
        safe_chars = string.ascii_letters + string.digits + '-_'
        
        # Generate random token
        token = ''.join(secrets.choice(safe_chars) for _ in range(length))
        
        # Ensure token doesn't already exist
        registry = self._load_registry()
        while token in registry.get('tokens', {}):
            token = ''.join(secrets.choice(safe_chars) for _ in range(length))
        
        return token
    
    def publish_calendar_with_access(self, user_id: str, project_id: str, 
                                   calendar_data: Dict, project_data: Dict) -> Dict:
        """Publish calendar and create public access
        
        Returns access info with code and token
        """
        # Generate access identifiers
        access_code = self.generate_access_code()
        access_token = self.generate_access_token()
        
        # Create access info
        access_info = {
            "access_code": access_code,
            "access_token": access_token,
            "user_id": user_id,
            "project_id": project_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": None,  # No expiration for now
            "view_count": 0,
            "last_accessed": None
        }
        
        # Create public calendar data
        public_data = {
            "project": {
                "name": project_data.get("name", "Unknown Project"),
                "id": project_id,
                "published_at": access_info["created_at"]
            },
            "calendar": calendar_data,
            "access": access_info
        }
        
        # Save to both code and token directories
        code_dir = os.path.join(self.public_root, access_code)
        token_dir = os.path.join(self.public_root, access_token)
        
        os.makedirs(code_dir, exist_ok=True)
        os.makedirs(token_dir, exist_ok=True)
        
        # Save calendar data
        with open(os.path.join(code_dir, "calendar.json"), 'w') as f:
            json.dump(public_data, f, indent=2)
        
        with open(os.path.join(token_dir, "calendar.json"), 'w') as f:
            json.dump(public_data, f, indent=2)
        
        # Update registry
        registry = self._load_registry()
        if 'codes' not in registry:
            registry['codes'] = {}
        if 'tokens' not in registry:
            registry['tokens'] = {}
        if 'projects' not in registry:
            registry['projects'] = {}
        
        # Map access identifiers to project
        registry['codes'][access_code] = {
            "user_id": user_id,
            "project_id": project_id,
            "token": access_token,
            "created_at": access_info["created_at"]
        }
        
        registry['tokens'][access_token] = {
            "user_id": user_id,
            "project_id": project_id,
            "code": access_code,
            "created_at": access_info["created_at"]
        }
        
        # Map project to current access
        project_key = f"{user_id}:{project_id}"
        registry['projects'][project_key] = {
            "access_code": access_code,
            "access_token": access_token,
            "created_at": access_info["created_at"]
        }
        
        self._save_registry(registry)
        
        return access_info
    
    def get_calendar_by_code(self, access_code: str) -> Optional[Dict]:
        """Retrieve calendar data by access code"""
        return self._get_calendar_data(access_code)
    
    def get_calendar_by_token(self, access_token: str) -> Optional[Dict]:
        """Retrieve calendar data by access token"""
        return self._get_calendar_data(access_token)
    
    def _get_calendar_data(self, access_identifier: str) -> Optional[Dict]:
        """Internal method to get calendar data"""
        calendar_path = os.path.join(self.public_root, access_identifier, "calendar.json")
        
        if not os.path.exists(calendar_path):
            return None
        
        try:
            with open(calendar_path, 'r') as f:
                data = json.load(f)
            
            # Update access stats
            self.update_access_stats(access_identifier)
            
            return data
        except (json.JSONDecodeError, IOError):
            return None
    
    def update_access_stats(self, access_identifier: str):
        """Track view counts and last access"""
        calendar_path = os.path.join(self.public_root, access_identifier, "calendar.json")
        
        if not os.path.exists(calendar_path):
            return
        
        try:
            with open(calendar_path, 'r') as f:
                data = json.load(f)
            
            # Update stats
            data['access']['view_count'] = data['access'].get('view_count', 0) + 1
            data['access']['last_accessed'] = datetime.now(timezone.utc).isoformat()
            
            # Save updated data
            with open(calendar_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            # Also update the paired access method (code <-> token)
            if len(access_identifier) == 8:  # It's a code
                token = data['access']['access_token']
                token_path = os.path.join(self.public_root, token, "calendar.json")
            else:  # It's a token
                code = data['access']['access_code']
                token_path = os.path.join(self.public_root, code, "calendar.json")
            
            # Update paired access data
            if os.path.exists(token_path):
                with open(token_path, 'w') as f:
                    json.dump(data, f, indent=2)
                    
        except (json.JSONDecodeError, IOError):
            pass
    
    def get_project_access_info(self, user_id: str, project_id: str) -> Optional[Dict]:
        """Get access information for a project"""
        registry = self._load_registry()
        project_key = f"{user_id}:{project_id}"
        
        if project_key not in registry.get('projects', {}):
            return None
        
        access_data = registry['projects'][project_key]
        access_code = access_data['access_code']
        
        # Get current stats from calendar data
        calendar_data = self.get_calendar_by_code(access_code)
        if calendar_data:
            return calendar_data['access']
        
        return None
    
    def revoke_access(self, user_id: str, project_id: str) -> bool:
        """Revoke public access for a project"""
        registry = self._load_registry()
        project_key = f"{user_id}:{project_id}"
        
        if project_key not in registry.get('projects', {}):
            return False
        
        access_data = registry['projects'][project_key]
        access_code = access_data['access_code']
        access_token = access_data['access_token']
        
        # Remove from registry
        registry['codes'].pop(access_code, None)
        registry['tokens'].pop(access_token, None)
        registry['projects'].pop(project_key, None)
        
        # Remove directories
        code_dir = os.path.join(self.public_root, access_code)
        token_dir = os.path.join(self.public_root, access_token)
        
        try:
            if os.path.exists(code_dir):
                import shutil
                shutil.rmtree(code_dir)
            
            if os.path.exists(token_dir):
                import shutil
                shutil.rmtree(token_dir)
        except OSError:
            pass
        
        self._save_registry(registry)
        return True
    
    def cleanup_expired_access(self) -> int:
        """Clean up expired access codes (future feature)
        
        Returns number of cleaned up entries
        """
        # For now, no expiration logic
        # Could be implemented later with expires_at field
        return 0
    
    def get_access_statistics(self, user_id: str) -> Dict:
        """Get access statistics for a user's projects"""
        registry = self._load_registry()
        user_projects = {k: v for k, v in registry.get('projects', {}).items() 
                        if k.startswith(f"{user_id}:")}
        
        total_views = 0
        total_projects = len(user_projects)
        
        for project_key, access_data in user_projects.items():
            calendar_data = self.get_calendar_by_code(access_data['access_code'])
            if calendar_data:
                total_views += calendar_data['access'].get('view_count', 0)
        
        return {
            "total_projects_shared": total_projects,
            "total_views": total_views,
            "projects": user_projects
        }
    
    def validate_access_identifier(self, identifier: str) -> bool:
        """Validate if an access identifier exists"""
        if not identifier:
            return False
        
        registry = self._load_registry()
        return (identifier in registry.get('codes', {}) or 
                identifier in registry.get('tokens', {}))