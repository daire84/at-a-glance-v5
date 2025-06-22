/**
 * =============================================================================
 * Calendar Functionality (calendar.js)
 * =============================================================================
 *
 * Handles various features for the calendar view:
 * - Color coding for location areas and department tags.
 * - Admin-specific event handling (row clicks, drag-and-drop).
 * - Calendar filtering (rows and columns).
 * - Mobile menu toggle functionality.
 * - Scrollable table detection and touch interactions.
 * - Zoom controls for mobile view.
 *
 * Structure:
 * - Helper Functions (e.g., hexToRgb, ensureTextContrast)
 * - Feature Initialization Functions (e.g., initializeFilters, setupMobileMenu)
 * - Main Consolidated DOMContentLoaded Listener
 */

// =======================================
// Helper Functions
// =======================================

/**
 * Convert hex color to RGB object.
 * @param {string} hex - The hex color string (e.g., "#RRGGBB").
 * @returns {object|null} RGB object {r, g, b} or null if invalid hex.
 */
function hexToRgb(hex) {
    if (!hex) return null;
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

/**
 * Ensure text has proper contrast against its background color.
 * Sets element's color style to black or white based on brightness.
 * @param {HTMLElement} element - The element to check contrast for.
 */
function ensureTextContrast(element) {
    const bgColor = window.getComputedStyle(element).backgroundColor;
    const rgbMatch = bgColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)/);
    if (rgbMatch) {
        const r = parseInt(rgbMatch[1]);
        const g = parseInt(rgbMatch[2]);
        const b = parseInt(rgbMatch[3]);
        // Calculate brightness (YIQ formula)
        const brightness = (r * 299 + g * 587 + b * 114) / 1000;
        // Set text color based on background brightness threshold (128 is common)
        element.style.color = brightness > 128 ? '#000000' : '#ffffff';
    }
}

/**
 * Checks if calendar table wrappers are scrollable and adds/removes a class.
 * Needs to be accessible by zoom controls, hence defined globally here.
 */
function checkIfScrollable() {
    const tableWrappers = document.querySelectorAll('.calendar-table-wrapper');
    tableWrappers.forEach(wrapper => {
        const table = wrapper.querySelector('.calendar-table');
        if (!table) return;
        // Check if the table's content width exceeds the wrapper's visible width
        if (table.scrollWidth > wrapper.clientWidth + 1) { // Add 1px tolerance
            wrapper.classList.add('scrollable');
        } else {
            wrapper.classList.remove('scrollable');
        }
    });
}

/**
 * Enhance location counters with proper color coding from location data
 */
function enhanceLocationCounters() {
    console.log("Enhancing location counters with proper colors");
    
    // Get all counter items in the location counter section
    const locationCounters = document.querySelectorAll('.location-counters .counter-item');
    const areaCounters = document.querySelectorAll('.location-areas .area-tag');
    
    // Update location counter colors
    locationCounters.forEach(counter => {
      const locationName = counter.querySelector('.counter-label').textContent.trim();
      
      // Check if counter already has a background color set
      const currentColor = counter.style.backgroundColor;
      if (!currentColor || currentColor === 'transparent' || currentColor === '') {
        // Try to find the color from data attributes
        const areaColor = counter.getAttribute('data-area-color');
        if (areaColor) {
          counter.style.backgroundColor = areaColor;
          
          // Ensure text contrast is appropriate for the background color
          ensureTextContrast(counter);
        }
      }
    });
    
    // Update area counter colors
    areaCounters.forEach(counter => {
      // Ensure text contrast is appropriate for the background color
      ensureTextContrast(counter);
    });
}

/**
 * Enhanced Go to Today functionality - scrolls calendar to today's date and shows current shoot day
 */
function goToToday() {
    const today = new Date();
    const todayString = today.toISOString().split('T')[0]; // Format: YYYY-MM-DD
    
    // Find the day element for today - try different possible selectors
    let todayElement = document.querySelector(`[data-date="${todayString}"]`);
    
    // If not found, try looking in calendar rows
    if (!todayElement) {
        todayElement = document.querySelector(`.calendar-row[data-date="${todayString}"]`);
    }
    
    if (todayElement) {
        // Smooth scroll to today's date
        todayElement.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        
        // Optional: Add a temporary highlight effect
        todayElement.classList.add('today-highlight');
        setTimeout(() => {
            todayElement.classList.remove('today-highlight');
        }, 2000);
        
        // Get shoot day info
        const shootDayCell = todayElement.querySelector('.day-cell');
        const shootDay = shootDayCell ? shootDayCell.textContent.trim() : '';
        
        console.log(`Scrolled to today's date: ${todayString}${shootDay ? ` (Shoot Day ${shootDay})` : ''}`);
    } else {
        // If today's date isn't in the current calendar view
        console.log(`Today's date (${todayString}) not found in calendar`);
        
        // Show a more helpful message
        const button = document.getElementById('go-to-today-btn');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-exclamation-circle"></i> Not in Schedule';
        button.classList.add('not-found');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('not-found');
        }, 3000);
    }
}

/**
 * Update the Go to Today button with current information
 */
