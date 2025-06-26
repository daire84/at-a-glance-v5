# 04 - Phase 1 Foundation: Basic Scene Integration (Weeks 1-10)

## 🎯 Phase 1 Overview

**Goal**: Establish the fundamental infrastructure for scene management while preserving all existing functionality. By the end of Phase 1, users can create scenes, schedule them on calendar days, and see basic expandable calendar rows.

**Duration**: 8-10 weeks  
**Complexity**: Medium-High (New data structures + UI patterns)  
**Risk Level**: Low (Additive features, no breaking changes)

---

## 📋 Phase 1 Deliverables

### **Core Features to Implement**
- [ ] Scene data storage and basic CRUD operations
- [ ] Enhanced calendar data model with scene integration
- [ ] Expandable calendar rows (basic version)
- [ ] Scene scheduling via drag-and-drop
- [ ] Basic scene list management interface
- [ ] Auto-generated day summaries from scene data
- [ ] Data migration utilities for existing projects

### **What's NOT in Phase 1**
- Complex resource conflict detection
- Advanced stripboard views  
- One-liner generation
- Cast/equipment databases
- Advanced scene editing
- Performance optimizations

---

## 🗓️ Week-by-Week Implementation Plan

### **Weeks 1-3: Data Foundation**

#### **Week 1: Scene Data Model Implementation**
```python
# Priority tasks:
1. Create scene data schema (scenes.json structure)
2. Implement basic SceneManager utility class
3. Add scene management routes to Flask app
4. Create scene validation functions
5. Write unit tests for scene data operations

# Key deliverables:
✅ utils/scene_helpers.py - Core scene management class
✅ routes/scenes.py - Basic API endpoints
✅ scenes.json schema documented and validated
✅ Unit tests for scene CRUD operations
```

**Detailed Implementation:**
```python
# utils/scene_helpers.py
class SceneManager:
    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id
        self.scenes_file = f"data/users/{user_id}/projects/{project_id}/scenes.json"
    
    def create_scene(self, scene_data):
        """Create new scene with validation"""
        # Validate required fields
        # Generate unique scene ID
        # Save to scenes.json
        # Return scene object
    
    def get_scenes(self, scheduled_only=False):
        """Retrieve scenes with optional filtering"""
        # Load from scenes.json
        # Apply filters
        # Return scene list
    
    def schedule_scene(self, scene_id, date, position=None):
        """Schedule scene on specific date"""
        # Update scene.scheduled_date
        # Update calendar.json with scene reference
        # Maintain scene order
        # Validate no conflicts
```

#### **Week 2: Calendar Integration**
```python
# Priority tasks:
1. Extend calendar.json schema with scene fields
2. Create calendar-scene synchronization functions
3. Implement auto-summary generation from scenes
4. Add scene references to existing calendar entries
5. Test data consistency between calendar and scenes

# Key deliverables:
✅ Enhanced calendar data model
✅ Calendar-scene synchronization functions
✅ Auto-summary generation algorithm
✅ Data consistency validation
```

**Detailed Implementation:**
```python
# utils/calendar_scene_sync.py
class CalendarSceneSync:
    def sync_calendar_with_scenes(self, project_id, user_id, date):
        """Synchronize calendar entry with scheduled scenes"""
        # Get scenes scheduled for date
        # Calculate summary data
        # Update calendar entry
        # Preserve manual overrides
    
    def generate_day_summary(self, scenes_list):
        """Generate calendar summary from scene data"""
        # Count scenes and pages
        # Aggregate locations and departments
        # Calculate estimated timing
        # Return summary object
```

#### **Week 3: Data Migration & Compatibility**
```python
# Priority tasks:
1. Create migration utilities for existing projects
2. Implement backward compatibility layer
3. Add feature flags for scene management
4. Test migration with existing project data
5. Create rollback procedures

# Key deliverables:
✅ Migration utility functions
✅ Feature flag system
✅ Backward compatibility tested
✅ Rollback procedures documented
```

### **Weeks 4-6: Backend API Development**

#### **Week 4: Scene Management API**
```python
# Priority tasks:
1. Implement complete scene CRUD API endpoints
2. Add authentication and authorization
3. Create scene scheduling endpoints
4. Implement basic error handling
5. Write API documentation

# routes/scenes.py
@scenes_bp.route('/api/scenes/<project_id>', methods=['GET'])
@login_required
def get_project_scenes(project_id):
    """Get all scenes for project"""
    # Verify user access to project
    # Load scenes from SceneManager
    # Return JSON response

@scenes_bp.route('/api/scenes/<project_id>/create', methods=['POST'])
@login_required  
def create_scene(project_id):
    """Create new scene"""
    # Validate input data
    # Create scene via SceneManager
    # Update calendar if scheduled
    # Return created scene

@scenes_bp.route('/api/scenes/<project_id>/schedule', methods=['POST'])
@login_required
def schedule_scene(project_id):
    """Schedule scene on date"""
    # Validate scene and date
    # Update scene scheduling
    # Sync with calendar
    # Return updated data
```

