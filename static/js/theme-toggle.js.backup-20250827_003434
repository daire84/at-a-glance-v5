/**
 * Theme toggle functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Find the theme toggle element
    const themeToggle = document.getElementById('theme-toggle');
    
    // Set initial state based on localStorage or default to dark theme
    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply the theme
    applyTheme(currentTheme);
    
    // Add toggle functionality if element exists
    if (themeToggle) {
        // Update toggle to match current theme
        updateToggleUI(currentTheme);
        
        // Add event listener
        themeToggle.addEventListener('click', function() {
            // Get current theme
            const currentTheme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
            
            // Toggle to other theme
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            // Apply the new theme
            applyTheme(newTheme);
            
            // Update toggle UI
            updateToggleUI(newTheme);
            
            // Save preference
            localStorage.setItem('theme', newTheme);
        });
    }
});

/**
 * Apply the specified theme to the document by toggling a class on the body.
 * CSS will handle the application of variables based on this class.
 * @param {string} theme - 'light' or 'dark'
 */
function applyTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light-theme');
        // All document.documentElement.style.setProperty(...) lines removed for light theme
    } else { // Dark Theme
        document.body.classList.remove('light-theme');
        // All document.documentElement.style.setProperty(...) lines removed for dark theme
        // Also, the explicit .removeProperty() calls from the previous step are no longer needed
        // as we are not setting them in JS for light mode anymore either.
    }
    
    // Re-apply location area colors after theme change
    // This might still be needed if locationAreaColors are dynamically generated
    // and rely on CSS variables that might change with the theme class.
    // If applyLocationAreaColors directly sets styles or depends on
    // JS-calculated values based on theme, it should remain.
    // If it purely relies on CSS variables now defined in style.css,
    // this explicit call might become less critical, but often harmless.
    setTimeout(function() {
        if (typeof window.applyLocationAreaColors === 'function') {
            const areas = window.getLocationAreas ? window.getLocationAreas() : {};
            window.applyLocationAreaColors(areas);
        } else if (typeof applyLocationAreaColors === 'function') {
            const areas = typeof getLocationAreas === 'function' ? getLocationAreas() : {};
            applyLocationAreaColors(areas);
        }
    }, 10);
}

/**
 * Update the toggle UI to reflect the current theme
 * @param {string} theme - 'light' or 'dark'
 */
function updateToggleUI(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    const themeIcon = themeToggle.querySelector('.theme-icon');
    const themeText = themeToggle.querySelector('.theme-text'); // Assuming you might have text
    
    if (theme === 'light') {
        // Update to show dark mode option
        if (themeIcon) {
            themeIcon.innerHTML = '🌙'; // Moon icon
        }
        if (themeText) {
            themeText.textContent = 'Dark Mode';
        }
    } else {
        // Update to show light mode option
        if (themeIcon) {
            themeIcon.innerHTML = '☀️'; // Sun icon
        }
        if (themeText) {
            themeText.textContent = 'Light Mode';
        }
    }
}