function updateGoToTodayButton() {
    const button = document.getElementById('go-to-today-btn');
    if (!button) return;
    
    const today = new Date();
    const todayString = today.toISOString().split('T')[0];
    
    // Find today's row
    const todayRow = document.querySelector(`.calendar-row[data-date="${todayString}"]`);
    
    if (todayRow) {
        const shootDayCell = todayRow.querySelector('.day-cell');
        const shootDay = shootDayCell ? shootDayCell.textContent.trim() : '';
        
        if (shootDay) {
            button.innerHTML = `
                <div class="today-btn-content">
                    <i class="fas fa-calendar-day"></i>
                    <span class="today-btn-main">Go to Today</span>
                    <span class="today-btn-sub">Shoot Day ${shootDay}</span>
                </div>
            `;
        } else {
            // Check if it's a weekend, holiday, or other day type
            const dayType = todayRow.classList.contains('weekend') ? 'Weekend' :
                           todayRow.classList.contains('holiday') ? 'Holiday' :
                           todayRow.classList.contains('hiatus') ? 'Hiatus' :
                           todayRow.classList.contains('prep') ? 'Prep Day' : 'Non-Shoot';
            
            button.innerHTML = `
                <div class="today-btn-content">
                    <i class="fas fa-calendar-day"></i>
                    <span class="today-btn-main">Go to Today</span>
                    <span class="today-btn-sub">${dayType}</span>
                </div>
            `;
        }
        button.classList.add('enhanced-today-btn');
    } else {
        button.innerHTML = `
            <div class="today-btn-content">
                <i class="fas fa-calendar-day"></i>
                <span class="today-btn-main">Go to Today</span>
                <span class="today-btn-sub">Not in Schedule</span>
            </div>
        `;
        button.classList.add('enhanced-today-btn', 'not-in-schedule');
    }
}

class LocationFilter {
    constructor() {
        this.activeFilters = {
            locations: new Set(),
            areas: new Set()
        };
        this.init();
    }

    init() {
        this.setupLocationClickHandlers();
        this.setupAreaClickHandlers();
        this.setupClearFilters();
    }

    setupLocationClickHandlers() {
        document.querySelectorAll('.location-counters .counter-item').forEach(counter => {
            const label = counter.querySelector('.counter-label');
            if (label) {
                counter.style.cursor = 'pointer';
                counter.title = 'Click to filter by this location';
                counter.classList.add('clickable-filter');
                
                counter.addEventListener('click', (e) => {
                    e.preventDefault();
                    const locationName = label.textContent.trim();
                    this.toggleLocationFilter(locationName, counter);
                });
            }
        });
    }

    setupAreaClickHandlers() {
        document.querySelectorAll('.location-areas .area-tag').forEach(counter => {
            counter.style.cursor = 'pointer';
            counter.title = 'Click to filter by this area';
            counter.classList.add('clickable-filter');
            
            counter.addEventListener('click', (e) => {
                e.preventDefault();
                const nameElement = counter.cloneNode(true);
                const countElement = nameElement.querySelector('.area-count');
                if (countElement) {
                    nameElement.removeChild(countElement);
                }
                const areaName = nameElement.textContent.trim();
                this.toggleAreaFilter(areaName, counter);
            });
        });
    }

    toggleLocationFilter(locationName, element) {
        if (this.activeFilters.locations.has(locationName)) {
            this.activeFilters.locations.delete(locationName);
            element.classList.remove('filter-active');
        } else {
            this.activeFilters.locations.add(locationName);
            element.classList.add('filter-active');
        }
        this.applyFilters();
    }

    toggleAreaFilter(areaName, element) {
        if (this.activeFilters.areas.has(areaName)) {
            this.activeFilters.areas.delete(areaName);
            element.classList.remove('filter-active');
        } else {
            this.activeFilters.areas.add(areaName);
            element.classList.add('filter-active');
        }
        this.applyFilters();
    }

    applyFilters() {
        const hasLocationFilters = this.activeFilters.locations.size > 0;
        const hasAreaFilters = this.activeFilters.areas.size > 0;
        
        if (!hasLocationFilters && !hasAreaFilters) {
            this.showAllDays();
            return;
        }

        // Apply filters to table view (calendar rows)
        document.querySelectorAll('.calendar-row').forEach(row => {
            let showRow = false;

            if (hasLocationFilters) {
                const locationCell = row.querySelector('.location-cell');
                if (locationCell) {
                    const locationText = locationCell.textContent.trim();
                    showRow = Array.from(this.activeFilters.locations).some(loc => 
                        locationText.includes(loc)
                    );
                }
            }

            if (hasAreaFilters && !showRow) {
                const areaAttribute = row.getAttribute('data-area');
                if (areaAttribute) {
                    showRow = this.activeFilters.areas.has(areaAttribute);
                } else {
                    const locationCell = row.querySelector('.location-cell');
                    if (locationCell) {
                        const locationText = locationCell.textContent.trim();
                        showRow = Array.from(this.activeFilters.areas).some(area => 
                            locationText.includes(area)
                        );
                    }
                }
            }

            row.classList.toggle('location-filtered-hidden', !showRow);
        });

        // Apply to calendar view if it exists and is active
        this.applyToCalendarView();

        this.updateFilterIndicator();
        this.updateFilterStats();
    }

    applyToCalendarView() {
        // Only apply if calendar view exists and is currently active
        if (window.calendarView && window.calendarView.getCurrentView() === 'calendar') {
            const hasLocationFilters = this.activeFilters.locations.size > 0;
            const hasAreaFilters = this.activeFilters.areas.size > 0;
            
            if (!hasLocationFilters && !hasAreaFilters) {
                // Show all calendar days
                document.querySelectorAll('.calendar-day:not(.outside-month)').forEach(dayEl => {
                    dayEl.classList.remove('location-filtered-hidden');
                });
                return;
            }

            // Apply location/area filters to calendar days
            document.querySelectorAll('.calendar-day:not(.outside-month)').forEach(dayEl => {
                let showDay = false;
                const date = dayEl.dataset.date;
                const dayData = window.calendarView.calendarData.days.find(d => d.date === date);

                if (dayData) {
                    // Check location filters
                    if (hasLocationFilters && dayData.location) {
                        showDay = Array.from(this.activeFilters.locations).some(loc => 
                            dayData.location.includes(loc)
                        );
                    }

                    // Check area filters
                    if (hasAreaFilters && !showDay && dayData.locationArea) {
                        showDay = this.activeFilters.areas.has(dayData.locationArea);
                    }
                }

                dayEl.classList.toggle('location-filtered-hidden', !showDay);
            });
            
            // Update calendar view statistics
            if (typeof window.calendarView.updateCalendarFilterStats === 'function') {
                window.calendarView.updateCalendarFilterStats();
            }
        }
    }

