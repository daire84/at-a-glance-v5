# 07 - UI/UX Specifications: Interface Design & User Interactions

## 🎨 Design Philosophy

### **Core Principles**
1. **Progressive Disclosure**: Complexity hidden until needed
2. **Familiar Enhancement**: Build on existing STRIPS patterns
3. **Professional Quality**: Interface suitable for industry professionals
4. **Mobile-First**: Ensure touch-friendly interactions across devices
5. **Performance-Focused**: Smooth animations and fast interactions

### **Visual Design Language**
- **Existing STRIPS Aesthetics**: Maintain current color scheme and typography
- **Professional Polish**: Enhanced visual hierarchy and spacing
- **Clear Information Architecture**: Logical grouping and intuitive navigation
- **Accessibility**: WCAG 2.1 AA compliance for professional use

---

## 📱 Enhanced Calendar Interface

### **Expandable Calendar Row Design**

#### **Collapsed State (Default)**
```html
<!-- Enhanced calendar row maintains familiar appearance -->
<tr class="calendar-row scene-enabled" data-date="2025-01-15">
    <td class="date-cell">
        <div class="date-primary">January 15</div>
        <div class="date-meta">Monday</div>
    </td>
    <td class="summary-cell">
        <!-- Existing summary content enhanced -->
        <div class="day-summary-header">
            <div class="location-area">
                <span class="location-badge primary">Smith House</span>
                <span class="area-badge">Kitchen, Dining Room</span>
            </div>
            <div class="department-tags">
                <span class="dept-tag camera">📷</span>
                <span class="dept-tag sound">🎵</span>
                <span class="dept-tag art">🎨</span>
            </div>
            <div class="time-indicators">
                <span class="time-badge day">DAY</span>
                <span class="duration-badge">8 hrs</span>
            </div>
        </div>
        
        <!-- New scene summary section -->
        <div class="scene-summary-compact">
            <div class="scene-stats">
                <span class="scene-count">
                    <span class="count-number">4</span>
                    <span class="count-label">scenes</span>
                </span>
                <span class="page-count">
                    <span class="count-number">8 3/8</span>
                    <span class="count-label">pages</span>
                </span>
                <span class="cast-count">
                    <span class="count-number">6</span>
                    <span class="count-label">cast</span>
                </span>
            </div>
            
            <!-- Conflict indicators -->
            <div class="conflict-indicators">
                <!-- Only show if conflicts exist -->
                <span class="conflict-warning" title="2 cast conflicts detected">
                    ⚠️ <span class="conflict-count">2</span>
                </span>
            </div>
        </div>
        
        <!-- Expandable control -->
        <button class="expand-toggle" 
                data-date="2025-01-15" 
                aria-expanded="false"
                aria-controls="scene-details-2025-01-15">
            <span class="expand-icon">▼</span>
            <span class="expand-text">Scene Details</span>
        </button>
    </td>
</tr>
```

