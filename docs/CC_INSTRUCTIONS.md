# Instructions for Claude Code

## Project Overview
You're implementing a comprehensive theming system for **STRIPS**, a Flask-based film production scheduler. The goal is to transform it into a cohesive, professionally branded application while preserving all existing functionality.

## What You Have Available

### 📋 Documentation Files
1. **`THEMING_IMPLEMENTATION_GUIDE.md`** - Complete implementation guide (READ ONLY - reference document)
2. **`IMPLEMENTATION_PROGRESS.md`** - Progress tracker (UPDATE THIS after each task)
3. **`DESIGN_SYSTEM.md`** - Component reference and design tokens (REFERENCE)
4. **Existing Flask Application** - Fully functional app in current directory

### 🎯 Your Mission
Transform STRIPS from a functional but basic-looking app into a professional, branded film production management platform with:
- Beautiful animated welcome page with 3-path navigation (Viewer/Admin/Help)
- Consistent theming across all pages
- Enhanced user experience with modern UI patterns
- Mobile-responsive design
- All existing functionality preserved

## 🚨 Critical Rules (NEVER BREAK THESE)

### ✅ Functionality Preservation
- **ALL existing features must continue working identically**
- **ALL existing routes must work exactly as before**
- **ALL authentication flows must remain unchanged**
- **ALL admin features must be fully functional**

### ✅ Implementation Approach
- **Work incrementally** - test each change before moving on
- **Update `IMPLEMENTATION_PROGRESS.md`** after completing each task
- **Follow the design system specifications** in `DESIGN_SYSTEM.md` exactly
- **Ask before making major architectural changes**
- **Commit your work** frequently with descriptive messages

### ✅ Quality Standards
- **Mobile responsive** - all pages must work on mobile devices
- **Cross-browser compatible** - test in multiple browsers
- **Performance conscious** - don't degrade loading times
- **Accessible** - maintain keyboard navigation and screen reader compatibility

## 📚 How to Get Started

### Step 1: Understand the Current State
1. **Examine the existing project structure**
   - Look at the current Flask application
   - Understand the routing in `routes/main.py`
   - Review existing templates in `templates/`
   - Check current styling in `static/css/`

### Step 2: Read the Documentation
1. **Read `THEMING_IMPLEMENTATION_GUIDE.md` thoroughly**
   - Understand the phased approach
   - Note the file structure changes needed
   - Review the routing modifications required

2. **Study `DESIGN_SYSTEM.md`**
   - Understand the color palette
   - Note typography scales
   - Review component patterns

### Step 3: Create Implementation Plan
1. **Create a detailed plan for Phase 1** based on the guide
2. **Update `IMPLEMENTATION_PROGRESS.md`** with your plan
3. **Start with the first task**: Creating the base theme system

### Step 4: Begin Implementation
**Start with Phase 1 tasks in this exact order:**
1. Create `static/css/theme.css` with the design system
2. Update `templates/base.html` with new header/navigation
3. Implement the welcome page (route, template, styles, JS)
4. Move existing index functionality to `/dashboard`
5. Test that everything works

## 📋 Task Management

### Before Starting Each Task
- [ ] Read the task requirements in the implementation guide
- [ ] Understand what files need to be created/modified
- [ ] Plan your approach

### While Working on Each Task
- [ ] Follow the design system specifications exactly
- [ ] Test functionality as you go
- [ ] Make incremental commits

### After Completing Each Task
- [ ] Test that the feature works correctly
- [ ] Test that existing functionality still works
- [ ] Update `IMPLEMENTATION_PROGRESS.md` with:
  - What you completed
  - What files you created/modified
  - Any issues encountered and how you solved them
  - What's next

## 🎨 Design Implementation Notes

### Welcome Page Requirements
The welcome page should have:
- **3 main access paths**:
  1. **Viewer Access** → `/login` (for crew members with project codes)
  2. **Admin Access** → `/admin/login` (for full management access)
  3. **Help & About** → `/help` (information about the app)
- **Animated background elements** (subtle, professional)
- **STRIPS branding** with the colorful logo design
- **Mobile responsive** design

### Routing Changes Required
```python
# NEW ROUTING STRUCTURE
@main_bp.route('/')
def welcome():
    """Welcome page - no authentication required"""
    return render_template('welcome.html')

@main_bp.route('/dashboard')  # MOVED FROM /
@viewer_required
def dashboard():
    """Project dashboard - renamed from index"""
    projects = get_projects()
    return render_template('dashboard.html', projects=projects)  # RENAMED FROM index.html
```

### File Organization
- **Keep existing files** when possible, enhance them
- **Create new files** for new functionality
- **Follow naming conventions** established in the project
- **Organize CSS** into logical files (theme.css, welcome.css, components.css)

## 🔧 Technical Requirements

### Browser Support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance Targets
- No degradation in page load times
- Smooth animations (60fps)
- Responsive interactions

### File Structure to Create
```
static/
├── css/
│   ├── theme.css           # Main design system (CREATE)
│   ├── welcome.css         # Welcome page styles (CREATE)
│   ├── components.css      # Reusable components (CREATE)
│   └── [existing files]    # Enhanced existing styles
├── js/
│   ├── theme.js           # Theme utilities (CREATE)
│   ├── welcome.js         # Welcome interactions (CREATE)
│   └── [existing files]   # Updated with new features
templates/
├── welcome.html           # New welcome page (CREATE)
├── dashboard.html         # Renamed from index.html (RENAME)
├── help.html              # New help page (CREATE)
├── base.html              # Updated header/nav (UPDATE)
└── [existing files]       # Enhanced with new styling
```

## 📞 Communication Protocol

### When to Ask Questions
- **Before making major architectural changes**
- **If you encounter breaking issues**
- **If the requirements are unclear**
- **If you need to deviate from the plan**

### Status Updates
- **Update progress file** after each completed task
- **Include what you're working on next**
- **Note any blockers or issues**

### Documentation
- **Document your decisions** in the progress file
- **Explain any deviations** from the original plan
- **Note any improvements** you discover

## 🏁 Success Criteria

### Visual Goals
- [ ] Welcome page is beautiful and professional
- [ ] All pages follow consistent design system
- [ ] Mobile responsive across all devices
- [ ] Smooth animations and transitions

### Functional Goals
- [ ] All existing features work identically
- [ ] New routing structure works correctly
- [ ] Authentication flows preserved
- [ ] Admin functionality intact

### Technical Goals
- [ ] Performance maintained or improved
- [ ] Code is clean and maintainable
- [ ] Proper error handling
- [ ] Cross-browser compatibility

## 🚀 Ready to Begin!

Your next steps:
1. **Examine the current project structure**
2. **Read the full implementation guide**
3. **Create your Phase 1 implementation plan**
4. **Update the progress file with your plan**
5. **Start with creating `static/css/theme.css`**

Remember: **Incremental progress, frequent testing, and clear documentation** are key to success!

Good luck! 🎬✨