    showAllDays() {
        // Clear table view filters
        document.querySelectorAll('.calendar-row').forEach(row => {
            row.classList.remove('location-filtered-hidden');
        });
        
        // Clear calendar view filters
        document.querySelectorAll('.calendar-day').forEach(dayEl => {
            dayEl.classList.remove('location-filtered-hidden');
        });
        
        this.clearFilterIndicator();
        this.updateFilterStats();
    }

    updateFilterIndicator() {
        let filterText = 'Active Location Filters: ';
        const filters = [];
        
        if (this.activeFilters.locations.size > 0) {
            filters.push(`Locations: ${Array.from(this.activeFilters.locations).join(', ')}`);
        }
        
        if (this.activeFilters.areas.size > 0) {
            filters.push(`Areas: ${Array.from(this.activeFilters.areas).join(', ')}`);
        }
        
        filterText += filters.join(' | ');
        this.showFilterIndicator(filterText);
    }

    showFilterIndicator(text) {
        let indicator = document.getElementById('location-filter-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'location-filter-indicator';
            indicator.className = 'location-filter-indicator';
            indicator.style.margin = '15px 0 20px 0';
            indicator.style.display = 'flex';
            indicator.style.justifyContent = 'space-between';
            indicator.style.alignItems = 'center';
            
            const textSpan = document.createElement('span');
            textSpan.textContent = text;
            
            const clearBtn = document.createElement('button');
            clearBtn.textContent = 'Clear Location Filters';
            clearBtn.className = 'button small secondary';
            clearBtn.onclick = () => this.clearAllFilters();
            
            indicator.appendChild(textSpan);
            indicator.appendChild(clearBtn);
            
            const locationAreas = document.querySelector('.location-areas');
            if (locationAreas) {
                locationAreas.parentNode.insertBefore(indicator, locationAreas);
            }
        } else {
            indicator.querySelector('span').textContent = text;
        }
    }