#### **Expanded State**
```html
<!-- Expanded row reveals scene breakdown -->
<tr class="calendar-row scene-enabled expanded" data-date="2025-01-15">
    <!-- Date cell remains the same -->
    <td class="date-cell">
        <div class="date-primary">January 15</div>
        <div class="date-meta">Monday</div>
    </td>
    
    <td class="summary-cell expanded">
        <!-- Collapsed summary content -->
        <div class="day-summary-header collapsed">
            <!-- Same content as collapsed state, but smaller -->
        </div>
        
        <!-- Expanded scene details -->
        <div class="scene-details" id="scene-details-2025-01-15">
            <div class="scene-details-header">
                <div class="details-actions">
                    <button class="add-scene-btn">+ Add Scene</button>
                    <button class="reorder-scenes-btn">⋮⋮ Reorder</button>
                    <button class="day-settings-btn">⚙️ Settings</button>
                </div>
            </div>
            
            <!-- Scene list -->
            <div class="scene-list" data-date="2025-01-15">
                <!-- Individual scene items -->
                <div class="scene-item" data-scene-id="scene_001" draggable="true">
                    <div class="scene-drag-handle">⋮⋮</div>
                    
                    <div class="scene-content">
                        <div class="scene-header">
                            <div class="scene-number-badge">42</div>
                            <div class="scene-title">
                                <h4>Kitchen breakfast - family argument</h4>
                                <div class="scene-meta">
                                    <span class="scene-location">Kitchen (Smith House)</span>
                                    <span class="scene-time">INT/DAY</span>
                                    <span class="scene-pages">2 1/8 pages</span>
                                </div>
                            </div>
                            <div class="scene-status">
                                <span class="status-badge scheduled">Scheduled</span>
                            </div>
                        </div>
                        
                        <div class="scene-requirements">
                            <div class="cast-chips">
                                <span class="cast-chip">Dad</span>
                                <span class="cast-chip">Mom</span>
                                <span class="cast-chip conflict">Son</span>
                            </div>
                            <div class="equipment-summary">
                                <span class="equipment-item">📷 Alexa Mini</span>
                                <span class="equipment-item">💡 5K Kit</span>
                                <span class="equipment-item">🎵 Boom</span>
                            </div>
                        </div>
                        
                        <div class="scene-timing">
                            <span class="call-time">Call: 6:00 AM</span>
                            <span class="duration">Est: 2 hours</span>
                            <span class="completion">Complete by: 8:30 AM</span>
                        </div>
                    </div>
                    
                    <div class="scene-actions">
                        <button class="edit-scene-btn" title="Edit Scene">✏️</button>
                        <button class="duplicate-scene-btn" title="Duplicate">📄</button>
                        <button class="delete-scene-btn" title="Delete">🗑️</button>
                    </div>
                </div>
                
                <!-- More scene items... -->
            </div>
            
            <!-- Expanded details footer -->
            <div class="scene-details-footer">
                <div class="day-statistics">
                    <span class="total-scenes">4 scenes total</span>
                    <span class="total-pages">8 3/8 pages</span>
                    <span class="estimated-day">6:00 AM - 6:00 PM</span>
                </div>
                <div class="day-actions">
                    <button class="generate-call-sheet">📋 Generate Call Sheet</button>
                    <button class="export-day-schedule">📄 Export Schedule</button>
                </div>
            </div>
        </div>
        
        <!-- Collapse control -->
        <button class="expand-toggle expanded" 
                data-date="2025-01-15" 
                aria-expanded="true"
                aria-controls="scene-details-2025-01-15">
            <span class="expand-icon">▲</span>
            <span class="expand-text">Hide Details</span>
        </button>
    </td>
</tr>
```

### **Expansion Animation Behavior**
```css
/* Smooth expansion animation */
.scene-details {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-in-out;
}

.scene-details.expanding {
    max-height: 800px; /* Large enough for most content */
}

.scene-item {
    opacity: 0;
    transform: translateY(-10px);
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.scene-details.expanded .scene-item {
    opacity: 1;
    transform: translateY(0);
}

/* Staggered animation for multiple scenes */
.scene-item:nth-child(1) { transition-delay: 0.1s; }
.scene-item:nth-child(2) { transition-delay: 0.15s; }
.scene-item:nth-child(3) { transition-delay: 0.2s; }
```

---

## 🎬 Scene Management Interfaces

