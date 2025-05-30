/**
 * Print View Management
 * Add this to static/js/calendar-view.js (append to existing file)
 * OR create as separate file static/js/print-manager.js
 */

class PrintManager {
    constructor() {
        this.init();
    }

    init() {
        // Override the default print behavior
        this.setupPrintHandler();
        
        // Listen for print events
        window.addEventListener('beforeprint', () => this.beforePrint());
        window.addEventListener('afterprint', () => this.afterPrint());
        
        // Handle Ctrl+P and Cmd+P
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                this.handlePrint();
            }
        });
    }

    setupPrintHandler() {
        // Find and replace existing print buttons
        const printButtons = document.querySelectorAll('.print-button, [onclick*="print"]');
        
        printButtons.forEach(button => {
            // Remove existing onclick handlers
            button.removeAttribute('onclick');
            
            // Add new click handler
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handlePrint();
            });
        });
    }

    handlePrint() {
        console.log('Custom print handler triggered');
        
        // Determine current view
        const currentView = this.getCurrentView();
        console.log(`Printing in ${currentView} view`);
        
        // Prepare for printing
        this.beforePrint();
        
        // Trigger print
        setTimeout(() => {
            window.print();
        }, 100);
    }

    getCurrentView() {
        // Check if CalendarView exists and is active
        if (window.calendarView) {
            return window.calendarView.getCurrentView();
        }
        
        // Fallback: check DOM visibility
        const calendarView = document.querySelector('.calendar-view');
        const tableView = document.querySelector('.calendar-table-wrapper');
        
        if (calendarView && calendarView.style.display !== 'none' && calendarView.classList.contains('active')) {
            return 'calendar';
        } else if (tableView && tableView.style.display !== 'none') {
            return 'table';
        }
        
        // Default to table view
        return 'table';
    }

    beforePrint() {
        const currentView = this.getCurrentView();
        console.log(`Preparing ${currentView} view for printing`);
        
        // Add body class to indicate current view for print CSS
        document.body.classList.add(`print-${currentView}-view`);
        
        // For table view, add page break classes to keep first page clean
        if (currentView === 'table') {
            const tableWrapper = document.querySelector('.calendar-table-wrapper');
            if (tableWrapper) {
                tableWrapper.classList.add('print-page-break');
            }
            
            // Add class to last info section to force page break
            const locationCounters = document.querySelector('.location-counters');
            if (locationCounters) {
                locationCounters.classList.add('print-first-page-content');
            }
        }
        
        // Hide the non-active view completely for printing
        if (currentView === 'calendar') {
            this.hideForPrint('.calendar-table-wrapper');
            this.showForPrint('.calendar-view');
        } else {
            this.hideForPrint('.calendar-view');
            this.showForPrint('.calendar-table-wrapper');
        }
        
        // Hide UI elements that shouldn't print
        this.hideForPrint('.view-toggle-container');
        this.hideForPrint('.calendar-actions');
        this.hideForPrint('.filter-panel');
        this.hideForPrint('.admin-actions');
        this.hideForPrint('.calendar-mobile-controls');
        this.hideForPrint('.zoom-controls');
        this.hideForPrint('.scroll-hint');
        this.hideForPrint('.version-selector');
        
        // Ensure counters and headers still print
        this.showForPrint('.department-counters');
        this.showForPrint('.location-counters');
        this.showForPrint('.location-areas');
        this.showForPrint('.project-info-header');
    }
    
    afterPrint() {
        console.log('Cleaning up after print');
        
        // Remove print-specific body classes
        document.body.classList.remove('print-table-view', 'print-calendar-view');
        
        // Remove page break classes
        document.querySelectorAll('.print-page-break, .print-first-page-content').forEach(el => {
            el.classList.remove('print-page-break', 'print-first-page-content');
        });
        
        // Restore original view visibility
        this.restoreViewVisibility();
        
        // Remove print-specific visibility overrides
        document.querySelectorAll('[data-print-hidden]').forEach(el => {
            el.style.display = el.getAttribute('data-original-display') || '';
            el.removeAttribute('data-print-hidden');
            el.removeAttribute('data-original-display');
        });
        
        document.querySelectorAll('[data-print-shown]').forEach(el => {
            el.style.display = el.getAttribute('data-original-display') || '';
            el.removeAttribute('data-print-shown');
            el.removeAttribute('data-original-display');
        });
    }
    
    hideForPrint(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            if (!el.hasAttribute('data-print-hidden')) {
                el.setAttribute('data-original-display', el.style.display || '');
                el.setAttribute('data-print-hidden', 'true');
                el.style.display = 'none';
            }
        });
    }

    showForPrint(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            if (!el.hasAttribute('data-print-shown')) {
                el.setAttribute('data-original-display', el.style.display || '');
                el.setAttribute('data-print-shown', 'true');
                el.style.display = 'block';
            }
        });
    }

    restoreViewVisibility() {
        const currentView = this.getCurrentView();
        
        // Restore proper view visibility
        const calendarView = document.querySelector('.calendar-view');
        const tableView = document.querySelector('.calendar-table-wrapper');
        
        if (currentView === 'calendar') {
            if (tableView) tableView.style.display = 'none';
            if (calendarView) {
                calendarView.style.display = 'block';
                calendarView.classList.add('active');
            }
        } else {
            if (tableView) tableView.style.display = 'block';
            if (calendarView) {
                calendarView.style.display = 'none';
                calendarView.classList.remove('active');
            }
        }
    }
}

// Initialize print manager when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on a calendar page
    if (document.querySelector('.calendar-container') || document.querySelector('.admin-calendar')) {
        window.printManager = new PrintManager();
        console.log('Print manager initialized');
    }
});

// Make PrintManager available globally
window.PrintManager = PrintManager;