    clearFilterIndicator() {
        const indicator = document.getElementById('location-filter-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    updateFilterStats() {
        // Update existing filter stats to account for location filtering
        if (typeof updateFilterStats === 'function') {
            updateFilterStats();
        }
    }

    clearAllFilters() {
        this.activeFilters.locations.clear();
        this.activeFilters.areas.clear();
        
        document.querySelectorAll('.filter-active').forEach(el => {
            el.classList.remove('filter-active');
        });
        
        this.showAllDays();
    }

    setupClearFilters() {
        // The clear button is handled in the filter indicator
    }
}

// Make LocationFilter available globally
window.LocationFilter = LocationFilter;

// =======================================
// Feature Initialization Functions
// =======================================

/**
 * Get location areas and their colors from data attributes or elements.
 * @returns {object} An object mapping area names to color strings.
 */
function getLocationAreas() {
    const areas = {};
    // Try getting from dedicated area tags first
    const areaElements = document.querySelectorAll('.location-areas .area-tag');
    if (areaElements.length > 0) {
        areaElements.forEach(el => {
            // Extract name cleanly, excluding count if present
            const nameElement = el.cloneNode(true);
            const countElement = nameElement.querySelector('.area-count');
            if (countElement) {
                nameElement.removeChild(countElement);
            }
            const areaName = nameElement.textContent.trim();
            const backgroundColor = el.style.backgroundColor;
            if (areaName && backgroundColor) {
                areas[areaName] = backgroundColor;
            }
        });
    } else {
        // Fallback or alternative method if needed
        console.warn("Could not find .location-areas .area-tag elements.");
    }
    console.log("Detected Location Areas:", areas);
    return areas;
}
// Make it available globally for other scripts
window.getLocationAreas = getLocationAreas;

/**
 * Apply location area colors as CSS variables to calendar rows.
 * @param {object} areas - Object mapping area names to colors (from getLocationAreas).
 */
function applyLocationAreaColors(areas) {
    const rows = document.querySelectorAll('.calendar-row');
    
    rows.forEach(row => {
      const locationCell = row.querySelector('.location-cell');
      const areaAttribute = row.getAttribute('data-area');
      
      // If row has area attribute, use that
      if (areaAttribute && areas[areaAttribute]) {
        row.style.setProperty('--row-area-color', areas[areaAttribute]);
        row.classList.add('has-area-color');
        // Also set the data-color attribute for better print support
        row.setAttribute('data-color', areas[areaAttribute]);
        return;
      }
      
      // Otherwise try to find location in the row
      if (locationCell) {
        const locationText = locationCell.textContent.trim();
        
        // Find area that matches this location
        for (const areaName in areas) {
          if (locationText.includes(areaName)) {
            row.style.setProperty('--row-area-color', areas[areaName]);
            row.classList.add('has-area-color');
            // Also set the data-color attribute for better print support
            row.setAttribute('data-color', areas[areaName]);
            break;
          }
        }
      }
    });
}

// Make it available globally for other scripts
window.applyLocationAreaColors = applyLocationAreaColors;

/**
 * Apply colors to department tags based on embedded or default data.
 */
function applyDepartmentTagColors() {
    console.log("Applying department tag colors...");
    let departmentColors = {};
    const departmentDataElement = document.getElementById('department-data');

    const fallbackColors = { // Keep fallback just in case
        "SFX": "#ffd8e6", "STN": "#ffecd8", "CR": "#d8fff2", "ST": "#f2d8ff",
        "PR": "#d8fdff", "LL": "#e6ffd8", "VFX": "#d8e5ff", "ANI": "#ffedd8",
        "UW": "#d8f8ff", "INCY": "#f542dd", "TEST": "#067bf9"
    };

    if (departmentDataElement) {
        try {
            departmentColors = JSON.parse(departmentDataElement.textContent.trim());
            // console.log("Parsed department colors:", departmentColors);
        } catch (e) {
            console.error('Error parsing department data, using fallbacks:', e);
            departmentColors = fallbackColors;
        }
    } else {
        console.warn("Department data element not found, using fallbacks.");
        departmentColors = fallbackColors;
    }

    const departmentTags = document.querySelectorAll('.department-tag');
    departmentTags.forEach(tag => {
        const deptCode = tag.getAttribute('data-dept-code') || tag.textContent.trim();
        if (departmentColors[deptCode]) {
            tag.style.backgroundColor = departmentColors[deptCode];
            ensureTextContrast(tag); // Ensure text is readable
        } else {
            // console.warn(`No color found for department code: ${deptCode}`);
             // Apply a default neutral color?
             tag.style.backgroundColor = '#cccccc';
             ensureTextContrast(tag);
        }
    });
    console.log("Finished applying department tag colors.");
}

/**
 * Toggles visibility of calendar rows based on their type (e.g., 'weekend', 'shoot').
 * @param {string} rowType - The class name identifying the row type.
 * @param {boolean} isVisible - True to show, false to hide.
 */
function toggleRowType(rowType, isVisible) {
    // console.log(`Toggling row type ${rowType} to ${isVisible ? 'visible' : 'hidden'}`);
    const rows = document.querySelectorAll(`.calendar-row.${rowType}`);
    rows.forEach(row => {
        row.classList.toggle('filtered-hidden', !isVisible);
    });
    updateFilterStats(); // Update stats after visibility change
}

/**
 * Toggles visibility of calendar columns (header and cells).
 * @param {string} colName - The identifier for the column (e.g., 'sequence', 'second-unit').
 * @param {boolean} isVisible - True to show, false to hide.
 */
function toggleColumnVisibility(colName, isVisible) {
    // console.log(`Toggling column ${colName} to ${isVisible ? 'visible' : 'hidden'}`);
    const headers = document.querySelectorAll(`.${colName}-col`);
    const cells = document.querySelectorAll(`.${colName}-cell`);
    const displayValue = isVisible ? '' : 'none'; // Use '' to reset to default display

    headers.forEach(header => { header.style.display = displayValue; });
    cells.forEach(cell => { cell.style.display = displayValue; });
}

/**
 * Loads filter preferences from localStorage and updates checkbox states.
 */
function loadFilterPreferences() {
    try {
        const preferences = JSON.parse(localStorage.getItem('calendarFilterPrefs') || '{}');
        const mappings = {
            'filter-weekends': 'hideWeekends', 'filter-prep': 'hidePrep',
            'filter-holidays': 'hideHolidays', 'filter-hiatus': 'hideHiatus',
            'filter-shoot': 'hideShoot', 'filter-col-sequence': 'hideColSequence',
            'filter-col-second-unit': 'hideColSecondUnit', 'filter-col-sun-times': 'hideColSunTimes'
        };

        for (const [elementId, prefKey] of Object.entries(mappings)) {
            const toggle = document.getElementById(elementId);
            if (toggle && preferences[prefKey] !== undefined) {
                toggle.checked = !preferences[prefKey];
            } else if (toggle && preferences[prefKey] === undefined) {
                // If pref not set, ensure checkbox reflects default 'checked' state from HTML
                 toggle.checked = true; // Assuming default is checked
            }
        }
    } catch (error) {
        console.error("Error loading filter preferences:", error);
        // Optionally reset to defaults if parsing fails
    }
}

/**
 * Saves the current state of filter checkboxes to localStorage.
 */
function saveFilterPreferences() {
    const preferences = {};
    const mappings = {
        'filter-weekends': 'hideWeekends', 'filter-prep': 'hidePrep',
        'filter-holidays': 'hideHolidays', 'filter-hiatus': 'hideHiatus',
        'filter-shoot': 'hideShoot', 'filter-col-sequence': 'hideColSequence',
        'filter-col-second-unit': 'hideColSecondUnit', 'filter-col-sun-times': 'hideColSunTimes'
    };

    for (const [elementId, prefKey] of Object.entries(mappings)) {
        const toggle = document.getElementById(elementId);
        // Store the "hide" state, which is the opposite of the checkbox "checked" state
        preferences[prefKey] = toggle ? !toggle.checked : false;
    }

    localStorage.setItem('calendarFilterPrefs', JSON.stringify(preferences));
    // console.log("Saved Filter Prefs:", preferences);
}

/**
 * Applies all currently selected filters (both row and column).
 */
function applyAllFilters() {
    // console.log("Applying all filters based on checkbox states...");
    // Reset row visibility first
    document.querySelectorAll('.calendar-row').forEach(row => {
        row.classList.remove('filtered-hidden');
    });

    // Apply row filters
    const rowMappings = {
        'filter-weekends': 'weekend', 'filter-prep': 'prep', 'filter-holidays': 'holiday',
        'filter-hiatus': 'hiatus', 'filter-shoot': 'shoot'
    };
    for (const [elementId, rowType] of Object.entries(rowMappings)) {
        const toggle = document.getElementById(elementId);
        if (toggle && !toggle.checked) {
            toggleRowType(rowType, false);
        } else if (toggle && toggle.checked) {
             toggleRowType(rowType, true); // Ensure shown if checked (handles reset case)
        }
    }

    // Apply column filters
    const colMappings = {
        'filter-col-sequence': 'sequence', 'filter-col-second-unit': 'second-unit', 'filter-col-sun-times': 'sun-times'
    };
    for (const [elementId, colName] of Object.entries(colMappings)) {
        const toggle = document.getElementById(elementId);
        if (toggle) { // Check if toggle exists before applying
             toggleColumnVisibility(colName, toggle.checked);
        }
    }

    updateFilterStats(); // Update stats after applying all filters
    // console.log("Finished applying all filters.");
}

/**
 * FIXED VERSION - Replace in static/js/calendar.js around line 650
 * Updates the filter statistics display elements - ENHANCED VERSION
 */
function updateFilterStats() {
    // Check current view mode
    const isCalendarView = window.calendarView && window.calendarView.getCurrentView() === 'calendar';
    
    if (isCalendarView) {
        // Use calendar view elements
        const totalDays = document.querySelectorAll('.calendar-day:not(.outside-month)').length;
        const visibleDays = document.querySelectorAll('.calendar-day:not(.outside-month):not(.calendar-filtered-hidden):not(.location-filtered-hidden)').length;
        const totalShootDays = document.querySelectorAll('.calendar-day.shoot:not(.outside-month)').length;
        const visibleShootDays = document.querySelectorAll('.calendar-day.shoot:not(.outside-month):not(.calendar-filtered-hidden):not(.location-filtered-hidden)').length;
        
        updateStatsDisplay(totalDays, visibleDays, visibleShootDays, totalShootDays);
    } else {
        // Use table view elements with comprehensive hidden state checking
        const allRows = document.querySelectorAll('.calendar-row');
        const totalRows = allRows.length;
        
        // Count visible rows more accurately by checking all possible hidden states
        let visibleRows = 0;
        let visibleShootDays = 0;
        let totalShootDays = 0;
        
        allRows.forEach(row => {
            // Check if row is a shoot day
            const isShootDay = row.classList.contains('shoot');
            if (isShootDay) {
                totalShootDays++;
            }
            
            // Check ALL possible ways a row can be hidden
            const isHidden = row.classList.contains('filtered-hidden') || 
                           row.classList.contains('location-filtered-hidden') ||
                           row.classList.contains('search-hidden') ||
                           row.classList.contains('calendar-filtered-hidden') ||
                           row.style.display === 'none' ||
                           getComputedStyle(row).display === 'none';
            
            if (!isHidden) {
                visibleRows++;
                if (isShootDay) {
                    visibleShootDays++;
                }
            }
        });
        
        updateStatsDisplay(totalRows, visibleRows, visibleShootDays, totalShootDays);
    }
}

// Helper function to update the display elements
function updateStatsDisplay(totalRows, visibleRows, visibleShootDays, totalShootDays) {
    const statsTotal = document.getElementById('filter-stats-total');
    const statsVisible = document.getElementById('filter-stats-visible');
    const statsShootDays = document.getElementById('filter-stats-shoot-days');

    if (statsTotal) statsTotal.textContent = totalRows;
    if (statsVisible) statsVisible.textContent = visibleRows;
    if (statsShootDays) statsShootDays.textContent = `${visibleShootDays} / ${totalShootDays}`;
    
    // Optional debug logging - remove in production
    console.log(`Filter stats: ${visibleRows}/${totalRows} days visible, ${visibleShootDays}/${totalShootDays} shoot days`);
}

/**
 * Initializes the filter controls, loads preferences, and attaches event listeners.
 */
function initializeFilters() {
    console.log("Initializing filters...");
    const filterPanel = document.querySelector('.filter-panel');
    // Only initialize if filter panel elements exist on the page
    if (!filterPanel || !document.getElementById('filter-weekends')) {
        console.log("Filter panel/elements not found, skipping filter initialization.");
        return;
    }

    console.log("Filter elements found, setting up event listeners...");

    // Define mappings for easier event listener attachment
    const rowMappings = {
        'filter-weekends': 'weekend', 'filter-prep': 'prep', 'filter-holidays': 'holiday',
        'filter-hiatus': 'hiatus', 'filter-shoot': 'shoot'
    };
    const colMappings = {
        'filter-col-sequence': 'sequence', 'filter-col-second-unit': 'second-unit', 'filter-col-sun-times': 'sun-times'
    };

    // Load saved preferences BEFORE applying initial filters
    loadFilterPreferences();

    // Add event listeners to row type toggles
    for (const [elementId, rowType] of Object.entries(rowMappings)) {
        const toggle = document.getElementById(elementId);
        if (toggle) {
            toggle.addEventListener('change', function() {
                toggleRowType(rowType, this.checked);
                saveFilterPreferences(); // Save prefs on change
            });
        }
    }

    // Add event listeners to column visibility toggles
    for (const [elementId, colName] of Object.entries(colMappings)) {
        const toggle = document.getElementById(elementId);
        if (toggle) {
            toggle.addEventListener('change', function() {
                toggleColumnVisibility(colName, this.checked);
                saveFilterPreferences(); // Save prefs on change
            });
        }
    }

    // Reset button functionality
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            console.log("Resetting filters...");
            // Reset all checkboxes to checked (visible) state
            Object.keys(rowMappings).forEach(id => {
                const el = document.getElementById(id);
                if (el) el.checked = true;
            });
            Object.keys(colMappings).forEach(id => {
                const el = document.getElementById(id);
                if (el) el.checked = true;
            });

            applyAllFilters(); // Re-apply filters based on reset state
            saveFilterPreferences(); // Save the reset state
        });
    }

    // Apply initial filter state based on loaded preferences (or defaults)
    applyAllFilters();

    console.log("Filter initialization complete.");
}