### **Advanced Scene Editor Modal**
```html
<!-- Comprehensive scene editing interface -->
<div class="scene-editor-modal" data-scene-id="scene_001">
    <div class="modal-header">
        <h2>Edit Scene 42 - Kitchen breakfast</h2>
        <div class="scene-status-controls">
            <select class="scene-status-select">
                <option value="scheduled">Scheduled</option>
                <option value="shot">Shot</option>
                <option value="omitted">Omitted</option>
                <option value="postponed">Postponed</option>
            </select>
        </div>
        <button class="close-modal">✕</button>
    </div>
    
    <!-- Tabbed interface for complex scene data -->
    <div class="scene-editor-tabs">
        <nav class="tab-navigation">
            <button class="tab-btn active" data-tab="basic">Basic Info</button>
            <button class="tab-btn" data-tab="cast">Cast & Characters</button>
            <button class="tab-btn" data-tab="equipment">Equipment & Departments</button>
            <button class="tab-btn" data-tab="scheduling">Scheduling & Notes</button>
        </nav>
        
        <!-- Tab 1: Basic Information -->
        <div class="tab-content active" data-tab="basic">
            <div class="form-grid">
                <div class="form-group">
                    <label for="scene-number">Scene Number</label>
                    <input type="text" id="scene-number" value="42" class="scene-input">
                </div>
                
                <div class="form-group">
                    <label for="scene-description">Description</label>
                    <textarea id="scene-description" class="scene-textarea" rows="3">Kitchen breakfast - family argument</textarea>
                </div>
                
                <div class="form-group">
                    <label for="script-pages">Script Pages</label>
                    <input type="text" id="script-pages" value="2 1/8" class="scene-input">
                </div>
                
                <div class="form-group">
                    <label for="scene-location">Location</label>
                    <select id="scene-location" class="scene-select">
                        <option value="smith_house">Smith House</option>
                        <option value="studio_stage_1">Studio Stage 1</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="scene-area">Area</label>
                    <select id="scene-area" class="scene-select">
                        <option value="kitchen">Kitchen</option>
                        <option value="dining_room">Dining Room</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Time of Day</label>
                    <div class="radio-group">
                        <label><input type="radio" name="time-of-day" value="DAY" checked> DAY</label>
                        <label><input type="radio" name="time-of-day" value="NIGHT"> NIGHT</label>
                        <label><input type="radio" name="time-of-day" value="DAWN"> DAWN</label>
                        <label><input type="radio" name="time-of-day" value="DUSK"> DUSK</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Interior/Exterior</label>
                    <div class="radio-group">
                        <label><input type="radio" name="int-ext" value="INT" checked> INT</label>
                        <label><input type="radio" name="int-ext" value="EXT"> EXT</label>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tab 2: Cast & Characters -->
        <div class="tab-content" data-tab="cast">
            <div class="cast-management">
                <div class="cast-search-add">
                    <input type="text" placeholder="Search or add cast member..." class="cast-search">
                    <button class="add-cast-btn">+ Add Cast</button>
                </div>
                
                <div class="cast-list">
                    <div class="cast-item" data-cast-id="dad">
                        <div class="cast-info">
                            <div class="cast-avatar">👨</div>
                            <div class="cast-details">
                                <h4>Robert Thompson (Dad)</h4>
                                <span class="actor-name">John Smith</span>
                            </div>
                        </div>
                        <div class="cast-availability">
                            <span class="availability-indicator available">✓ Available</span>
                        </div>
                        <div class="cast-actions">
                            <button class="remove-cast">Remove</button>
                        </div>
                    </div>
                    
                    <div class="cast-item" data-cast-id="son">
                        <div class="cast-info">
                            <div class="cast-avatar">👦</div>
                            <div class="cast-details">
                                <h4>Tommy Thompson (Son)</h4>
                                <span class="actor-name">Billy Johnson</span>
                            </div>
                        </div>
                        <div class="cast-availability">
                            <span class="availability-indicator conflict">⚠️ Conflict</span>
                            <span class="conflict-details">Also in Scene 45</span>
                        </div>
                        <div class="cast-actions">
                            <button class="resolve-conflict">Resolve</button>
                            <button class="remove-cast">Remove</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tab 3: Equipment & Departments -->
        <div class="tab-content" data-tab="equipment">
            <div class="equipment-management">
                <div class="department-selection">
                    <h3>Required Departments</h3>
                    <div class="department-grid">
                        <label class="department-checkbox">
                            <input type="checkbox" value="camera" checked>
                            <span class="dept-icon">📷</span>
                            <span class="dept-name">Camera</span>
                        </label>
                        <label class="department-checkbox">
                            <input type="checkbox" value="sound" checked>
                            <span class="dept-icon">🎵</span>
                            <span class="dept-name">Sound</span>
                        </label>
                        <label class="department-checkbox">
                            <input type="checkbox" value="art">
                            <span class="dept-icon">🎨</span>
                            <span class="dept-name">Art</span>
                        </label>
                    </div>
                </div>
                
                <div class="equipment-selection">
                    <h3>Equipment Requirements</h3>
                    <div class="equipment-categories">
                        <div class="equipment-category">
                            <h4>Camera Equipment</h4>
                            <div class="equipment-list">
                                <label class="equipment-checkbox">
                                    <input type="checkbox" value="alexa_mini" checked>
                                    <span class="equipment-name">ARRI Alexa Mini</span>
                                    <span class="equipment-cost">$500/day</span>
                                </label>
                                <label class="equipment-checkbox">
                                    <input type="checkbox" value="steadicam">
                                    <span class="equipment-name">Steadicam</span>
                                    <span class="equipment-cost">$300/day</span>
                                </label>
                            </div>
                        </div>
                        
                        <div class="equipment-category">
                            <h4>Lighting Equipment</h4>
                            <div class="equipment-list">
                                <label class="equipment-checkbox">
                                    <input type="checkbox" value="5k_tungsten" checked>
                                    <span class="equipment-name">5K Tungsten Kit</span>
                                    <span class="equipment-cost">$200/day</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tab 4: Scheduling & Notes -->
        <div class="tab-content" data-tab="scheduling">
            <div class="scheduling-details">
                <div class="timing-controls">
                    <div class="form-group">
                        <label for="estimated-duration">Estimated Duration</label>
                        <input type="number" id="estimated-duration" value="120" min="15" step="15">
                        <span class="input-suffix">minutes</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="setup-time">Setup Time</label>
                        <input type="number" id="setup-time" value="30" min="0" step="15">
                        <span class="input-suffix">minutes</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="strike-time">Strike Time</label>
                        <input type="number" id="strike-time" value="15" min="0" step="15">
                        <span class="input-suffix">minutes</span>
                    </div>
                </div>
                
                <div class="special-requirements">
                    <label for="special-requirements">Special Requirements</label>
                    <textarea id="special-requirements" rows="4" placeholder="Special equipment, props, effects, etc.">Breakfast food styling, newspaper prop, practical kitchen lighting</textarea>
                </div>
                
                <div class="scene-notes">
                    <label for="scene-notes">Production Notes</label>
                    <textarea id="scene-notes" rows="4" placeholder="Additional notes for this scene...">Complex blocking with family interactions around breakfast table</textarea>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal footer with actions -->
    <div class="modal-footer">
        <div class="conflict-summary">
            <!-- Show if conflicts detected -->
            <span class="conflict-indicator">⚠️ 2 conflicts detected</span>
            <button class="view-conflicts-btn">View Details</button>
        </div>
        
        <div class="modal-actions">
            <button class="cancel-btn">Cancel</button>
            <button class="save-draft-btn">Save Draft</button>
            <button class="save-schedule-btn primary">Save & Schedule</button>
        </div>
    </div>
</div>
```

