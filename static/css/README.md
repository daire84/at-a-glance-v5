# Film Production Scheduler - CSS Style Guide

## 📁 CSS Folder Structure

This folder contains all the stylesheets for the Film Production Scheduler application. The CSS is organized in a modular approach for maintainability and easy customization.

```
static/css/
├── style.css                           # 🎨 Main stylesheet with global styles and theme variables
├── admin/                              # 📁 Admin interface specific styles
│   ├── dashboard.css                   # Admin dashboard project cards and stats
│   ├── dates.css                       # Special dates management interface
│   ├── departments.css                 # Department management interface
│   └── locations.css                   # Location management interface
├── components/                         # 📁 Reusable component styles
│   ├── calendar-core.css               # Core calendar structure and layout
│   ├── calendar-filters.css            # Filter panels and search functionality
│   ├── calendar-interactions.css       # Hover effects and interactive elements
│   ├── calendar-layout.css             # Calendar table layout and responsive design
│   ├── calendar-mobile.css             # Mobile-specific calendar optimizations
│   ├── calendar-print.css              # Print-specific styles for calendar
│   ├── calendar-table.css              # Calendar table cells and content
│   └── modals.css                      # Modal dialogs and overlays
├── calendar-view.css                   # Alternative calendar grid view
├── day-editor-enhanced.css             # Enhanced day editor interface
├── forms.css                           # Form controls and input styling
├── help.css                            # Help documentation styling
└── version-manager.css                 # Version control interface
```

## 🎨 Core Customization Files

### 1. **style.css** - Global Theme System
**Primary file for visual customization**

Contains CSS variables that control the entire application's appearance:

```css
:root {
  /* Base colors - Change these to customize the overall look */
  --primary-color: #5b5b5c;        /* Main UI color */
  --accent-color: #0b5fb3;         /* Buttons and highlights */
  --background-color: #1e1e20;     /* Main background */
  --text-color: #e0e2e7;           /* Primary text */
  
  /* Calendar row colors - Customize day type appearances */
  --weekend-color: #7f7f83;        /* Weekend day rows */
  --prep-color: #477551;           /* Prep day rows */
  --shoot-color: #2d4561;          /* Shoot day rows */
  --hiatus-color: #5a3a3a;         /* Hiatus period rows */
  --holiday-color: #5a4a2f;        /* Holiday rows */
  --working-weekend-color: #355a35; /* Working weekend rows */
}
```

**Key customizable sections:**
- **Theme Variables** (lines 1-50): Change colors, fonts, spacing
- **Light Theme Override** (around line 60): Customize light mode appearance
- **Typography** (around line 150): Font sizes, weights, and families
- **Button Styles** (around line 400): Button appearance and hover effects

### 2. **forms.css** - Form Controls
**Customize input fields, buttons, and form layouts**

Key areas for customization:
- Form container appearance
- Input field styling
- Button variations (primary, secondary, danger)
- Department tag selectors
- Responsive form layouts

### 3. **components/calendar-table.css** - Calendar Appearance
**Main calendar table styling**

Customize:
- Table cell appearance
- Row hover effects
- Column widths and spacing
- Department tag colors
- Location area color coding

## 🎯 Common Customization Tasks

### 🎨 Changing the Color Scheme

**To change the overall color theme:**

1. **Edit `style.css`** - Find the `:root` section (top of file)
2. **Modify theme variables:**
   ```css
   :root {
     --primary-color: #your-new-color;     /* Main theme color */
     --accent-color: #your-accent-color;   /* Buttons/highlights */
     --background-color: #your-bg-color;   /* Main background */
   }
   ```

3. **For light theme:** Edit the `body.light-theme` section

### 📱 Mobile Appearance

**Files to modify for mobile customization:**
- `components/calendar-mobile.css` - Mobile-specific calendar controls
- `style.css` - Global responsive breakpoints (search for `@media`)
- `components/calendar-layout.css` - Mobile table layout

### 🖨️ Print Styling

**To customize printed calendars:**
- Edit `components/calendar-print.css`
- Modify print-specific styles in `calendar-view.css` (search for `@media print`)

### 🏷️ Department and Location Colors

**Department tag colors:**
1. **Via Admin Interface:** Use `/admin/departments` to set colors visually
2. **Direct CSS:** Modify department tag styles in `components/calendar-table.css`

**Location area colors:**
1. **Via Admin Interface:** Use `/admin/locations` to assign area colors
2. **CSS Override:** Use location-specific selectors in custom CSS