/**
 * Search Filter Functionality for Calendar
 * To be added to static/js/calendar.js
 */

/**
 * Initialize the search filter
 */
function initializeSearchFilter() {
    console.log("Initializing search filter...");
    
    const searchInput = document.getElementById('calendar-search');
    const clearButton = document.getElementById('clear-search');
    const searchStatus = document.getElementById('search-status');
    const resultsCount = document.getElementById('search-results-count');
    const searchTerm = document.getElementById('search-term');
    
    if (!searchInput || !clearButton) {
        console.log("Search filter elements not found, skipping initialization.");
        return;
    }
    
    // Search debounce timer
    let searchTimeout;
    
    // Add event listeners
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = e.target.value.trim();
            applySearchFilter(query);
        }, 300); // Debounce search for 300ms
    });
    
    clearButton.addEventListener('click', function() {
        searchInput.value = '';
        applySearchFilter('');
        searchInput.focus();
    });
    
    console.log("Search filter initialized");
}

/**
 * Apply search filter to calendar rows
 * @param {string} query - Search query
 */
function applySearchFilter(query) {
    console.log(`Applying search filter: "${query}"`);
    
    const rows = document.querySelectorAll('.calendar-row');
    const searchStatus = document.getElementById('search-status');
    const resultsCount = document.getElementById('search-results-count');
    const searchTerm = document.getElementById('search-term');
    
    if (!query) {
        // Show all rows if query is empty
        rows.forEach(row => {
            row.classList.remove('search-hidden');
        });
        
        if (searchStatus) {
            searchStatus.style.display = 'none';
        }
        return;
    }
    
    // Convert query to lowercase for case-insensitive search
    const queryLower = query.toLowerCase();
    let matchCount = 0;
    
    rows.forEach(row => {
        // Search in multiple columns
        const dayNumber = row.querySelector('.day-cell')?.textContent || '';
        const mainUnit = row.querySelector('.main-unit-cell')?.textContent || '';
        const location = row.querySelector('.location-cell')?.textContent || '';
        const notes = row.querySelector('.notes-cell')?.textContent || '';
        const sequence = row.querySelector('.sequence-cell')?.textContent || '';
        const secondUnit = row.querySelector('.second-unit-cell')?.textContent || '';
        
        // Combine all searchable text
        const searchableText = `${dayNumber} ${mainUnit} ${location} ${notes} ${sequence} ${secondUnit}`.toLowerCase();
        
        // Check if any content matches the search query
        const isMatch = searchableText.includes(queryLower);
        
        // Toggle visibility based on match
        row.classList.toggle('search-hidden', !isMatch);
        
        if (isMatch) {
            matchCount++;
        }
    });
    
    // Update search status
    if (searchStatus && resultsCount && searchTerm) {
        searchStatus.style.display = 'block';
        resultsCount.textContent = matchCount;
        searchTerm.textContent = query;
    }
    
    // If using filter stats, update them
    if (typeof updateFilterStats === 'function') {
        updateFilterStats();
    }
    
    console.log(`Search complete: ${matchCount} matches found`);
}

