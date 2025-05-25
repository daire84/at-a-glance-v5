/**
 * Calendar View Module
 * Provides traditional calendar grid layout as an alternative to table view
 */

class CalendarView {
    constructor(calendarData, locations, departments) {
        this.calendarData = calendarData || { days: [] };
        this.locations = locations || [];
        this.departments = departments || [];
        this.currentView = 'table';
        this.isInitialized = false;
        
        // Wait for DOM to be ready before initializing  
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    init() {
        if (this.isInitialized) return;
        
        console.log('Initializing Calendar View...');
        this.createCalendarContainer();
        this.setupViewToggle();
        this.generateCalendarView();
        this.isInitialized = true;
        console.log('Calendar View initialized successfully');
    }

    createCalendarContainer() {
        // Check if container already exists
        if (document.getElementById('calendar-view')) return;

        // Create the calendar view container
        const container = document.createElement('div');
        container.id = 'calendar-view';
        container.className = 'calendar-view';
        
        // Insert after the table wrapper
        const tableWrapper = document.querySelector('.calendar-table-wrapper');
        if (tableWrapper && tableWrapper.parentNode) {
            tableWrapper.parentNode.insertBefore(container, tableWrapper.nextSibling);
        } else {
            // Fallback: append to calendar container
            const calendarContainer = document.querySelector('.calendar-container');
            if (calendarContainer) {
                calendarContainer.appendChild(container);
            }
        }
    }

    setupViewToggle() {
        // Check if toggle already exists
        if (document.querySelector('.view-toggle-container')) return;

        // Create view toggle controls
        const toggleContainer = this.createViewToggleHTML();
        
        // Insert before the calendar table wrapper
        const tableWrapper = document.querySelector('.calendar-table-wrapper');
        if (tableWrapper && tableWrapper.parentNode) {
            tableWrapper.parentNode.insertBefore(toggleContainer, tableWrapper);
        }

        // Add event listeners
        const toggleBtns = document.querySelectorAll('.view-toggle-btn');
        toggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                this.switchView(view);
            });
        });
    }

    createViewToggleHTML() {
        const toggleDiv = document.createElement('div');
        toggleDiv.className = 'view-toggle-container';
        toggleDiv.innerHTML = `
            <div class="view-toggle">
                <button class="view-toggle-btn active" data-view="table">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="7" height="3"></rect>
                        <rect x="14" y="3" width="7" height="3"></rect>
                        <rect x="3" y="10" width="7" height="3"></rect>
                        <rect x="14" y="10" width="7" height="3"></rect>
                        <rect x="3" y="17" width="7" height="3"></rect>
                        <rect x="14" y="17" width="7" height="3"></rect>
                    </svg>
                    Table View
                </button>
                <button class="view-toggle-btn" data-view="calendar">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    Calendar View
                </button>
            </div>
        `;
        return toggleDiv;
    }

    switchView(view) {
        this.currentView = view;
        console.log(`Switching to ${view} view`);
        
        // Update toggle buttons
        document.querySelectorAll('.view-toggle-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === view);
        });

        // Show/hide views
        const tableView = document.querySelector('.calendar-table-wrapper');
        const calendarView = document.querySelector('.calendar-view');

        if (view === 'calendar') {
            if (tableView) tableView.style.display = 'none';
            if (calendarView) {
                calendarView.classList.add('active');
                calendarView.style.display = 'block';
            }
            
            // Update filter info and disable irrelevant filters
            this.updateFilterInfoForView('calendar');
            this.toggleFilterAvailability('calendar');
            
        } else {
            if (tableView) tableView.style.display = 'block';
            if (calendarView) {
                calendarView.classList.remove('active');
                calendarView.style.display = 'none';
            }
            
            // Update filter info and enable all filters
            this.updateFilterInfoForView('table');
            this.toggleFilterAvailability('table');
        }

        // Apply current filters to new view
        setTimeout(() => {
            if (window.locationFilter) {
                if (view === 'calendar') {
                    this.applyFiltersToCalendarView();
                } else {
                    // Re-apply table filters
                    if (typeof window.locationFilter.applyFilters === 'function') {
                        window.locationFilter.applyFilters();
                    }
                }
            }
        }, 100);
    }

    updateFilterInfoForView(view) {
        const tableInfo = document.querySelector('.table-view-info');
        const calendarInfo = document.querySelector('.calendar-view-info');
        
        if (tableInfo && calendarInfo) {
            if (view === 'calendar') {
                tableInfo.style.display = 'none';
                calendarInfo.style.display = 'inline';
            } else {
                tableInfo.style.display = 'inline';
                calendarInfo.style.display = 'none';
            }
        }
    }

    toggleFilterAvailability(view) {
        // Disable weekend and shoot day filters in calendar view
        const weekendFilter = document.getElementById('filter-weekends');
        const shootFilter = document.getElementById('filter-shoot');
        const weekendLabel = weekendFilter ? weekendFilter.closest('label') : null;
        const shootLabel = shootFilter ? shootFilter.closest('label') : null;
        
        if (view === 'calendar') {
            // Disable weekend and shoot filters
            if (weekendFilter) {
                weekendFilter.disabled = true;
                weekendFilter.style.opacity = '0.5';
            }
            if (shootFilter) {
                shootFilter.disabled = true;
                shootFilter.style.opacity = '0.5';
            }
            if (weekendLabel) weekendLabel.style.opacity = '0.5';
            if (shootLabel) shootLabel.style.opacity = '0.5';
            
        } else {
            // Re-enable all filters
            if (weekendFilter) {
                weekendFilter.disabled = false;
                weekendFilter.style.opacity = '1';
            }
            if (shootFilter) {
                shootFilter.disabled = false;
                shootFilter.style.opacity = '1';
            }
            if (weekendLabel) weekendLabel.style.opacity = '1';
            if (shootLabel) shootLabel.style.opacity = '1';
        }
    }

    generateCalendarView() {
        if (!this.calendarData?.days || this.calendarData.days.length === 0) {
            console.warn('No calendar data available for calendar view');
            return;
        }

        const calendarContainer = document.getElementById('calendar-view');
        if (!calendarContainer) {
            console.error('Calendar view container not found');
            return;
        }
        
        // Group days by month
        const monthGroups = this.groupDaysByMonth(this.calendarData.days);
        
        // Generate HTML for each month
        calendarContainer.innerHTML = '';
        monthGroups.forEach(month => {
            const monthHtml = this.generateMonthHtml(month);
            calendarContainer.appendChild(monthHtml);
        });

        // Add click handlers for day editing (admin only)
        if (document.querySelector('.admin-calendar')) {
            this.addDayClickHandlers();
        }

        console.log(`Generated calendar view with ${monthGroups.length} months`);
    }

    groupDaysByMonth(days) {
        const months = {};
        
        days.forEach(day => {
            try {
                const date = new Date(day.date);
                const monthKey = `${date.getFullYear()}-${date.getMonth()}`;
                
                if (!months[monthKey]) {
                    months[monthKey] = {
                        year: date.getFullYear(),
                        month: date.getMonth(),
                        monthName: date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }),
                        days: []
                    };
                }
                
                months[monthKey].days.push(day);
            } catch (error) {
                console.warn('Invalid date format:', day.date);
            }
        });

        return Object.values(months).sort((a, b) => {
            return new Date(a.year, a.month) - new Date(b.year, b.month);
        });
    }

    generateMonthHtml(month) {
        const monthDiv = document.createElement('div');
        monthDiv.className = 'calendar-month';

        // Month header
        const header = document.createElement('div');
        header.className = 'calendar-month-header';
        header.textContent = month.monthName;
        monthDiv.appendChild(header);

        // Calendar grid
        const grid = document.createElement('div');
        grid.className = 'calendar-grid';

        // Add day headers
        const dayHeaders = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        dayHeaders.forEach(day => {
            const headerDiv = document.createElement('div');
            headerDiv.className = 'calendar-day-header';
            headerDiv.textContent = day;
            grid.appendChild(headerDiv);
        });

        // Generate calendar grid with proper week layout
        const monthDays = this.generateMonthGrid(month.year, month.month, month.days);
        monthDays.forEach(day => {
            grid.appendChild(this.createDayElement(day));
        });

        monthDiv.appendChild(grid);
        return monthDiv;
    }

    generateMonthGrid(year, month, monthDays) {
        // Create a map of days for quick lookup
        const dayMap = {};
        monthDays.forEach(day => {
            const date = new Date(day.date);
            dayMap[date.getDate()] = day;
        });

        // Get first day of month and total days
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();

        // Calculate starting position (Monday = 0)
        const startDay = (firstDay.getDay() + 6) % 7;

        const gridDays = [];

        // Add previous month's trailing days
        for (let i = startDay - 1; i >= 0; i--) {
            const prevDate = new Date(year, month, -i);
            gridDays.push({
                date: prevDate.toISOString().split('T')[0],
                day: prevDate.getDate(),
                outsideMonth: true
            });
        }

        // Add current month's days
        for (let day = 1; day <= daysInMonth; day++) {
            const dayData = dayMap[day];
            if (dayData) {
                gridDays.push(dayData);
            } else {
                // Create placeholder for days without data
                gridDays.push({
                    date: new Date(year, month, day).toISOString().split('T')[0],
                    day: day,
                    outsideMonth: false
                });
            }
        }

        // Fill remaining cells to complete the grid (should be multiple of 7)
        const totalCells = Math.ceil(gridDays.length / 7) * 7;
        const remaining = totalCells - gridDays.length;
        
        for (let i = 1; i <= remaining; i++) {
            const nextDate = new Date(year, month + 1, i);
            gridDays.push({
                date: nextDate.toISOString().split('T')[0],
                day: nextDate.getDate(),
                outsideMonth: true
            });
        }

        return gridDays;
    }

    createDayElement(day) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'calendar-day';
        dayDiv.dataset.date = day.date;

        // Add day type classes
        if (day.outsideMonth) {
            dayDiv.classList.add('outside-month');
        } else {
            if (day.dayType) {
                dayDiv.classList.add(day.dayType);
            }
            if (day.isWeekend) dayDiv.classList.add('weekend');
            if (day.isHoliday) dayDiv.classList.add('holiday');
            if (day.isHiatus) dayDiv.classList.add('hiatus');
            if (day.isPrep) dayDiv.classList.add('prep');
            if (day.isShootDay) dayDiv.classList.add('shoot');
            if (day.isWorkingWeekend) dayDiv.classList.add('working-weekend');
            if (day.locationArea || day.locationAreaId) dayDiv.classList.add('has-area-color');
        }

        // Set area color if available
        if (day.locationAreaId && this.calendarData.areaColorMap) {
            const color = this.calendarData.areaColorMap[day.locationAreaId];
            if (color) {
                dayDiv.style.setProperty('--row-area-color', color);
            }
        } else if (day.locationArea && this.calendarData.locationAreas) {
            // Fallback: find area by name
            const area = this.calendarData.locationAreas.find(a => a.name === day.locationArea);
            if (area && area.color) {
                dayDiv.style.setProperty('--row-area-color', area.color);
            }
        }

        if (!day.outsideMonth) {
            // Day number
            const dayNumber = document.createElement('div');
            dayNumber.className = 'calendar-day-number';
            dayNumber.textContent = new Date(day.date).getDate();
            dayDiv.appendChild(dayNumber);

            // Shoot day number
            if (day.shootDay) {
                const shootDay = document.createElement('div');
                shootDay.className = 'calendar-shoot-day';
                shootDay.textContent = day.shootDay;
                dayDiv.appendChild(shootDay);
            }

            // Day content
            const content = document.createElement('div');
            content.className = 'calendar-day-content';

            // Location
            if (day.location) {
                const location = document.createElement('div');
                location.className = 'calendar-location';
                location.textContent = day.location;
                content.appendChild(location);
            }

            // Main unit (truncated)
            if (day.mainUnit) {
                const mainUnit = document.createElement('div');
                mainUnit.className = 'calendar-main-unit';
                mainUnit.textContent = day.mainUnit;
                content.appendChild(mainUnit);
            }

            // Department tags (limit to 3)
            if (day.departments && day.departments.length > 0) {
                const depts = document.createElement('div');
                depts.className = 'calendar-departments';
                
                day.departments.slice(0, 3).forEach(deptCode => {
                    const dept = this.departments?.find(d => d.code === deptCode);
                    if (dept) {
                        const tag = document.createElement('span');
                        tag.className = 'calendar-department-tag';
                        tag.textContent = deptCode;
                        tag.style.backgroundColor = dept.color;
                        tag.style.color = this.getContrastColor(dept.color);
                        depts.appendChild(tag);
                    } else {
                        // Fallback for unknown departments
                        const tag = document.createElement('span');
                        tag.className = 'calendar-department-tag';
                        tag.textContent = deptCode;
                        tag.style.backgroundColor = '#cccccc';
                        tag.style.color = '#333333';
                        depts.appendChild(tag);
                    }
                });
                
                content.appendChild(depts);
            }

            // Status badge for special day types
            if (day.isPrep || (day.isWeekend && !day.isWorkingWeekend) || day.isHoliday || day.isHiatus) {
                const badge = document.createElement('div');
                badge.className = 'calendar-status-badge';
                
                if (day.isPrep) {
                    badge.classList.add('prep');
                    badge.textContent = 'Prep';
                } else if (day.isHoliday) {
                    badge.classList.add('holiday');
                    badge.textContent = 'Holiday';
                } else if (day.isHiatus) {
                    badge.classList.add('hiatus');
                    badge.textContent = 'Hiatus';
                } else if (day.isWeekend && !day.isWorkingWeekend) {
                    badge.classList.add('weekend');
                    badge.textContent = 'Weekend';
                }
                
                if (badge.textContent) {
                    dayDiv.appendChild(badge);
                }
            }

            dayDiv.appendChild(content);
        } else {
            // Outside month - just show day number
            const dayNumber = document.createElement('div');
            dayNumber.className = 'calendar-day-number';
            dayNumber.textContent = new Date(day.date).getDate();
            dayDiv.appendChild(dayNumber);
        }

        return dayDiv;
    }

    addDayClickHandlers() {
        const projectId = document.getElementById('project-id')?.value;
        if (!projectId) return;

        document.querySelectorAll('.calendar-day:not(.outside-month)').forEach(dayEl => {
            dayEl.addEventListener('click', (e) => {
                // Don't navigate if clicking on a button or during drag operation
                if (e.target.closest('button') || document.querySelector('.dragging')) {
                    return;
                }
                
                const date = dayEl.dataset.date;
                if (date) {
                    window.location.href = `/admin/day/${projectId}/${date}`;
                }
            });
        });
    }

    getContrastColor(backgroundColor) {
        if (!backgroundColor) return '#000000';
        
        // Remove # if present
        const hex = backgroundColor.replace('#', '');
        
        // Handle 3-character hex codes
        const fullHex = hex.length === 3 ? 
            hex.split('').map(c => c + c).join('') : hex;
        
        if (fullHex.length !== 6) return '#000000';
        
        const r = parseInt(fullHex.substr(0, 2), 16);
        const g = parseInt(fullHex.substr(2, 2), 16);
        const b = parseInt(fullHex.substr(4, 2), 16);
        
        // Calculate brightness using YIQ formula
        const brightness = (r * 299 + g * 587 + b * 114) / 1000;
        return brightness > 128 ? '#000000' : '#ffffff';
    }

    // Apply current filters to calendar view
    applyFiltersToCalendarView() {
        if (!window.locationFilter) return;

        const hasLocationFilters = window.locationFilter.activeFilters.locations.size > 0;
        const hasAreaFilters = window.locationFilter.activeFilters.areas.size > 0;
        
        // Also check for row type filters that make sense in calendar view
        const hidePrepDays = document.getElementById('filter-prep') && !document.getElementById('filter-prep').checked;
        const hideHiatusDays = document.getElementById('filter-hiatus') && !document.getElementById('filter-hiatus').checked;
        const hideHolidayDays = document.getElementById('filter-holidays') && !document.getElementById('filter-holidays').checked;

        document.querySelectorAll('.calendar-day:not(.outside-month)').forEach(dayEl => {
            let showDay = true;
            const date = dayEl.dataset.date;
            const dayData = this.calendarData.days.find(d => d.date === date);

            if (dayData) {
                // Apply location/area filters
                if (hasLocationFilters || hasAreaFilters) {
                    let locationMatch = false;
                    
                    // Check location filters
                    if (hasLocationFilters && dayData.location) {
                        locationMatch = Array.from(window.locationFilter.activeFilters.locations).some(loc => 
                            dayData.location.includes(loc)
                        );
                    }

                    // Check area filters
                    if (hasAreaFilters && !locationMatch && dayData.locationArea) {
                        locationMatch = window.locationFilter.activeFilters.areas.has(dayData.locationArea);
                    }
                    
                    if (!locationMatch) {
                        showDay = false;
                    }
                }
                
                // Apply day type filters that make sense in calendar view
                if (showDay && hidePrepDays && dayData.isPrep) {
                    showDay = false;
                }
                
                if (showDay && hideHiatusDays && dayData.isHiatus) {
                    showDay = false;
                }
                
                if (showDay && hideHolidayDays && dayData.isHoliday) {
                    showDay = false;
                }
            }

            dayEl.classList.toggle('location-filtered-hidden', !showDay);
        });
        
        // Update filter stats to account for calendar view
        this.updateCalendarFilterStats();
    }

    // Add this new method to update filter statistics for calendar view
    updateCalendarFilterStats() {
        if (this.currentView !== 'calendar') return;
        
        const totalDays = document.querySelectorAll('.calendar-day:not(.outside-month)').length;
        const visibleDays = document.querySelectorAll('.calendar-day:not(.outside-month):not(.location-filtered-hidden)').length;
        const totalShootDays = document.querySelectorAll('.calendar-day.shoot:not(.outside-month)').length;
        const visibleShootDays = document.querySelectorAll('.calendar-day.shoot:not(.outside-month):not(.location-filtered-hidden)').length;

        const statsTotal = document.getElementById('filter-stats-total');
        const statsVisible = document.getElementById('filter-stats-visible');
        const statsShootDays = document.getElementById('filter-stats-shoot-days');

        if (statsTotal) statsTotal.textContent = totalDays;
        if (statsVisible) statsVisible.textContent = visibleDays;
        if (statsShootDays) statsShootDays.textContent = `${visibleShootDays} / ${totalShootDays}`;
    }

    // Update calendar view with new data
    updateData(calendarData, locations, departments) {
        this.calendarData = calendarData || { days: [] };
        this.locations = locations || [];
        this.departments = departments || [];
        
        if (this.isInitialized) {
            this.generateCalendarView();
        }
    }

    // Get current view
    getCurrentView() {
        return this.currentView;
    }

    // Refresh the calendar view
    refresh() {
        if (this.isInitialized) {
            this.generateCalendarView();
        }
    }
}

// Make CalendarView available globally
window.CalendarView = CalendarView;

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CalendarView;
}