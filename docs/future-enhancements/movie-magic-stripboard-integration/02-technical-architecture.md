# 02 - Technical Architecture: Integration with Existing STRIPS

## 🏗️ Current STRIPS Architecture Analysis

### **Existing System Strengths**
Based on the current codebase, STRIPS has excellent foundations for the stripboard integration:

#### **Data Architecture**
```python
# Current strong foundations:
✅ User-scoped project management (data/users/{user-id}/projects/)
✅ Location and department management (locations.json, departments.json)
✅ Version control system (versions.json)
✅ Public sharing with access codes (data/public/)
✅ Calendar data structure (calendar.json)
```

#### **Frontend Architecture**
```javascript
// Current capabilities:
✅ Drag-and-drop calendar interface
✅ Modal systems for editing and management
✅ Responsive mobile design
✅ Dynamic content loading and updates
✅ Color-coded department and location systems
```

#### **Backend Architecture**
```python
# Flask routes and utilities:
✅ Authentication and user management (routes/auth.py)
✅ Admin project management (routes/admin.py)
✅ Utility functions for data handling (utils/)
✅ Template rendering system
✅ API endpoints for AJAX operations
```

---

## 🔗 Integration Strategy

### **Additive Architecture Principle**
The stripboard integration will **extend** existing systems rather than replace them:

```
Current Calendar System + Scene Layer = Enhanced Calendar
Existing Data Models + Scene Models = Complete Production Data
Current UI + Expandable Rows = Unified Interface
```

### **Data Flow Integration**
```
Script Breakdown → Scene Database → Calendar Summaries → Public Sharing
     ↓                    ↓              ↓               ↓
New Feature         Enhanced Data    Enhanced Calendar   Same Interface
```

---

## 🗄️ Data Architecture Extension

### **New Data Models (Additive)**

#### **Scenes Database Structure**
```python
# New file: data/users/{user-id}/projects/{project-id}/scenes.json
{
    "scenes": {
        "scene_001": {
            "id": "scene_001",
            "scene_number": "42",
            "description": "Kitchen breakfast scene",
            "location": "kitchen",
            "area": "smith_house", 
            "time_of_day": "DAY",
            "interior_exterior": "INT",
            "script_pages": 2.125,
            "estimated_minutes": 45,
            "cast_required": ["dad", "mom", "son"],
            "departments": ["camera", "sound", "art"],
            "equipment_required": ["alexa_camera", "5k_tungsten"],
            "special_requirements": ["breakfast_props", "practical_lighting"],
            "notes": "Complex blocking with family interactions",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    },
    "cast_database": {
        "dad": {"name": "John Smith", "role": "Father", "contact": "..."},
        "mom": {"name": "Jane Doe", "role": "Mother", "contact": "..."}
    },
    "equipment_database": {
        "alexa_camera": {"name": "ARRI Alexa Mini", "type": "camera", "rate": "500/day"},
        "5k_tungsten": {"name": "5K Tungsten Kit", "type": "lighting", "rate": "200/day"}
    }
}
```

#### **Enhanced Calendar Structure**
```python
# Extended: data/users/{user-id}/projects/{project-id}/calendar.json
{
    "2025-01-15": {
        # Existing calendar data preserved
        "date": "2025-01-15",
        "location": "smith_house",
        "area": "kitchen", 
        "departments": ["camera", "sound"],
        "time_of_day": "DAY",
        "main_unit": "Kitchen scenes",
        
        # New scene integration
        "scenes_scheduled": ["scene_001", "scene_002", "scene_003"],
        "scene_order": ["scene_001", "scene_002", "scene_003"],
        "auto_generated_summary": {
            "total_scenes": 3,
            "total_pages": 6.375,
            "estimated_duration": "8 hours",
            "cast_count": 4,
            "locations_count": 2,
            "departments": ["camera", "sound", "art"]
        },
        
        # Existing fields remain unchanged
        "notes": "...",
        "created_at": "...",
        "updated_at": "..."
    }
}
```