#### **Week 5: Calendar API Enhancement**
```python
# Priority tasks:
1. Enhance existing calendar API with scene support
2. Add endpoints for calendar-scene operations
3. Implement summary auto-generation endpoints
4. Add scene ordering within days
5. Test integration with existing calendar features

# Enhanced routes/admin.py
@app.route('/api/calendar/<project_id>/day/<date>/scenes', methods=['GET'])
@login_required
def get_day_scenes(project_id, date):
    """Get scenes scheduled for specific day"""
    # Load day's scenes in order
    # Return scene details
    
@app.route('/api/calendar/<project_id>/day/<date>/reorder', methods=['POST']) 
@login_required
def reorder_day_scenes(project_id, date):
    """Reorder scenes within a day"""
    # Update scene_order in calendar
    # Update scheduled_position in scenes
    # Maintain data consistency
```

#### **Week 6: Integration Testing & Error Handling**
```python
# Priority tasks:
1. Comprehensive API testing
2. Error handling and validation
3. Performance testing with sample data
4. Security testing and authorization
5. API documentation completion

# Testing priorities:
✅ Scene CRUD operations
✅ Calendar-scene synchronization
✅ Data consistency validation
✅ User authentication/authorization
✅ Error conditions and edge cases
```

### **Weeks 7-10: Frontend Implementation**

#### **Week 7: Expandable Calendar Rows (Basic)**
```javascript
// Priority tasks:
1. Create ExpandableCalendarRow component
2. Add expand/collapse functionality to calendar
3. Implement basic scene display in expanded rows
4. Add smooth animations for expansion
5. Test on mobile devices

// static/js/components/expandable-calendar-row.js
class ExpandableCalendarRow {
    constructor(dateElement, projectId) {
        this.dateElement = dateElement;
        this.projectId = projectId;
        this.date = dateElement.dataset.date;
        this.isExpanded = false;
        this.sceneData = null;
        
        this.setupExpandButton();
        this.loadSceneData();
    }
    
    setupExpandButton() {
        // Add expand button to existing calendar row
        // Preserve all existing functionality
        // Add click handler for expansion
    }
    
    async loadSceneData() {
        // Fetch scenes for this date
        // Cache data for performance
        // Update expand button state
    }
    
    toggleExpansion() {
        // Smooth animation
        // Load scene details on first expansion
        // Update button state and icon
    }
    
    renderSceneList() {
        // Display scenes in expanded area
        // Basic scene information only
        // Prepare for drag-and-drop
    }
}
```

#### **Week 8: Scene Management Interface**
```javascript
// Priority tasks:
1. Create basic scene creation/editing modals
2. Implement scene list display
3. Add basic scene information forms
4. Connect to backend API
5. Test scene CRUD operations

// static/js/components/scene-manager.js
class SceneManager {
    constructor(projectId) {
        this.projectId = projectId;
        this.scenes = {};
        this.setupEventHandlers();
    }
    
    showCreateSceneModal() {
        // Display scene creation form
        // Basic fields only (number, description, location)
        // Connect to API for creation
    }
    
    createScene(sceneData) {
        // Validate form data
        // Call API to create scene
        // Update local scene cache
        // Refresh UI as needed
    }
    
    editScene(sceneId) {
        // Load scene data into edit form
        // Allow basic field editing
        // Save changes via API
    }
}
```

#### **Week 9: Drag-and-Drop Integration**
```javascript
// Priority tasks:
1. Extend existing drag-and-drop for scenes
2. Allow scene scheduling via drag-and-drop
3. Implement scene reordering within days
4. Add visual feedback for drag operations
5. Test interaction with existing calendar drag-drop

// Enhanced static/js/calendar-drag-drop.js
class SceneDragDrop extends CalendarDragDrop {
    setupSceneDragging() {
        // Make scene items draggable
        // Allow dropping on calendar days
        // Support reordering within days
    }
    
    handleSceneDrop(sceneElement, targetDate, position) {
        // Schedule scene on target date
        // Update scene position
        // Sync with calendar
        // Refresh day summary
    }
    
    updateDayAfterSceneChange(date) {
        // Recalculate day summary
        // Update calendar row display
        // Refresh expanded view if open
    }
}
```

#### **Week 10: Testing & Polish**
```javascript
// Priority tasks:
1. Comprehensive UI testing
2. Mobile responsiveness testing
3. Integration testing with existing features
4. Performance optimization
5. User experience polish

// Testing checklist:
✅ Expandable rows work on all devices
✅ Scene drag-and-drop integrates smoothly
✅ No conflicts with existing calendar features
✅ Performance acceptable with 50+ scenes
✅ User interactions feel natural and responsive
```

---

## 🎨 User Interface Specifications

