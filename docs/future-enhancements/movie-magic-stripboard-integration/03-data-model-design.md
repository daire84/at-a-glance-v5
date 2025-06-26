# 03 - Data Model Design: Scene and Resource Management Schema

## 🗄️ Database Schema Overview

The stripboard integration requires careful data model design that extends existing STRIPS structures while maintaining backward compatibility and performance. This document defines the complete data architecture for scene management.

---

## 📊 Current Data Model Analysis

### **Existing STRIPS Data Structure**
```
data/
├── users.json                    # User accounts
├── departments.json              # Global departments  
├── locations.json               # Global locations
├── areas.json                   # Location areas
└── users/{user-id}/
    ├── profile.json             # User profile
    └── projects/{project-id}/
        ├── main.json            # Project details
        ├── special_dates.json   # Holidays, hiatus
        ├── calendar.json        # Calendar entries
        ├── versions.json        # Version history
        └── workspace.json       # View settings
```

### **Current Calendar Entry Schema**
```json
{
    "2025-01-15": {
        "date": "2025-01-15",
        "location": "smith_house",
        "area": "kitchen",
        "departments": ["camera", "sound"], 
        "time_of_day": "DAY",
        "main_unit": "Kitchen breakfast scenes",
        "notes": "Complex family interaction blocking",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }
}
```

---

## 🎬 New Scene Data Models

### **Core Scene Database**
```json
// New file: data/users/{user-id}/projects/{project-id}/scenes.json
{
    "metadata": {
        "version": "1.0",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "scene_count": 45,
        "total_pages": 120.5
    },
    
    "scenes": {
        "scene_001": {
            // Core scene identification
            "id": "scene_001",
            "scene_number": "42",
            "scene_letter": null,                    // For pickup scenes (42A, 42B)
            "description": "Kitchen breakfast - family argument",
            "synopsis": "Dad reads paper while Mom serves breakfast. Tension builds as Son refuses to eat.",
            
            // Script breakdown data
            "script_pages": 2.125,                  // Standard film pages (2 1/8)
            "estimated_minutes": 45,                // Shooting time estimate
            "story_day": "Day 1",                   // Narrative timeline
            
            // Location information
            "location": "smith_house",              // Links to locations.json
            "area": "kitchen",                      // Links to areas.json  
            "interior_exterior": "INT",             // INT/EXT
            "time_of_day": "DAY",                   // DAY/NIGHT/DAWN/DUSK
            
            // Production requirements
            "cast_required": ["dad", "mom", "son"], // References cast database
            "departments": ["camera", "sound", "art", "makeup"],
            "equipment_required": ["alexa_mini", "5k_tungsten", "boom_kit"],
            "vehicles_required": [],
            "special_requirements": [
                "breakfast_food_styling",
                "newspaper_prop",
                "practical_kitchen_lighting"
            ],
            
            // Scheduling data
            "scheduled_date": "2025-01-15",         // null if unscheduled
            "scheduled_position": 1,                // Order within day (1, 2, 3...)
            "call_time": "06:00",                   // Call time for this scene
            "estimated_wrap": "07:30",              // Estimated completion
            
            // Status tracking
            "status": "scheduled",                  // scheduled/shot/omitted/postponed
            "completion_percentage": 0,             // 0-100
            "actual_pages_shot": 0,                 // Tracking actual vs planned
            "shooting_notes": "",                   // Notes from actual shooting
            
            // Metadata
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
            "created_by": "user_001",
            "tags": ["family_drama", "breakfast_scene", "dialogue_heavy"]
        }
    },
    
    "cast_database": {
        "dad": {
            "id": "dad",
            "character_name": "Robert Thompson", 
            "actor_name": "John Smith",
            "actor_contact": {
                "email": "john@talent.com",
                "phone": "+1-555-0123",
                "agent": "Creative Artists Agency"
            },
            "availability": {
                "not_available": ["2025-01-20", "2025-01-21"],
                "half_days": ["2025-01-25"],
                "notes": "Available all days except Jan 20-21"
            },
            "requirements": {
                "makeup_time": 30,                  // Minutes
                "wardrobe_changes": 2,
                "special_skills": ["driving"],
                "restrictions": ["no_water_scenes"]
            }
        }
    },
    
    "equipment_database": {
        "alexa_mini": {
            "id": "alexa_mini",
            "name": "ARRI Alexa Mini Camera Package",
            "category": "camera",
            "subcategory": "digital_cinema_camera",
            "rental_info": {
                "vendor": "camera_rentals_inc",
                "day_rate": 500,
                "week_rate": 2000,
                "contact": "rentals@camerahouse.com"
            },
            "specifications": {
                "resolution": "4K",
                "mount": "PL",
                "includes": ["camera_body", "viewfinder", "battery_kit"]
            },
            "scheduling": {
                "requires_operator": true,
                "setup_time": 45,                   // Minutes
                "strike_time": 30
            }
        }
    },
    
    "element_tags": {
        "family_drama": {
            "name": "Family Drama",
            "description": "Scenes focusing on family relationships",
            "color": "#FF6B6B"
        },
        "breakfast_scene": {
            "name": "Breakfast Scene", 
            "description": "Scenes involving meal preparation/consumption",
            "color": "#4ECDC4"
        }
    }
}
```