### **Database Migration Strategy**
```python
# New utility: utils/scene_migration.py
def migrate_project_to_scenes(project_id):
    """Safely add scene capability to existing project"""
    # 1. Create scenes.json if it doesn't exist
    # 2. Preserve all existing calendar data
    # 3. Add scene fields to calendar entries
    # 4. Maintain backward compatibility
```

---

## 🎨 Frontend Architecture Extension

### **Enhanced Calendar Interface**

#### **Expandable Row Component**
```javascript
// New component: static/js/components/expandable-calendar-row.js
class ExpandableCalendarRow {
    constructor(dateElement, sceneData) {
        this.dateElement = dateElement;
        this.sceneData = sceneData;
        this.isExpanded = false;
        this.setupExpandToggle();
    }
    
    setupExpandToggle() {
        // Add expand/collapse button to existing calendar row
        // Preserve all existing calendar row functionality
        // Add smooth animation for expansion
    }
    
    renderSceneDetails() {
        // Show scene breakdown in expanded state
        // Drag-and-drop for scene reordering
        // Scene editing capabilities
    }
}
```

#### **Scene Management Interface**
```javascript
// New component: static/js/components/scene-manager.js
class SceneManager {
    constructor(projectId) {
        this.projectId = projectId;
        this.scenes = {};
        this.loadScenes();
    }
    
    // Scene CRUD operations
    createScene(sceneData) { /* ... */ }
    updateScene(sceneId, updates) { /* ... */ }
    deleteScene(sceneId) { /* ... */ }
    scheduleScene(sceneId, date) { /* ... */ }
    
    // Integration with existing calendar
    updateCalendarSummary(date) { /* ... */ }
    syncWithCalendarData() { /* ... */ }
}
```

### **UI Component Integration**

#### **Enhanced Calendar Table**
```html
<!-- Extended: templates/calendar_table.html -->
<tr class="calendar-row" data-date="2025-01-15">
    <!-- Existing calendar row content preserved -->
    <td class="date-cell">January 15</td>
    <td class="summary-cell">
        <div class="day-summary">
            <!-- Existing summary display -->
            <span class="location">Smith House - Kitchen</span>
            <span class="departments">Camera, Sound</span>
            
            <!-- New scene summary (auto-generated) -->
            <span class="scene-summary">4 scenes | 2 locations | 8 3/8 pages</span>
        </div>
        
        <!-- New expandable section -->
        <div class="scene-details" style="display: none;">
            <div class="scene-list">
                <!-- Scene breakdown rendered here -->
            </div>
        </div>
        
        <!-- New expand/collapse button -->
        <button class="expand-toggle" data-date="2025-01-15">
            <span class="expand-icon">▼</span> Scene Details
        </button>
    </td>
</tr>
```

---

## 🔧 Backend Architecture Extension

### **Enhanced Route Structure**

#### **New Scene Management Routes**
```python
# New file: routes/scenes.py
from flask import Blueprint, request, jsonify
from utils.scene_helpers import SceneManager

scenes_bp = Blueprint('scenes', __name__)

@scenes_bp.route('/api/scenes/<project_id>')
def get_scenes(project_id):
    """Get all scenes for a project"""
    # Integrate with existing authentication
    # Use existing project access control
    
@scenes_bp.route('/api/scenes/<project_id>/schedule', methods=['POST'])  
def schedule_scene(project_id):
    """Schedule a scene on a specific date"""
    # Update both scenes.json and calendar.json
    # Maintain data consistency
    
@scenes_bp.route('/api/scenes/<project_id>/summary/<date>')
def generate_day_summary(project_id, date):
    """Auto-generate calendar summary from scheduled scenes"""
    # Calculate summary from scene data
    # Update calendar.json automatically
```

