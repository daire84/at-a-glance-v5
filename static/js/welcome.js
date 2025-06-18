// STRIPS Welcome Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initWelcomePage();
});

function initWelcomePage() {
    // Initialize animations
    initAnimations();
    
    // Initialize card interactions
    initCardInteractions();
    
    // Initialize keyboard navigation
    initKeyboardNavigation();
    
    // Initialize loading states
    initLoadingStates();
}

// Animation handling
function initAnimations() {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (prefersReducedMotion) {
        // Remove animations for users who prefer reduced motion
        const animatedElements = document.querySelectorAll('.hero-logo, .nav-card, .welcome-stats');
        animatedElements.forEach(el => {
            el.style.animation = 'none';
        });
        return;
    }
    
    // Stagger card animations
    const cards = document.querySelectorAll('.nav-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${0.6 + (index * 0.2)}s`;
    });
    
    // Add scroll-triggered animations for elements below the fold
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    const statsSection = document.querySelector('.welcome-stats');
    if (statsSection) {
        observer.observe(statsSection);
    }
}

// Card interaction enhancements
function initCardInteractions() {
    const cards = document.querySelectorAll('.nav-card');
    
    cards.forEach(card => {
        // Add hover sound effect (optional - could be enabled via setting)
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
        
        // Add click effect
        card.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(-4px) scale(0.98)';
        });
        
        card.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        // Add focus handling for accessibility
        const button = card.querySelector('.nav-card-button');
        if (button) {
            button.addEventListener('focus', function() {
                card.classList.add('focused');
            });
            
            button.addEventListener('blur', function() {
                card.classList.remove('focused');
            });
        }
    });
}

// Keyboard navigation support
function initKeyboardNavigation() {
    const buttons = document.querySelectorAll('.nav-card-button');
    
    buttons.forEach((button, index) => {
        button.addEventListener('keydown', function(e) {
            let targetIndex;
            
            switch(e.key) {
                case 'ArrowRight':
                case 'ArrowDown':
                    e.preventDefault();
                    targetIndex = (index + 1) % buttons.length;
                    buttons[targetIndex].focus();
                    break;
                    
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    targetIndex = index === 0 ? buttons.length - 1 : index - 1;
                    buttons[targetIndex].focus();
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    buttons[0].focus();
                    break;
                    
                case 'End':
                    e.preventDefault();
                    buttons[buttons.length - 1].focus();
                    break;
            }
        });
    });
}

// Loading states for navigation
function initLoadingStates() {
    const buttons = document.querySelectorAll('.nav-card-button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Don't show loading for help page (local navigation)
            if (this.getAttribute('href') === '/help') {
                return;
            }
            
            // Add loading state
            const originalText = this.textContent;
            this.classList.add('loading');
            this.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-dasharray="60 60" stroke-dashoffset="60">
                        <animate attributeName="stroke-dashoffset" dur="2s" values="60;0;60" repeatCount="indefinite"/>
                    </circle>
                </svg>
                Loading...
            `;
            
            // Remove loading state after a delay if navigation doesn't happen
            setTimeout(() => {
                if (this.classList.contains('loading')) {
                    this.classList.remove('loading');
                    this.textContent = originalText;
                }
            }, 3000);
        });
    });
}

// Utility functions
function addRippleEffect(element, event) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add CSS for ripple effect
const rippleCSS = `
    .nav-card-button {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: rippleEffect 600ms linear;
        pointer-events: none;
    }
    
    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .nav-card.focused {
        outline: 2px solid var(--primary-blue);
        outline-offset: 4px;
    }
    
    .animate-in {
        animation: slideUp 0.6s ease forwards;
    }
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Add ripple effects to buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav-card-button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            addRippleEffect(this, e);
        });
    });
});

// Preload critical resources for faster navigation
function preloadResources() {
    const preloadLinks = [
        '/login',
        '/admin/login',
        '/help'
    ];
    
    preloadLinks.forEach(href => {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = href;
        document.head.appendChild(link);
    });
}

// Initialize preloading after page load
window.addEventListener('load', preloadResources);

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initWelcomePage,
        initAnimations,
        initCardInteractions,
        initKeyboardNavigation,
        initLoadingStates
    };
}