---

## 📊 Multiple View Modes

### **View Switcher Interface**
```html
<div class="view-switcher">
    <nav class="view-navigation">
        <button class="view-btn active" data-view="calendar">
            <span class="view-icon">📅</span>
            <span class="view-label">Calendar</span>
        </button>
        <button class="view-btn" data-view="schedule">
            <span class="view-icon">📋</span>
            <span class="view-label">Schedule</span>
        </button>
        <button class="view-btn" data-view="stripboard">
            <span class="view-icon">🎬</span>
            <span class="view-label">Stripboard</span>
        </button>
    </nav>
    
    <div class="view-controls">
        <button class="filter-btn">🔍 Filter</button>
        <button class="settings-btn">⚙️ View Settings</button>
        <button class="export-btn">📤 Export</button>
    </div>
</div>
```

### **Schedule View (One-Liner Format)**
```html
<div class="schedule-view">
    <div class="schedule-header">
        <h1 class="production-title">THE MUMMY - SHOOTING SCHEDULE</h1>
        <div class="schedule-meta">
            <span class="date-range">January 15-19, 2025</span>
            <span class="total-pages">120 3/8 pages</span>
            <span class="total-days">25 shoot days</span>
        </div>
    </div>
    
    <div class="schedule-content">
        <div class="day-section">
            <div class="day-header">
                <h2>DAY 1 - MONDAY, JANUARY 15, 2025</h2>
                <div class="day-meta">
                    <span class="day-pages">Pages: 8 3/8</span>
                    <span class="call-time">Call: 6:00 AM</span>
                    <span class="wrap-time">Wrap: 6:00 PM</span>
                </div>
                <div class="location-info">
                    <strong>LOCATION:</strong> Smith House - Kitchen & Dining Room
                </div>
            </div>
            
            <div class="scene-entries">
                <div class="scene-entry">
                    <div class="scene-number">Sc 42</div>
                    <div class="scene-details">
                        <div class="scene-description">
                            <span class="scene-location">Kitchen INT/DAY</span>
                            <span class="scene-pages">2 1/8 pgs</span>
                            <span class="scene-cast">Dad, Mom, Son</span>
                        </div>
                        <div class="scene-synopsis">Breakfast scene - family tension</div>
                    </div>
                </div>
                
                <div class="scene-entry">
                    <div class="scene-number">Sc 43</div>
                    <div class="scene-details">
                        <div class="scene-description">
                            <span class="scene-location">Kitchen INT/DAY</span>
                            <span class="scene-pages">1 7/8 pgs</span>
                            <span class="scene-cast">Dad, Mom</span>
                        </div>
                        <div class="scene-synopsis">Private conversation continues</div>
                    </div>
                </div>
            </div>
            
            <div class="day-footer">
                <div class="special-requirements">
                    <strong>SPECIAL REQUIREMENTS:</strong> Breakfast food styling, practical lighting
                </div>
                <div class="equipment-summary">
                    <strong>EQUIPMENT:</strong> Alexa Mini, 5K tungsten kit, boom package
                </div>
            </div>
        </div>
    </div>
</div>
```