## 📋 Admin Interface Customization

### Admin Dashboard (`admin/dashboard.css`)
- Project card appearance
- Statistics boxes
- Admin navigation styling

### Special Dates Manager (`admin/dates.css`)
- Date picker styling
- Holiday/hiatus period cards
- Form layouts for date management

### Department Manager (`admin/departments.css`)
- Department card grid
- Color preview styling
- Tag appearance controls

### Location Manager (`admin/locations.css`)
- Location list/table styling
- Area assignment interface
- Color swatch displays

## 🎭 Theme System

The application supports both **dark** (default) and **light** themes:

### Dark Theme (Default)
- Defined in the `:root` section of `style.css`
- Dark backgrounds with light text
- Suitable for low-light environments

### Light Theme
- Defined in `body.light-theme` section of `style.css`
- Light backgrounds with dark text
- Better for printing and high-light environments

### Creating Custom Themes

**To add a new theme:**

1. **Add theme class to `style.css`:**
   ```css
   body.your-theme-name {
     --primary-color: #new-color;
     --background-color: #new-bg;
     /* ... other overrides */
   }
   ```

2. **Update theme toggle** in `static/js/theme-toggle.js`

## 🔧 Advanced Customization

### Custom CSS Classes

**Add custom styles by creating:**
```css
/* Custom overrides - add to end of style.css */
.your-custom-class {
  /* Your custom styles */
}

/* Target specific calendar elements */
.calendar-row.your-custom-type {
  background-color: #your-color;
}
```

### Component-Specific Styling

**Calendar components** - Edit files in `components/` folder:
- `calendar-core.css` - Base calendar structure
- `calendar-table.css` - Table cells and content
- `calendar-filters.css` - Filter panels and search

**Form components** - Edit `forms.css`:
- Input field appearance
- Button styling
- Form layout and spacing

### Print Customization

**For custom print layouts:**

1. **Edit `components/calendar-print.css`**
2. **Add print-specific rules:**
   ```css
   @media print {
     .your-element {
       /* Print-only styles */
     }
   }
   ```

## 📐 Responsive Design

**Breakpoints used throughout the application:**
- **Mobile:** `max-width: 768px`
- **Tablet:** `768px - 1024px`
- **Desktop:** `min-width: 1024px`

**Key responsive files:**
- `components/calendar-mobile.css` - Mobile calendar optimizations
- `components/calendar-layout.css` - Responsive table layout
- `style.css` - Global responsive utilities

## 🎨 Quick Customization Examples

### Example 1: Change Primary Color
```css
/* In style.css - :root section */
:root {
  --primary-color: #2c3e50;        /* Change to dark blue-gray */
  --primary-light: #34495e;        /* Lighter variant */
  --primary-dark: #1a252f;         /* Darker variant */
}
```

### Example 2: Customize Shoot Day Appearance
```css
/* In style.css or components/calendar-table.css */
.calendar-row.shoot {
  background-color: #your-color !important;
  border-left: 4px solid #accent-color;
}
```

### Example 3: Custom Department Tag
```css
/* In components/calendar-table.css */
.department-tag[data-dept="YOUR_CODE"] {
  background-color: #your-color;
  color: #text-color;
}
```

## 🚀 Best Practices

### ✅ Recommended Approach
- **Start with theme variables** in `style.css`
- **Use CSS custom properties** for consistency
- **Test both light and dark themes** after changes
- **Check mobile responsiveness** after modifications
- **Verify print layouts** if print functionality is important

### ❌ Avoid
- **Modifying core structural CSS** unless necessary
- **Using `!important` excessively**
- **Breaking responsive design** with fixed widths
- **Overriding print styles** without testing

## 🔍 Troubleshooting

### Common Issues

**Changes not appearing:**
1. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
2. Check browser developer tools for CSS errors
3. Verify file paths are correct

**Mobile layout broken:**
1. Check responsive CSS in `components/calendar-mobile.css`
2. Verify viewport meta tag in base template
3. Test on actual mobile devices

**Print styles not working:**
1. Use browser print preview to test
2. Check `@media print` rules in relevant files
3. Verify `print-color-adjust: exact` for colors

## 📚 Additional Resources

**CSS Variables Reference:** [MDN CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
**Flexbox Guide:** [CSS-Tricks Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
**Grid Layout:** [MDN CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)

---

**Happy Customizing! 🎨**

For questions about specific styling needs or issues, refer to the main project documentation or create an issue in the project repository.