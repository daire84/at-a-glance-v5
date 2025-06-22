# STRIPS Design System Reference

## Brand Colors

### Primary Palette
```css
:root {
    --primary-blue: #4FC3F7;
    --primary-pink: #FF6B9D;
    --primary-yellow: #FFD54F;
    --primary-dark: #1E293B;
}
```

### Neutral Palette
```css
:root {
    --text-light: #F8FAFC;
    --text-gray: #64748B;
    --background-dark: #0F172A;
    --card-dark: #1E293B;
    --border-subtle: #334155;
}
```

### Status Colors
```css
:root {
    --success-green: #10B981;
    --warning-orange: #F59E0B;
    --error-red: #EF4444;
}
```

## Typography Scale

### Font Family
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Size Scale
- **Hero Text**: `4.5rem` - Welcome page title
- **Page Title**: `2.5rem` - Main page headings  
- **Section Header**: `1.8rem` - Section titles
- **Card Title**: `1.4rem` - Card headings
- **Body Large**: `1.25rem` - Important body text
- **Body**: `1rem` - Standard body text
- **Body Small**: `0.9rem` - Secondary text
- **Label**: `0.8rem` - Form labels, captions

### Font Weights
- **Light**: `300` - Subtitles, secondary text
- **Regular**: `400` - Body text
- **Medium**: `500` - Emphasized text
- **Semi-Bold**: `600` - Card titles, important text
- **Bold**: `700` - Page titles
- **Extra Bold**: `800` - Hero text

## Spacing System

### Base Unit: `1rem` (16px)

### Scale
```css
--space-xs: 0.5rem;   /* 8px */
--space-sm: 1rem;     /* 16px */
--space-md: 1.5rem;   /* 24px */
--space-lg: 2rem;     /* 32px */
--space-xl: 3rem;     /* 48px */
--space-2xl: 4rem;    /* 64px */
```

### Usage Guidelines
- **Component padding**: `1rem` - `2rem`
- **Section spacing**: `3rem` - `4rem`
- **Element gaps**: `0.5rem` - `1rem`
- **Container padding**: `1rem` mobile, `2rem` desktop

## Border Radius

```css
--radius-sm: 8px;     /* Form inputs, small buttons */
--radius-md: 12px;    /* Buttons, pills */
--radius-lg: 16px;    /* Cards, modals */
--radius-xl: 20px;    /* Special elements */
--radius-full: 50px;  /* Pills, avatar */
```

## Shadows

### Elevation System
```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

/* Branded shadows (with blue tint) */
--shadow-blue-sm: 0 4px 15px rgba(79, 195, 247, 0.2);
--shadow-blue-md: 0 8px 25px rgba(79, 195, 247, 0.3);
--shadow-blue-lg: 0 15px 35px rgba(79, 195, 247, 0.4);
```

## Component Templates

### Buttons

#### Primary Button
```css
.btn-primary {
    background: linear-gradient(135deg, var(--primary-blue), var(--primary-pink));
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-md);
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-blue-sm);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-blue-md);
}
```

#### Secondary Button
```css
.btn-secondary {
    background: transparent;
    color: var(--text-gray);
    border: 1px solid var(--border-subtle);
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-md);
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    border-color: var(--primary-blue);
    color: var(--primary-blue);
}
```

### Cards

#### Standard Card
```css
.card {
    background: var(--card-dark);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 2rem;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    border-color: var(--primary-blue);
    box-shadow: var(--shadow-blue-md);
}
```

#### Project Card (Enhanced)
```css
.project-card {
    background: var(--card-dark);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.project-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(135deg, var(--primary-blue), var(--primary-pink), var(--primary-yellow));
}
```

### Form Elements

#### Input Field
```css
.form-input {
    background: var(--card-dark);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    color: var(--text-light);
    width: 100%;
    transition: border-color 0.3s ease;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-blue);
    box-shadow: 0 0 0 3px rgba(79, 195, 247, 0.1);
}
```

#### Label
```css
.form-label {
    display: block;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-gray);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}
```

## Layout Components

### Container
```css
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

@media (min-width: 768px) {
    .container {
        padding: 0 2rem;
    }
}
```

### Section Header
```css
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-subtle);
}

.section-title {
    font-size: 1.8rem;
    color: var(--text-light);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
```

### Grid Layouts
```css
.grid-auto {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
```

## Gradients

### Primary Gradients
```css
--gradient-primary: linear-gradient(135deg, var(--primary-blue), var(--primary-pink));
--gradient-accent: linear-gradient(135deg, var(--primary-blue), var(--primary-pink), var(--primary-yellow));
--gradient-background: linear-gradient(135deg, var(--background-dark) 0%, var(--primary-dark) 100%);
```

## Animation Guidelines

### Standard Transitions
```css
--transition-fast: 0.15s ease;
--transition-normal: 0.3s ease;
--transition-slow: 0.5s ease;
```

### Common Animations
```css
/* Hover lift effect */
.hover-lift:hover {
    transform: translateY(-4px);
}

/* Fade in animation */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Slide up animation */
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Responsive Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 640px;   /* Small tablets */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Small desktops */
--breakpoint-xl: 1280px;  /* Large desktops */
```

### Usage
```css
/* Mobile styles first */
.element {
    font-size: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
    .element {
        font-size: 1.2rem;
    }
}
```

## Usage Guidelines

### Do's ✅
- Use consistent spacing from the scale
- Apply hover effects to interactive elements
- Maintain color contrast ratios
- Use semantic color meanings (blue for primary actions, red for errors)
- Follow the typography hierarchy

### Don'ts ❌
- Don't use arbitrary spacing values
- Don't mix different border radius values on related elements
- Don't use colors outside the defined palette
- Don't skip typography scale levels
- Don't forget hover/focus states