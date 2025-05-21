/**
 * Enhanced Day Editor JavaScript
 * To be created as static/js/day-editor-enhanced.js
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing enhanced day editor...');
    
    // Get project data from the script tag
    const projectDataElement = document.getElementById('project-data');
    let projectData = {};
    
    if (projectDataElement) {
        try {
            projectData = JSON.parse(projectDataElement.textContent);
        } catch (e) {
            console.error('Error parsing project data:', e);
        }
    }
    
    const projectId = projectData.projectId;
    const currentDate = projectData.currentDate;
    
    // Get form elements
    const dayForm = document.getElementById('day-form');
    const saveStayBtn = document.getElementById('save-stay');
    const saveExitBtn = document.getElementById('save-exit');
    const exitEditorBtn = document.getElementById('exit-editor');
    const prevDayBtn = document.getElementById('prev-day');
    const nextDayBtn = document.getElementById('next-day');
    const prevDayBottomBtn = document.getElementById('prev-day-bottom');
    const nextDayBottomBtn = document.getElementById('next-day-bottom');
    
    // Save status indicator
    const saveStatus = document.getElementById('save-status');
    
    // Track if there are unsaved changes
    let hasUnsavedChanges = false;
    let isNavigating = false;
    
    // Track form changes
    if (dayForm) {
        dayForm.addEventListener('input', function() {
            hasUnsavedChanges = true;
        });
        
        dayForm.addEventListener('change', function() {
            hasUnsavedChanges = true;
        });
    }
    
    // Initialize navigation
    initializeNavigation();
    
    // Add event listeners
    if (saveStayBtn) {
        saveStayBtn.addEventListener('click', function(e) {
            e.preventDefault();
            saveDay(false); // Save but don't exit
        });
    }
    
    if (saveExitBtn) {
        saveExitBtn.addEventListener('click', function(e) {
            e.preventDefault();
            saveDay(true); // Save and exit
        });
    }
    
    if (exitEditorBtn) {
        exitEditorBtn.addEventListener('click', function(e) {
            e.preventDefault();
            exitEditor();
        });
    }
    
    // Navigation button events
    [prevDayBtn, prevDayBottomBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function() {
                navigateToDay('previous');
            });
        }
    });
    
    [nextDayBtn, nextDayBottomBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function() {
                navigateToDay('next');
            });
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+S or Cmd+S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            saveDay(false);
        }
        
        // Ctrl+Enter or Cmd+Enter to save and exit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            saveDay(true);
        }
        
        // Escape to exit (with confirmation if unsaved changes)
        if (e.key === 'Escape') {
            e.preventDefault();
            exitEditor();
        }
        
        // Alt+Left arrow for previous day
        if (e.altKey && e.key === 'ArrowLeft') {
            e.preventDefault();
            navigateToDay('previous');
        }
        
        // Alt+Right arrow for next day
        if (e.altKey && e.key === 'ArrowRight') {
            e.preventDefault();
            navigateToDay('next');
        }
    });
    
    // Add keyboard shortcuts indicator
    addKeyboardShortcutsIndicator();
    
    // Warn about unsaved changes when leaving the page
    window.addEventListener('beforeunload', function(e) {
        if (hasUnsavedChanges && !isNavigating) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
    
    /**
     * Initialize navigation by fetching calendar data
     */
    async function initializeNavigation() {
        try {
            // Fetch calendar data to build navigation
            const response = await fetch(`/api/projects/${projectId}/calendar`);
            if (!response.ok) {
                throw new Error('Failed to fetch calendar data');
            }
            
            const calendarData = await response.json();
            const shootDays = getShootDays(calendarData);
            
            updateNavigationButtons(shootDays);
            
        } catch (error) {
            console.error('Error initializing navigation:', error);
            // Disable navigation buttons if we can't load calendar data
            disableNavigationButtons();
        }
    }
    
    /**
     * Extract shoot days from calendar data
     */
    function getShootDays(calendarData) {
        if (!calendarData.days) return [];
        
        return calendarData.days
            .filter(day => day.isShootDay || day.isPrep) // Include both shoot and prep days
            .map(day => ({
                date: day.date,
                shootDay: day.shootDay,
                isPrep: day.isPrep,
                dayOfWeek: day.dayOfWeek
            }))
            .sort((a, b) => new Date(a.date) - new Date(b.date));
    }
    
    /**
     * Update navigation button states
     */
    function updateNavigationButtons(shootDays) {
        const currentIndex = shootDays.findIndex(day => day.date === currentDate);
        
        const hasPrevious = currentIndex > 0;
        const hasNext = currentIndex < shootDays.length - 1;
        
        // Update all navigation buttons
        [prevDayBtn, prevDayBottomBtn].forEach(btn => {
            if (btn) {
                btn.disabled = !hasPrevious;
                if (hasPrevious && shootDays[currentIndex - 1]) {
                    const prevDay = shootDays[currentIndex - 1];
                    const label = prevDay.isPrep ? `Prep Day` : `Day ${prevDay.shootDay}`;
                    btn.title = `Previous: ${label} (${prevDay.date})`;
                }
            }
        });
        
        [nextDayBtn, nextDayBottomBtn].forEach(btn => {
            if (btn) {
                btn.disabled = !hasNext;
                if (hasNext && shootDays[currentIndex + 1]) {
                    const nextDay = shootDays[currentIndex + 1];
                    const label = nextDay.isPrep ? `Prep Day` : `Day ${nextDay.shootDay}`;
                    btn.title = `Next: ${label} (${nextDay.date})`;
                }
            }
        });
        
        // Store shoot days for navigation
        window.shootDays = shootDays;
        window.currentDayIndex = currentIndex;
    }
    
    /**
     * Disable all navigation buttons
     */
    function disableNavigationButtons() {
        [prevDayBtn, nextDayBtn, prevDayBottomBtn, nextDayBottomBtn].forEach(btn => {
            if (btn) {
                btn.disabled = true;
            }
        });
    }
    
    /**
     * Save the current day
     */
    async function saveDay(shouldExit = false) {
        if (!dayForm) return;
        
        try {
            showSaveStatus('saving', 'Saving changes...');
            
            // Get form data
            const formData = new FormData(dayForm);
            
            // Send save request
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to save changes');
            }
            
            // Mark as saved
            hasUnsavedChanges = false;
            showSaveStatus('success', 'Changes saved');
            
            if (shouldExit) {
                exitEditor();
            }
            
        } catch (error) {
            console.error('Error saving day:', error);
            showSaveStatus('error', 'Save failed');
        }
    }
    
    /**
     * Navigate to previous or next day
     */
    async function navigateToDay(direction) {
        // Check for unsaved changes
        if (hasUnsavedChanges) {
            const shouldSave = confirm('You have unsaved changes. Would you like to save them before navigating?');
            if (shouldSave) {
                try {
                    await saveDay(false);
                } catch (error) {
                    alert('Failed to save changes. Navigation cancelled.');
                    return;
                }
            }
        }
        
        const shootDays = window.shootDays;
        const currentIndex = window.currentDayIndex;
        
        if (!shootDays || currentIndex === undefined) {
            console.error('Navigation data not available');
            return;
        }
        
        let targetIndex;
        if (direction === 'previous') {
            targetIndex = currentIndex - 1;
        } else if (direction === 'next') {
            targetIndex = currentIndex + 1;
        }
        
        if (targetIndex < 0 || targetIndex >= shootDays.length) {
            console.log('No more days in that direction');
            return;
        }
        
        const targetDay = shootDays[targetIndex];
        const targetUrl = `/admin/day/${projectId}/${targetDay.date}`;
        
        // Set navigation flag to prevent beforeunload warning
        isNavigating = true;
        
        // Add loading state to navigation buttons
        setNavigationLoading(true);
        
        // Navigate to the target day
        window.location.href = targetUrl;
    }
    
    /**
     * Exit the editor and return to calendar
     */
    function exitEditor() {
        if (hasUnsavedChanges) {
            const shouldSave = confirm('You have unsaved changes. Would you like to save them before exiting?');
            if (shouldSave) {
                saveDay(true);
                return;
            }
        }
        
        // Set navigation flag
        isNavigating = true;
        
        // Return to calendar with anchor to current day
        const calendarUrl = `/admin/calendar/${projectId}#day-${currentDate}`;
        window.location.href = calendarUrl;
    }
    
    /**
     * Show save status indicator
     */
    function showSaveStatus(type, message) {
        if (!saveStatus) return;
        
        const statusIcon = saveStatus.querySelector('.status-icon');
        const statusText = saveStatus.querySelector('.status-text');
        
        // Update content
        if (statusIcon) {
            statusIcon.textContent = type === 'saving' ? '⏳' : type === 'success' ? '✓' : '✗';
        }
        if (statusText) {
            statusText.textContent = message;
        }
        
        // Update styling
        saveStatus.className = `save-status ${type}`;
        saveStatus.style.display = 'flex';
        
        // Auto-hide after a delay (except for errors)
        if (type !== 'error') {
            setTimeout(() => {
                saveStatus.style.display = 'none';
            }, type === 'saving' ? 1000 : 3000);
        }
    }
    
    /**
     * Set loading state for navigation buttons
     */
    function setNavigationLoading(isLoading) {
        [prevDayBtn, nextDayBtn, prevDayBottomBtn, nextDayBottomBtn].forEach(btn => {
            if (btn) {
                if (isLoading) {
                    btn.classList.add('loading');
                    btn.disabled = true;
                } else {
                    btn.classList.remove('loading');
                }
            }
        });
    }
    
    /**
     * Add keyboard shortcuts indicator
     */
    function addKeyboardShortcutsIndicator() {
        const shortcuts = document.createElement('div');
        shortcuts.className = 'keyboard-shortcuts';
        shortcuts.innerHTML = `
            <div class="shortcut-item">
                <span>Save:</span>
                <span class="shortcut-key">Ctrl+S</span>
            </div>
            <div class="shortcut-item">
                <span>Save & Exit:</span>
                <span class="shortcut-key">Ctrl+Enter</span>
            </div>
            <div class="shortcut-item">
                <span>Previous Day:</span>
                <span class="shortcut-key">Alt+←</span>
            </div>
            <div class="shortcut-item">
                <span>Next Day:</span>
                <span class="shortcut-key">Alt+→</span>
            </div>
            <div class="shortcut-item">
                <span>Exit:</span>
                <span class="shortcut-key">Esc</span>
            </div>
        `;
        
        document.body.appendChild(shortcuts);
    }
    
    console.log('Enhanced day editor initialized successfully');
});