/**
 * Enhanced calendar navigation with anchor support
 */
function initializeCalendarAnchors() {
    console.log("Initializing calendar anchors...");
    
    // Check if there's an anchor in the URL when the page loads
    if (window.location.hash) {
        const anchor = window.location.hash.substring(1); // Remove the #
        
        // Check if it's a day anchor (format: day-YYYY-MM-DD)
        if (anchor.startsWith('day-')) {
            const date = anchor.replace('day-', '');
            scrollToDay(date);
        }
    }
    
    // Add anchor IDs to calendar rows for easy navigation
    addAnchorIdsToCalendarRows();
}

/**
 * Add anchor IDs to calendar rows
 */
function addAnchorIdsToCalendarRows() {
    const calendarRows = document.querySelectorAll('.calendar-row[data-date]');
    
    calendarRows.forEach(row => {
        const date = row.getAttribute('data-date');
        if (date) {
            row.id = `day-${date}`;
        }
    });
}

/**
 * Scroll to a specific day in the calendar
 */
function scrollToDay(date) {
    const targetRow = document.getElementById(`day-${date}`);
    
    if (targetRow) {
        // Add a small delay to ensure the page has fully rendered
        setTimeout(() => {
            targetRow.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
            
            // Add a temporary highlight effect
            targetRow.classList.add('day-highlight');
            setTimeout(() => {
                targetRow.classList.remove('day-highlight');
            }, 3000);
            
            console.log(`Scrolled to day: ${date}`);
        }, 100);
    } else {
        console.warn(`Day not found: ${date}`);
    }
}

// Add the initialization call to the DOMContentLoaded listener in calendar.js
// This should be manually inserted as part of an update to the existing listener

/**
 * OLD CODE PLACEHELD FOR RELIC CALLS - Initializes the mobile menu toggle button functionality.
 */
function setupMobileMenu() {
    console.log("Mobile menu setup skipped - handled by mobile-menu.js");
    // Do nothing - mobile menu is now handled by mobile-menu.js
    return;
}

/**
 * Sets up click handlers for calendar rows in admin mode - 
 * IMPORTANT: No longer sets up drag and drop (moved to calendar-dragdrop.js)
 */
function setupAdminEventHandlers() {
    // Check if we're in admin mode (presence of .admin-calendar class)
    const isAdminMode = document.querySelector('.admin-calendar') !== null;
    const projectIdElement = document.getElementById('project-id');

    if (isAdminMode && projectIdElement) {
        console.log("Admin mode detected, setting up admin click handlers...");
        const projectId = projectIdElement.value;
        const calendarRows = document.querySelectorAll('.calendar-row');

        calendarRows.forEach(row => {
            // We only set up click handlers here, not drag and drop
            // Remove existing listener before adding new one to prevent duplicates if called multiple times
            row.removeEventListener('click', handleAdminRowClick); 
            // Add listener for row click navigation
            row.addEventListener('click', handleAdminRowClick);
        });
        
        console.log("Admin event handlers setup complete.");
    } else {
        console.log("Not in admin mode or projectId not found, skipping admin event handlers.");
    }
}

// Named function for row click handling
function handleAdminRowClick(event) {
    // Don't navigate if we're in the middle of a drag operation
    if (document.querySelector('.dragging')) {
        console.log('Click ignored during drag operation');
        return;
    }
    
    // Don't navigate if the click was on an interactive element
    if (event.target.closest('button, a')) {
        console.log('Click on interactive element ignored');
        return;
    }
    
    const date = this.dataset.date;
    const projectId = document.getElementById('project-id').value;
    
    if (date && projectId) {
        console.log(`Navigating to admin day view: /admin/day/${projectId}/${date}`);
        window.location.href = `/admin/day/${projectId}/${date}`;
    } else {
        console.warn("Could not navigate: Date or ProjectID missing from row.", {date, projectId});
    }
}

/**
 * Initializes scrollable table detection and touch interactions.
 */