#### **Enhanced Admin Routes**
```python
# Extended: routes/admin.py
@app.route('/admin/project/<project_id>/scenes')
@login_required
def project_scenes(project_id):
    """Scene management page"""
    # Integrate with existing project access control
    # Use existing template system
    
@app.route('/admin/project/<project_id>/stripboard')
@login_required  
def project_stripboard(project_id):
    """Full stripboard view"""
    # Alternative view of scene data
    # Maintain all existing navigation
```

### **Enhanced Utility Functions**

#### **Scene Processing Utilities**
```python
# New file: utils/scene_helpers.py
class SceneManager:
    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id
        self.project_path = f"data/users/{user_id}/projects/{project_id}"
    
    def get_scenes(self):
        """Load scenes with caching"""
        # Efficient scene data loading
        
    def schedule_scene(self, scene_id, date, position=None):
        """Schedule scene and update calendar"""
        # Update scenes.json
        # Update calendar.json 
        # Maintain data consistency
        
    def generate_day_summary(self, date):
        """Auto-generate calendar summary"""
        # Calculate from scheduled scenes
        # Preserve manual overrides
        
    def detect_conflicts(self, scene_id, date):
        """Detect cast/equipment conflicts"""
        # Cross-reference scene requirements
        # Return conflict warnings
```

---

## 📱 Mobile and Responsive Considerations

### **Expandable Interface on Mobile**
```css
/* Enhanced: static/css/components/calendar-mobile.css */
.calendar-row {
    /* Existing mobile optimizations preserved */
}

.scene-details {
    /* Mobile-specific scene display */
    max-height: 60vh;
    overflow-y: auto;
    background: var(--background-light);
}

@media (max-width: 768px) {
    .scene-list {
        /* Stack scenes vertically on mobile */
        /* Touch-friendly drag handles */
        /* Simplified scene cards */
    }
}
```

### **Progressive Enhancement**
```javascript
// Enhanced: static/js/mobile-calendar.js
class MobileCalendarEnhancer {
    enhanceWithScenes() {
        // Add scene functionality to mobile calendar
        // Maintain existing mobile optimizations
        // Touch-friendly interactions
    }
}
```

---

## 🔄 Integration Timeline

### **Phase 1: Foundation Integration (Weeks 1-10)**
1. **Data Model Extension** (Weeks 1-3)
   - Add scene data structures
   - Enhance calendar data model
   - Create migration utilities

2. **Backend API Development** (Weeks 4-6)
   - Scene management routes
   - Calendar integration endpoints
   - Summary generation logic

3. **Basic UI Integration** (Weeks 7-10)
   - Expandable calendar rows
   - Basic scene display
   - Simple drag-and-drop

### **Phase 2: Feature Integration (Weeks 11-22)**
4. **Advanced UI Components** (Weeks 11-16)
   - Scene editing interfaces
   - Resource conflict detection
   - Advanced drag-and-drop

5. **Report Generation** (Weeks 17-22)
   - One-liner schedules
   - Call sheet integration
   - Resource reports

### **Phase 3: Polish & Optimization (Weeks 23-30)**
6. **Performance Optimization** (Weeks 23-26)
   - Caching strategies
   - Mobile optimization
   - Database indexing

7. **Testing & Deployment** (Weeks 27-30)
   - Integration testing
   - User acceptance testing
   - Production deployment

---

## 🚀 Next Steps

After reviewing this technical architecture, proceed to:

1. **[03-data-model-design.md](03-data-model-design.md)** - Detailed database schema design
2. **[04-phase-1-foundation.md](04-phase-1-foundation.md)** - Begin implementation planning
3. **[08-technical-challenges.md](08-technical-challenges.md)** - Review specific challenges

---

**Architecture Principle**: Extend and enhance existing systems rather than replace them, ensuring all current functionality remains intact while adding powerful new capabilities.

**Integration Goal**: Seamless enhancement where users can't tell where old features end and new features begin.