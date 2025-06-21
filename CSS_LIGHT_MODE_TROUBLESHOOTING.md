# STRIPS Light/Dark Mode CSS Troubleshooting Guide

## 🎯 **Purpose**
This document serves as a comprehensive guide for troubleshooting light/dark mode CSS issues in the STRIPS application. It documents the complete solution approach used to achieve perfect theming compatibility.

**Last Updated**: 2025-06-21  
**Status**: Complete reference guide based on successful implementation

---

## 🔍 **Common Light Mode Issues & Solutions**

### **Issue Type 1: Dark Containers in Light Mode**
**Symptoms**: Container boxes stay dark navy/black when switching to light mode
**Root Cause**: Missing `body.light-theme` CSS overrides for container backgrounds
**Solution Pattern**:
```css
body.light-theme .container-class {
    background-color: var(--background-secondary);
    border-color: var(--border-color);
}
```

### **Issue Type 2: Invisible White Text**
**Symptoms**: Text appears white on white backgrounds in light mode, becoming invisible
**Root Cause**: Text color not overridden for light mode theme
**Solution Pattern**:
```css
body.light-theme .text-element {
    color: var(--text-primary);
}

body.light-theme .secondary-text {
    color: var(--text-secondary);
}
```

### **Issue Type 3: Dark Search/Input Elements**
**Symptoms**: Input fields, search boxes remain dark in light mode
**Root Cause**: Form elements need specific light mode styling
**Solution Pattern**:
```css
body.light-theme input[type="text"],
body.light-theme input[type="search"],
body.light-theme textarea {
    background-color: var(--input-bg);
    border-color: var(--input-border);
    color: var(--input-text);
}
```

---

## 🛠️ **Systematic Debugging Approach**

### **Step 1: Identify the HTML Structure**
Use browser dev tools or Task tool to find exact HTML elements and class names:
```html
<!-- Example: Find the actual HTML structure -->
<div class="problematic-container">
    <h4 class="problematic-header">Invisible Text</h4>
    <div class="problematic-content">
        <span class="problematic-text">Can't see this</span>
    </div>
</div>
```

### **Step 2: Locate Existing CSS**
Search for existing CSS selectors to understand current styling:
```bash
# Search for existing selectors
grep -r "problematic-container" static/css/
```

### **Step 3: Add Light Mode Overrides**
Add specific light mode overrides using correct CSS variables:
```css
/* Fix the problematic elements */
body.light-theme .problematic-container {
    background-color: var(--background-secondary);
    border-color: var(--border-color);
}

body.light-theme .problematic-header,
body.light-theme .problematic-text {
    color: var(--text-primary);
}
```

---

## 📁 **CSS File Organization**

### **Primary CSS Files for Light Mode Overrides**

1. **`/static/css/components/calendar-filters.css`**
   - Filter panels, search components
   - Stats sections, location filtering
   - Search inputs and results

2. **`/static/css/version-manager.css`**
   - Version management containers
   - Version items and notifications

3. **`/static/css/help.css`**
   - Help page layout and components
   - Navigation cards and sections

4. **`/static/css/welcome.css`**
   - Welcome page navigation cards
   - Access level containers

5. **`/static/css/forms.css`**
   - Form input elements
   - Text field visibility

6. **`/static/css/components/calendar-*.css`**
   - Calendar-specific components
   - Counters, tables, core elements

---

## 🎨 **CSS Variable Reference**

### **Background Variables**
```css
--background-primary: #ffffff;      /* Main light backgrounds */
--background-secondary: #f8f9fa;    /* Secondary light containers */
--background-tertiary: #e9ecef;     /* Tertiary light elements */
--background-hover: #f0f0f0;        /* Hover state backgrounds */
```

### **Text Variables**
```css
--text-primary: #333333;            /* Main text in light mode */
--text-secondary: #666666;          /* Secondary text */
--text-heading: #2c3e50;            /* Headings in light mode */
```

### **Form Variables**
```css
--input-bg: #ffffff;                /* Input field backgrounds */
--input-border: #dee2e6;            /* Input field borders */
--input-text: #495057;              /* Input field text */
```