function setupScrollableTables() {
    console.log("Setting up scrollable tables...");
    const tableWrappers = document.querySelectorAll('.calendar-table-wrapper');

    if (!tableWrappers.length) {
        console.log("No table wrappers found, skipping scrollable table setup.");
        return;
    }

    // Initial check and resize listener
    checkIfScrollable(); // Defined globally
    window.addEventListener('resize', checkIfScrollable);

    // Touch interactions for mobile
    tableWrappers.forEach(wrapper => {
        // Swipe/Scroll
        if (window.innerWidth <= 768) { // Check if likely mobile
            let startX, startScrollLeft;
            wrapper.addEventListener('touchstart', (e) => {
                startX = e.touches[0].pageX;
                startScrollLeft = wrapper.scrollLeft;
            }, { passive: true });
            wrapper.addEventListener('touchmove', (e) => {
                const x = e.touches[0].pageX;
                const dist = startX - x;
                wrapper.scrollLeft = startScrollLeft + dist;
            }, { passive: true });
        }

        // Double Tap Zoom/Fit (Optional - consider if needed with pinch zoom)
        let lastTap = 0;
        wrapper.addEventListener('touchend', function(e) {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;
            if (tapLength < 300 && tapLength > 0) { // Double tap threshold
                e.preventDefault();
                const table = wrapper.querySelector('.calendar-table');
                if (!table) return;
                // Example toggle: Fit width (consider usability)
                if (table.style.width === '100%') {
                    table.style.width = ''; // Reset width
                    table.style.fontSize = ''; // Reset font size
                    wrapper.classList.remove('fit-content'); // Example class
                } else {
                    table.style.width = '100%'; // Fit width
                    table.style.fontSize = '0.8rem'; // Adjust font size
                     wrapper.classList.add('fit-content'); // Example class
                }
            }
            lastTap = currentTime;
        });
    });
     console.log("Scrollable tables setup finished.");
}

/**
 * Initializes zoom controls for the calendar table.
 */
function setupZoomControls() {
    console.log("Setting up zoom controls...");
    // Assume controls are outside the wrappers, find them once
    const zoomInBtn = document.querySelector('.zoom-in');
    const zoomOutBtn = document.querySelector('.zoom-out');
    const fitWidthBtn = document.querySelector('.fit-width');
    const zoomLevelDisplay = document.querySelector('.zoom-level');
    const tableWrapper = document.querySelector('.calendar-table-wrapper'); // Assuming one main wrapper for zoom

    if (!zoomInBtn || !zoomOutBtn || !fitWidthBtn || !zoomLevelDisplay || !tableWrapper) {
        console.log("Zoom controls or table wrapper not found, skipping zoom setup.");
        return;
    }

    let currentZoom = 100; // Percentage

    const applyZoom = () => {
        // console.log(`Applying zoom: ${currentZoom}%`);
        zoomLevelDisplay.textContent = currentZoom + '%';
        tableWrapper.classList.remove('fit-width', 'zoom-50', 'zoom-75', 'zoom-125', 'zoom-150'); // Clear old zoom classes

        if (currentZoom !== 100) {
             tableWrapper.classList.add(`zoom-${currentZoom}`); // Use classes for 50, 75, 125, 150 if defined in CSS
        }

        // Check scrollability after zoom might change layout
        setTimeout(checkIfScrollable, 50); // Defined globally
    };

    zoomInBtn.addEventListener('click', () => {
        if (currentZoom < 150) { // Max zoom 150%
            currentZoom += 25;
            tableWrapper.classList.remove('fit-width'); // Ensure fit-width is off when zooming
            applyZoom();
        }
    });

    zoomOutBtn.addEventListener('click', () => {
        if (currentZoom > 50) { // Min zoom 50%
            currentZoom -= 25;
            tableWrapper.classList.remove('fit-width'); // Ensure fit-width is off when zooming
            applyZoom();
        }
    });

    fitWidthBtn.addEventListener('click', () => {
        const willFit = !tableWrapper.classList.contains('fit-width');
        tableWrapper.classList.toggle('fit-width', willFit);
        if (willFit) {
            zoomLevelDisplay.textContent = 'Fit';
             tableWrapper.classList.remove('zoom-50', 'zoom-75', 'zoom-125', 'zoom-150'); // Clear zoom classes
             // Reset direct scale if used
             // const table = tableWrapper.querySelector('.calendar-table');
             // if (table) { table.style.transform = ''; }
        } else {
            // Return to previous zoom level when toggling off
            applyZoom();
        }
         setTimeout(checkIfScrollable, 50); // Check scroll on fit toggle
    });

     // Hide scroll hint after user has scrolled (assuming one global hint)
     const scrollHint = document.querySelector('.scroll-hint');
     if (scrollHint) {
         tableWrapper.addEventListener('scroll', function() {
             if (tableWrapper.scrollLeft > 10) {
                 scrollHint.style.opacity = '0';
                 setTimeout(() => { scrollHint.style.display = 'none'; }, 500); // Hide after fade
             }
         }, { passive: true }); // Use passive listener for scroll
     }
     console.log("Zoom controls setup finished.");
}