### **Enhanced Calendar Row Design**
```html
<!-- Week 7 deliverable: Enhanced calendar row template -->
<tr class="calendar-row" data-date="2025-01-15" data-has-scenes="true">
    <!-- Existing calendar cells preserved -->
    <td class="date-cell">January 15</td>
    <td class="summary-cell">
        <!-- Existing summary content -->
        <div class="day-summary">
            <span class="location-badge">Smith House - Kitchen</span>
            <span class="department-tags">Camera, Sound</span>
            <span class="time-badge">DAY</span>
        </div>
        
        <!-- New scene summary (auto-generated) -->
        <div class="scene-summary">
            <span class="scene-count">3 scenes</span>
            <span class="page-count">6 3/8 pages</span>
            <span class="duration">~8 hours</span>
        </div>
        
        <!-- Expandable content area -->
        <div class="scene-details" style="display: none;">
            <div class="scene-list">
                <!-- Scene items populated by JavaScript -->
            </div>
        </div>
        
        <!-- Expand/collapse control -->
        <button class="expand-toggle" data-date="2025-01-15">
            <span class="expand-icon">▼</span>
            <span class="expand-text">Scene Details</span>
        </button>
    </td>
</tr>
```

### **Basic Scene Item Display**
```html
<!-- Week 8 deliverable: Scene item template -->
<div class="scene-item" data-scene-id="scene_001" draggable="true">
    <div class="scene-header">
        <span class="scene-number">42</span>
        <span class="scene-description">Kitchen breakfast - family argument</span>
    </div>
    <div class="scene-details">
        <span class="scene-location">Kitchen (Smith House)</span>
        <span class="scene-pages">2 1/8 pages</span>
        <span class="scene-time">INT/DAY</span>
    </div>
    <div class="scene-actions">
        <button class="edit-scene" data-scene-id="scene_001">Edit</button>
        <button class="drag-handle">⋮⋮</button>
    </div>
</div>
```

---

## 🧪 Testing Strategy

### **Week-by-Week Testing Approach**

#### **Weeks 1-3: Data Layer Testing**
```python
# Unit tests for data operations
def test_scene_creation():
    # Test scene creation with valid data
    # Test validation error handling
    # Test data persistence

def test_calendar_scene_sync():
    # Test synchronization logic
    # Test summary generation
    # Test data consistency

def test_migration_utilities():
    # Test project migration
    # Test backward compatibility
    # Test rollback procedures
```

#### **Weeks 4-6: API Testing**
```python
# Integration tests for API endpoints
def test_scene_api_endpoints():
    # Test CRUD operations
    # Test authentication
    # Test error handling

def test_calendar_scene_integration():
    # Test scheduling APIs
    # Test summary generation
    # Test data consistency
```

#### **Weeks 7-10: UI/UX Testing**
```javascript
// Frontend integration tests
describe('Expandable Calendar Rows', () => {
    test('expansion animation works smoothly');
    test('scene data loads correctly');
    test('mobile interface functions properly');
});

describe('Scene Management', () => {
    test('scene creation works');
    test('scene editing saves correctly');
    test('drag-and-drop scheduling functions');
});
```

---

## 🚀 Phase 1 Success Criteria

### **Technical Success Metrics**
- [ ] **Data Integrity**: 100% data consistency between scenes and calendar
- [ ] **Performance**: No degradation in calendar loading time
- [ ] **Compatibility**: All existing features work unchanged
- [ ] **Mobile**: Expandable interface works on smartphones

### **Feature Completeness**
- [ ] **Scene Creation**: Users can create and edit basic scene information
- [ ] **Scene Scheduling**: Scenes can be scheduled on calendar days
- [ ] **Calendar Integration**: Day summaries auto-generate from scene data
- [ ] **Expandable UI**: Calendar rows expand to show scene details

### **User Experience Goals**
- [ ] **Intuitive**: New features feel natural and discoverable
- [ ] **Non-Disruptive**: Existing users see no workflow changes
- [ ] **Progressive**: Scene features enhance rather than complicate
- [ ] **Responsive**: UI works well on all device sizes

---

## 🔄 Phase 1 to Phase 2 Transition

### **Handoff Requirements**
Before proceeding to Phase 2, ensure:
1. **Complete data model** for scenes and calendar integration
2. **Stable API** for scene management operations
3. **Basic UI** for scene creation and scheduling
4. **Comprehensive testing** of core functionality
5. **Performance benchmarks** established

### **Phase 2 Prerequisites**
- Scene data model proven with real user data
- Expandable UI pattern established and tested
- Backend infrastructure capable of handling advanced features
- User feedback collected on basic scene management

---

## 🚀 Next Steps

After Phase 1 completion, proceed to:

1. **[05-phase-2-core-features.md](05-phase-2-core-features.md)** - Advanced scene features
2. **[09-testing-and-validation.md](09-testing-and-validation.md)** - Comprehensive testing
3. **[11-success-metrics.md](11-success-metrics.md)** - Measure Phase 1 success

---

**Phase 1 Goal**: Establish scene management foundation while preserving all existing functionality and user workflows.

**Success Definition**: Users can create scenes, schedule them on calendar days, and see the information integrated naturally into the familiar calendar interface.