### **Border Variables**
```css
--border-color: #dee2e6;            /* Standard borders in light mode */
```

---

## 🔧 **Common Selector Patterns**

### **Pattern 1: Component Container Override**
```css
body.light-theme .component-name {
    background-color: var(--background-secondary);
    border-color: var(--border-color);
}
```

### **Pattern 2: Text Content Override**
```css
body.light-theme .component-name h1,
body.light-theme .component-name h2,
body.light-theme .component-name h3,
body.light-theme .component-name h4,
body.light-theme .component-name h5,
body.light-theme .component-name p {
    color: var(--text-primary);
}
```

### **Pattern 3: Form Elements Override**
```css
body.light-theme .component-name input[type="text"],
body.light-theme .component-name input[type="search"],
body.light-theme .component-name textarea,
body.light-theme .component-name select {
    background-color: var(--input-bg);
    border-color: var(--input-border);
    color: var(--input-text);
}
```

### **Pattern 4: Nested Element Override**
```css
body.light-theme .parent-component .child-element {
    color: var(--text-primary);
}

body.light-theme .parent-component .child-element strong {
    color: var(--primary-blue);
}
```

---

## 🕵️ **Investigation Techniques**

### **Using Task Tool for HTML Structure Discovery**
```markdown
Task Prompt Template:
"I need to find the exact HTML structure for [component name] that's having light mode issues. Please:
1. Search through template files for '[text or component identifier]'
2. Find the HTML structure and CSS class names
3. Identify exact selectors needed for light mode overrides"
```

### **Using Grep for CSS Selector Discovery**
```bash
# Find existing CSS for component
grep -r "component-name" static/css/

# Find CSS variables being used
grep -r "var(--" static/css/filename.css

# Find existing light mode overrides
grep -r "body.light-theme" static/css/
```

### **Browser Dev Tools Inspection**
1. Right-click on problematic element → Inspect
2. Look for actual class names and CSS selectors
3. Check computed styles to see which CSS is being applied
4. Test CSS overrides directly in browser console

---

## ✅ **Verification Checklist**

### **After Adding Light Mode Overrides**
- [ ] Switch to light mode and verify all text is visible
- [ ] Check all container backgrounds are light
- [ ] Verify form inputs have proper light styling
- [ ] Test hover states work in both modes
- [ ] Ensure borders and shadows are visible
- [ ] Confirm color contrast meets accessibility standards

### **Cross-Component Testing**
- [ ] Welcome page navigation cards
- [ ] Calendar filter panels and search
- [ ] Admin version management
- [ ] Help page layout and content
- [ ] Form inputs across all pages
- [ ] Location filtering components
- [ ] Statistics and counter displays

---

## 🚨 **Emergency Fix Template**

If you encounter a new light mode issue, use this template:

```css
/* Emergency Light Mode Fix for [Component Name] */
/* Issue: [Description of problem] */
/* Date: [Current date] */

body.light-theme .your-component {
    background-color: var(--background-secondary);
    border-color: var(--border-color);
}

body.light-theme .your-component h1,
body.light-theme .your-component h2,
body.light-theme .your-component h3,
body.light-theme .your-component h4,
body.light-theme .your-component p,
body.light-theme .your-component span {
    color: var(--text-primary);
}

body.light-theme .your-component .secondary-text {
    color: var(--text-secondary);
}

/* Add to appropriate CSS file in /static/css/ */
```

---

## 📚 **Reference Files**

### **Successfully Fixed Components**
All examples and patterns in this guide are based on successfully resolved issues in:
- Interactive Location Filtering containers
- Version management systems
- Filter and search components
- Help page layouts
- Welcome page navigation
- Calendar components and counters
- Form input elements
- Statistics displays

### **Pattern Source Files**
Reference these files for working examples:
- `/static/css/components/calendar-filters.css` (lines 379-491)
- `/static/css/version-manager.css` (lines 216-268)
- `/static/css/help.css` (lines 598-709)
- `/static/css/welcome.css` (light mode overrides section)

---

**This guide represents the complete solution methodology that achieved 100% light/dark mode compatibility across the STRIPS application.**