### **Stripboard View (Traditional Layout)**
```html
<div class="stripboard-view">
    <div class="stripboard-header">
        <div class="board-title">
            <h1>THE MUMMY - STRIPBOARD</h1>
            <div class="board-stats">
                <span>45 scenes</span>
                <span>25 days</span>
                <span>120 3/8 pages</span>
            </div>
        </div>
        
        <div class="board-controls">
            <button class="sort-btn">Sort Scenes</button>
            <button class="color-code-btn">Color Code</button>
            <button class="print-board-btn">Print Board</button>
        </div>
    </div>
    
    <div class="stripboard-container">
        <div class="stripboard-grid">
            <!-- Day columns -->
            <div class="day-column" data-date="2025-01-15">
                <div class="day-header">
                    <div class="day-number">Day 1</div>
                    <div class="day-date">Jan 15</div>
                    <div class="day-pages">8 3/8</div>
                </div>
                
                <div class="scene-strips">
                    <div class="scene-strip interior-day" data-scene-id="scene_001" draggable="true">
                        <div class="strip-number">42</div>
                        <div class="strip-content">
                            <div class="strip-description">Kitchen breakfast</div>
                            <div class="strip-location">Smith House</div>
                            <div class="strip-cast">Dad, Mom, Son</div>
                            <div class="strip-pages">2 1/8</div>
                        </div>
                    </div>
                    
                    <div class="scene-strip interior-day" data-scene-id="scene_002" draggable="true">
                        <div class="strip-number">43</div>
                        <div class="strip-content">
                            <div class="strip-description">Conversation cont.</div>
                            <div class="strip-location">Smith House</div>
                            <div class="strip-cast">Dad, Mom</div>
                            <div class="strip-pages">1 7/8</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

---

## 📱 Mobile Responsiveness

### **Mobile Calendar Enhancements**
```css
/* Mobile-specific expandable rows */
@media (max-width: 768px) {
    .calendar-row .summary-cell {
        padding: 12px 8px;
    }
    
    .scene-summary-compact {
        flex-direction: column;
        gap: 8px;
    }
    
    .scene-stats {
        justify-content: space-around;
        text-align: center;
    }
    
    .expand-toggle {
        width: 100%;
        padding: 12px;
        margin-top: 8px;
        font-size: 16px; /* Touch-friendly */
    }
    
    .scene-details {
        padding: 16px 8px;
    }
    
    .scene-item {
        padding: 16px 12px;
        margin-bottom: 12px;
        border-radius: 8px;
        background: var(--background-light);
    }
    
    .scene-content {
        flex-direction: column;
        gap: 12px;
    }
    
    .scene-actions {
        flex-direction: row;
        justify-content: space-around;
        padding-top: 12px;
        border-top: 1px solid var(--border-color);
    }
}