### **Enhanced Calendar Schema**
```json
// Extended: data/users/{user-id}/projects/{project-id}/calendar.json
{
    "2025-01-15": {
        // === EXISTING FIELDS (PRESERVED) ===
        "date": "2025-01-15",
        "location": "smith_house",              // Primary location
        "area": "kitchen",                      // Primary area
        "departments": ["camera", "sound"],     // Active departments
        "time_of_day": "DAY",                   // Primary time
        "main_unit": "Kitchen breakfast scenes", // Summary description
        "notes": "Complex family blocking",     // Manual notes
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        
        // === NEW SCENE INTEGRATION FIELDS ===
        "scene_integration": {
            "enabled": true,                    // Can be disabled for manual calendar entries
            "auto_summary": true,               // Auto-generate summary from scenes
            
            // Scene scheduling
            "scenes_scheduled": ["scene_001", "scene_002", "scene_003"],
            "scene_order": ["scene_001", "scene_002", "scene_003"],
            
            // Auto-calculated summaries (from scene data)
            "calculated_summary": {
                "total_scenes": 3,
                "total_pages": 6.375,
                "estimated_duration_minutes": 480,  // 8 hours
                "call_time": "06:00",               // Earliest scene call
                "estimated_wrap": "18:00",          // Latest scene wrap
                
                // Aggregated from scenes
                "all_locations": ["smith_house"],
                "all_areas": ["kitchen", "dining_room"],
                "all_departments": ["camera", "sound", "art", "makeup"],
                "cast_count": 4,
                "unique_cast": ["dad", "mom", "son", "neighbor"],
                
                // Resource requirements
                "equipment_required": ["alexa_mini", "5k_tungsten", "boom_kit"],
                "vehicles_required": [],
                "special_requirements": [
                    "breakfast_food_styling", 
                    "newspaper_prop",
                    "practical_lighting"
                ]
            },
            
            // Manual overrides (preserve user customization)
            "manual_overrides": {
                "location": null,               // Override calculated primary location
                "area": null,                   // Override calculated primary area
                "main_unit": null,              // Override calculated description
                "departments": null,            // Override calculated departments
                "notes": null                   // Additional notes
            }
        }
    }
}
```

---

## 🔄 Data Relationships and Integrity

### **Scene-Calendar Relationship**
```python
# Data consistency rules:
1. Scene.scheduled_date must exist in calendar.json
2. Calendar.scenes_scheduled must reference valid scenes
3. Calendar.scene_order must include all scheduled scenes
4. Scene.scheduled_position must match order in scene_order
```

### **Resource Availability Tracking**
```json
// New file: data/users/{user-id}/projects/{project-id}/resource_schedule.json
{
    "cast_schedule": {
        "dad": {
            "2025-01-15": ["scene_001", "scene_002"],    // Scenes actor works
            "2025-01-16": ["scene_005"],
            "conflicts": [],
            "utilization_stats": {
                "total_days": 25,
                "work_days": 18,
                "utilization_percentage": 72
            }
        }
    },
    
    "equipment_schedule": {
        "alexa_mini": {
            "2025-01-15": {
                "scenes": ["scene_001", "scene_002"],
                "rental_period": {
                    "start": "2025-01-15T05:00:00Z",
                    "end": "2025-01-15T20:00:00Z"
                },
                "vendor": "camera_rentals_inc"
            }
        }
    },
    
    "location_schedule": {
        "smith_house": {
            "2025-01-15": {
                "areas_used": ["kitchen", "dining_room"],
                "scenes": ["scene_001", "scene_002", "scene_003"],
                "access_times": {
                    "earliest_call": "05:30",
                    "latest_wrap": "19:00"
                }
            }
        }
    }
}
```