// Helper function to extract calendar data from existing DOM
// ADD THIS FUNCTION BEFORE YOUR DOMContentLoaded EVENT LISTENER
function extractCalendarDataFromDOM() {
    const days = [];
    const rows = document.querySelectorAll('.calendar-row');
    
    rows.forEach(row => {
        const date = row.getAttribute('data-date');
        const area = row.getAttribute('data-area');
        
        if (date) {
            const dayData = {
                date: date,
                locationArea: area,
                locationAreaId: row.getAttribute('data-location-area-id'),
                isWeekend: row.classList.contains('weekend'),
                isHoliday: row.classList.contains('holiday'),
                isHiatus: row.classList.contains('hiatus'),
                isPrep: row.classList.contains('prep'),
                isShootDay: row.classList.contains('shoot'),
                isWorkingWeekend: row.classList.contains('working-weekend'),
                dayOfWeek: new Date(date).toLocaleDateString('en-US', { weekday: 'long' }),
                day: new Date(date).getDate(),
                month: new Date(date).getMonth() + 1,
                year: new Date(date).getFullYear()
            };

            // Extract shoot day number
            const shootDayElement = row.querySelector('.day-cell');
            if (shootDayElement && shootDayElement.textContent.trim()) {
                const shootDayText = shootDayElement.textContent.trim();
                if (shootDayText && !isNaN(shootDayText)) {
                    dayData.shootDay = parseInt(shootDayText);
                }
            }

            // Extract location
            const locationElement = row.querySelector('.location-name');
            if (locationElement) {
                dayData.location = locationElement.textContent.trim();
            }

            // Extract main unit
            const mainUnitElement = row.querySelector('.main-unit-cell');
            if (mainUnitElement) {
                dayData.mainUnit = mainUnitElement.textContent.trim();
            }

            // Extract departments
            const deptElements = row.querySelectorAll('.department-tag');
            dayData.departments = Array.from(deptElements).map(el => el.textContent.trim());

            // Extract notes
            const notesElement = row.querySelector('.notes-cell');
            if (notesElement) {
                dayData.notes = notesElement.textContent.trim();
            }

            days.push(dayData);
        }
    });

    // Get location areas from existing function
    const locationAreas = getLocationAreas ? getLocationAreas() : {};
    
    // Extract department data from existing tags
    const departments = [];
    document.querySelectorAll('.department-tag').forEach(tag => {
        const code = tag.textContent.trim();
        const color = tag.style.backgroundColor;
        if (code && !departments.find(d => d.code === code)) {
            departments.push({
                code: code,
                color: color || '#cccccc',
                name: code
            });
        }
    });

    return {
        days: days,
        locationAreas: Object.keys(locationAreas).map(name => ({
            name: name,
            color: locationAreas[name]
        })),
        departments: departments,
        areaColorMap: locationAreas
    };
}

// =======================================
// Main Initialization on DOMContentLoaded
// =======================================

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed. Running initializers...");

    // --- 1. Core Visual Setup ---
    try {
        const locationAreas = getLocationAreas();
        applyLocationAreaColors(locationAreas);
        applyDepartmentTagColors();
        enhanceLocationCounters(); // Ensure contrast/colors for counters
    } catch (error) {
        console.error("Error during core visual setup:", error);
    }

    // --- 2. Initialize Calendar View (NEW SECTION) ---
    try {
        if (typeof CalendarView !== 'undefined') {
            // Get calendar data from the global scope or data attributes
            let calendarData = null;
            let locations = [];
            let departments = [];

            // Try to get data from global variables (set by templates)
            if (typeof window.calendarData !== 'undefined') {
                calendarData = window.calendarData;
            }
            if (typeof window.locationsData !== 'undefined') {
                locations = window.locationsData;
            }

            // Fallback: try to extract from existing DOM elements
            if (!calendarData) {
                // Try to build calendar data from existing table rows
                calendarData = extractCalendarDataFromDOM();
            }

            if (calendarData && calendarData.days && calendarData.days.length > 0) {
                departments = calendarData.departments || [];
                window.calendarView = new CalendarView(calendarData, locations, departments);
                console.log('Calendar view initialized with enhanced filter management');                
            } else {
                console.log('No calendar data available for calendar view');
            }
        }
    } catch (error) {
        console.error("Error initializing calendar view:", error);
    }

    // --- NEW: Go to Today Button Setup ---
    try {
        const goToTodayBtn = document.getElementById('go-to-today-btn');
        if (goToTodayBtn) {
            goToTodayBtn.addEventListener('click', goToToday);
            updateGoToTodayButton(); // Update button with current info
            console.log("Go to Today button initialized");
        }
    } catch (error) {
        console.error("Error setting up Go to Today button:", error);
    }

    // --- NEW: Location Filtering Setup ---
    try {
        // Initialize location filtering after a short delay to ensure all elements are rendered
        setTimeout(() => {
            window.locationFilter = new LocationFilter();
            console.log("Location filtering initialized");
        }, 100);
    } catch (error) {
        console.error("Error setting up location filtering:", error);
    }

    // --- 2. Filter Setup ---
    try {
        initializeFilters(); // Initializes filter controls and applies initial state
    } catch (error) {
        console.error("Error during filter initialization:", error);
    }

    // --- 3. Mobile Menu Setup ---
    try {
        setupMobileMenu(); // Initializes the hamburger menu toggle
    } catch (error) {
        console.error("Error during mobile menu setup:", error);
    }

    // --- 4. Admin-Specific Features ---
    // This checks internally if it's the admin page
    try {
        setupAdminEventHandlers(); // Sets up row clicks only, not drag/drop
    } catch (error) {
        console.error("Error during admin event handler setup:", error);
    }

    // --- 5. Scrollable Table / Touch Features ---
    try {
        setupScrollableTables(); // Adds scroll indicators and touch interactions
    } catch (error) {
        console.error("Error during scrollable table setup:", error);
    }

    // --- 6. Zoom Controls ---
    try {
        setupZoomControls(); // Initializes zoom buttons
    } catch (error) {
        console.error("Error during zoom control setup:", error);
    }

    // --- 7. Sticky Header Enhancement --- ADD THIS NEW SECTION HERE
    try {
        // Add sticky header effects
        const tableWrappers = document.querySelectorAll('.calendar-table-wrapper');
        
        tableWrappers.forEach(wrapper => {
            // Add shadow to header on scroll
            wrapper.addEventListener('scroll', function() {
                const thead = this.querySelector('thead');
                if (this.scrollTop > 0) {
                    thead.classList.add('scrolled');
                } else {
                    thead.classList.remove('scrolled');
                }
            });
        });
        
        console.log("Sticky header enhancement added");
    } catch (error) {
        console.error("Error setting up sticky header:", error);
    }
    
     // --- NEW: Search Filter Setup ---
     try {
        initializeSearchFilter();
        console.log("Search filter initialization complete");
    } catch (error) {
        console.error("Error during search filter setup:", error);
    }

        // Add this new call
    try {
        initializeCalendarAnchors();
    } catch (error) {
        console.error("Error initializing calendar anchors:", error);
    }

    console.log("All initializers called.");
});