/* Mobile scene editor */
@media (max-width: 768px) {
    .scene-editor-modal {
        width: 100vw;
        height: 100vh;
        margin: 0;
        border-radius: 0;
    }
    
    .scene-editor-tabs .tab-navigation {
        flex-wrap: wrap;
        gap: 4px;
    }
    
    .tab-btn {
        flex: 1;
        min-width: 120px;
        padding: 8px 12px;
        font-size: 14px;
    }
    
    .form-grid {
        grid-template-columns: 1fr; /* Single column on mobile */
        gap: 16px;
    }
}
```

### **Touch-Friendly Interactions**
```javascript
// Enhanced touch handling for mobile
class MobileEnhancements {
    setupTouchInteractions() {
        // Larger touch targets
        // Improved drag-and-drop for touch
        // Swipe gestures for navigation
        // Touch-friendly modals
    }
    
    handleSceneDragTouch(event) {
        // Touch-specific drag handling
        // Visual feedback for touch
        // Haptic feedback where available
    }
    
    optimizeModalForMobile() {
        // Full-screen modals on small screens
        // Simplified navigation
        // Touch-friendly form controls
    }
}
```

---

## 🎯 Accessibility Considerations

### **Keyboard Navigation**
```html
<!-- All interactive elements have proper tabindex and ARIA labels -->
<button class="expand-toggle" 
        tabindex="0"
        aria-expanded="false"
        aria-controls="scene-details-2025-01-15"
        aria-label="Expand scene details for January 15">
    <span class="expand-icon" aria-hidden="true">▼</span>
    <span class="expand-text">Scene Details</span>
</button>

<!-- Keyboard shortcuts for power users -->
<div class="keyboard-shortcuts" aria-label="Keyboard shortcuts">
    <kbd>E</kbd> Expand/collapse selected day
    <kbd>N</kbd> Create new scene
    <kbd>D</kbd> Duplicate selected scene
    <kbd>Delete</kbd> Delete selected scene
</div>
```

### **Screen Reader Support**
```html
<!-- Proper heading hierarchy -->
<h1>Film Production Schedule</h1>
<h2>January 15, 2025 - Kitchen Scenes</h2>
<h3>Scene 42 - Kitchen breakfast</h3>

<!-- Descriptive alternative text -->
<span class="conflict-indicator" 
      aria-label="Warning: 2 cast conflicts detected for this scene">
    ⚠️ <span aria-hidden="true">2</span>
</span>

<!-- Status announcements -->
<div aria-live="polite" class="status-announcements">
    <!-- Dynamic status updates announced to screen readers -->
</div>
```

---

## 🚀 Next Steps

After reviewing UI/UX specifications, proceed to:

1. **[08-technical-challenges.md](08-technical-challenges.md)** - Implementation challenges
2. **[09-testing-and-validation.md](09-testing-and-validation.md)** - User testing approaches
3. **[04-phase-1-foundation.md](04-phase-1-foundation.md)** - Begin implementation

---

**UI/UX Principle**: Enhance the familiar calendar interface with professional stripboard capabilities while maintaining the simplicity and accessibility that makes STRIPS powerful.

**Design Goal**: Create an interface that feels intuitive to both traditional calendar users and professional 1st ADs transitioning from Movie Magic.