---

## 📋 Data Migration Strategy

### **Backward Compatibility Schema**
```json
// Enhanced: data/users/{user-id}/projects/{project-id}/main.json
{
    // Existing project fields preserved
    "project_name": "The Mummy",
    "created_at": "2025-01-01T00:00:00Z",
    
    // New scene management capability flag
    "features": {
        "scene_management": {
            "enabled": false,           // Default disabled for existing projects
            "enabled_date": null,       // When user enabled scene features
            "version": "1.0"
        }
    }
}
```

### **Migration Utility Functions**
```python
# utils/data_migration.py
class SceneMigration:
    def enable_scene_management(self, project_id, user_id):
        """Enable scene features for existing project"""
        # 1. Create scenes.json with empty structure
        # 2. Add scene_integration fields to calendar entries
        # 3. Set features.scene_management.enabled = true
        # 4. Preserve all existing data
    
    def create_scenes_from_calendar(self, project_id, user_id):
        """Generate basic scenes from calendar entries"""
        # 1. Create one scene per calendar day
        # 2. Populate with calendar data
        # 3. Allow user to break down further
    
    def migrate_calendar_to_v2(self, project_id, user_id):
        """Add scene integration fields to calendar"""
        # 1. Add scene_integration structure
        # 2. Set enabled = false initially
        # 3. Preserve all existing fields
```

---

## 🚀 Performance Considerations

### **Data Loading Strategy**
```python
# Lazy loading for large projects
class SceneDataLoader:
    def load_project_summary(self, project_id):
        """Load only metadata and scene count"""
        # Fast initial page load
    
    def load_scenes_for_date_range(self, project_id, start_date, end_date):
        """Load scenes only for visible calendar range"""
        # Efficient calendar rendering
    
    def load_full_scene_data(self, scene_id):
        """Load complete scene details on demand"""
        # Expandable row population
```

### **Caching Strategy**
```python
# Cache calculated summaries
class SummaryCache:
    def calculate_day_summary(self, project_id, date):
        """Calculate and cache day summary from scenes"""
        # Cache result to avoid recalculation
    
    def invalidate_cache(self, project_id, date):
        """Clear cache when scenes change"""
        # Maintain data consistency
```

---

## 🔍 Data Validation Rules

### **Scene Data Validation**
```python
class SceneValidator:
    def validate_scene_data(self, scene_data):
        """Comprehensive scene validation"""
        # Required fields: id, scene_number, description
        # Valid values: interior_exterior, time_of_day
        # Reference integrity: location, area, cast, equipment
        
    def validate_scheduling(self, scene_id, date, position):
        """Validate scene scheduling"""
        # Date exists in calendar
        # Position is valid
        # No double-booking conflicts
        
    def validate_resource_availability(self, scene_id, date):
        """Check cast and equipment availability"""
        # Cast not double-booked
        # Equipment available
        # Location accessible
```

---

## 📊 Database Schema Summary

### **New Files Created**
- `scenes.json` - Complete scene and resource database
- `resource_schedule.json` - Resource availability tracking
- Migration utilities for existing projects

### **Enhanced Files**
- `calendar.json` - Scene integration fields added
- `main.json` - Feature flags for scene management

### **Preserved Files**
- All existing files remain unchanged
- Full backward compatibility maintained
- No breaking changes to current functionality

---

## 🚀 Next Steps

After reviewing this data model design, proceed to:

1. **[04-phase-1-foundation.md](04-phase-1-foundation.md)** - Implementation planning
2. **[07-ui-ux-specifications.md](07-ui-ux-specifications.md)** - Interface design
3. **[08-technical-challenges.md](08-technical-challenges.md)** - Review data challenges

---

**Data Model Principle**: Extend existing structures while maintaining complete backward compatibility and performance.

**Migration Strategy**: Opt-in scene features that enhance but never replace existing calendar functionality.