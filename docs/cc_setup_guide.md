# Setting Up the STRIPS Theming Project for Claude Code

## Recommended File Structure

Create these files in your project root directory:

```
film-scheduler-v5/
├── THEMING_IMPLEMENTATION_GUIDE.md    # Main implementation guide
├── IMPLEMENTATION_PROGRESS.md         # Progress tracking & checklist
├── DESIGN_SYSTEM.md                   # Component library reference
├── CC_INSTRUCTIONS.md                 # Initial instructions for Claude Code
└── [existing project files...]
```

## File Contents & Purpose

### 1. `THEMING_IMPLEMENTATION_GUIDE.md`
**Purpose**: Complete implementation guide (the one I just created)
**CC Usage**: Reference document - CC reads but doesn't modify
**Your Action**: Save the full implementation guide here

### 2. `IMPLEMENTATION_PROGRESS.md` ⭐ *Key File*
**Purpose**: Living document that CC updates as work progresses
**CC Usage**: CC updates this after each task completion
**Content**: Detailed checklist with status tracking

### 3. `DESIGN_SYSTEM.md`
**Purpose**: Quick reference for components, colors, spacing
**CC Usage**: Reference for maintaining consistency
**Content**: Design tokens, component specs, examples

### 4. `CC_INSTRUCTIONS.md`
**Purpose**: Initial setup instructions for Claude Code
**CC Usage**: First file CC reads to understand the project
**Content**: Context, objectives, and how to proceed

## Step-by-Step Setup

### Step 1: Create the Progress Tracking File
Create `IMPLEMENTATION_PROGRESS.md`:

```markdown
# STRIPS Theming Implementation Progress

## Current Status: 🔄 Planning Phase
**Last Updated**: [Date]
**Current Phase**: Phase 1 - Core Infrastructure

## Phase 1: Core Infrastructure ⏳
- [ ] Create `static/css/theme.css` with design system
- [ ] Update `templates/base.html` with new header/navigation  
- [ ] Implement welcome page (`/` route, template, styles, JS)
- [ ] Move existing index functionality to `/dashboard`
- [ ] Test routing and basic functionality

### Current Task
**Working On**: Setting up base infrastructure
**Next Steps**: [CC updates this]
**Blockers**: [CC notes any issues]

## Phase 2: Page Implementations ⏸️
[CC will expand this when Phase 1 is complete]

## Completed Tasks ✅
- [x] Created implementation plan
- [x] Set up project structure

## Notes & Decisions
[CC adds notes about implementation choices, problems solved, etc.]
```

### Step 2: Create Initial CC Instructions
Create `CC_INSTRUCTIONS.md`:

```markdown
# Instructions for Claude Code

## Project Overview
You're implementing a comprehensive theming system for STRIPS, a Flask-based film production scheduler. The goal is to transform it into a cohesive, professionally branded application.

## What You Have
1. **THEMING_IMPLEMENTATION_GUIDE.md** - Complete implementation guide (READ ONLY)
2. **IMPLEMENTATION_PROGRESS.md** - Progress tracker (UPDATE THIS)
3. **DESIGN_SYSTEM.md** - Component reference (REFERENCE)
4. **Existing Flask Application** - Fully functional app that needs styling

## Your Mission
1. **READ** the implementation guide thoroughly
2. **START** with Phase 1 tasks
3. **UPDATE** progress file after each completed task
4. **PRESERVE** all existing functionality
5. **ASK** before making major architectural changes

## Key Rules
- ✅ All existing features must continue working identically
- ✅ Implement changes incrementally (test each step)
- ✅ Update IMPLEMENTATION_PROGRESS.md after each task
- ✅ Follow the design system specifications exactly
- ✅ Ask before deviating from the plan

## How to Start
1. Examine the current project structure
2. Read the full implementation guide
3. Create a detailed plan for Phase 1
4. Start with the first task: creating `theme.css`
5. Update progress file as you go

## Success Criteria
- Welcome page works perfectly with 3-path navigation
- All existing pages have new theming applied
- No functionality is broken
- Mobile responsiveness maintained
- Professional, cohesive visual experience

Ready to begin! Start by examining the current project structure and creating your Phase 1 implementation plan.
```

### Step 3: Create Design System Reference
Create `DESIGN_SYSTEM.md`:

```markdown
# STRIPS Design System Reference

## Colors
```css
:root {
    --primary-blue: #4FC3F7;
    --primary-pink: #FF6B9D;
    --primary-yellow: #FFD54F;
    --primary-dark: #1E293B;
    --text-light: #F8FAFC;
    --text-gray: #64748B;
    --background-dark: #0F172A;
    --card-dark: #1E293B;
    --border-subtle: #334155;
}
```

## Typography Scale
- **Hero**: 4.5rem (welcome page)
- **Page Title**: 2.5rem 
- **Section Header**: 1.8rem
- **Card Title**: 1.4rem
- **Body**: 1rem
- **Small**: 0.9rem

## Component Templates
[Include button, card, form examples here]

## Spacing System
- Small: 0.5rem, 1rem
- Medium: 1.5rem, 2rem  
- Large: 3rem, 4rem

## Border Radius
- Cards: 16px
- Buttons: 12px
- Inputs: 8px
```

## Initial Claude Code Conversation

When you start with Claude Code, use this approach:

### Opening Message:
```
I have a Flask-based film production scheduler called STRIPS that I want to completely retheme with a professional design system. I've created implementation docs for you to follow.

Please:
1. Read CC_INSTRUCTIONS.md first
2. Examine the current project structure  
3. Read THEMING_IMPLEMENTATION_GUIDE.md
4. Create a detailed plan for Phase 1
5. Start implementing, updating IMPLEMENTATION_PROGRESS.md as you go

The goal is a beautiful, professional app with a welcome page and consistent theming throughout, while preserving all existing functionality.

Ready to begin?
```

### Follow-up Messages:
- **After each phase**: "Please update the progress file and show me what you've completed"
- **For reviews**: "Show me the current status and what you're working on next"
- **For issues**: "Check the progress file for any blockers and let's resolve them"

## Advantages of This Setup

### ✅ **For You:**
- Clear visibility of progress
- Easy to jump in/out of conversations with CC
- Structured approach reduces errors
- Can review work at each phase

### ✅ **For Claude Code:**
- Clear instructions and context
- Living progress document to maintain continuity
- Reference materials for consistency
- Defined success criteria

### ✅ **For the Project:**
- Systematic implementation
- Reduced risk of breaking existing functionality
- Maintainable documentation
- Easy to hand off or continue later

## Pro Tips

1. **Commit often**: Have CC commit after each major task
2. **Review phases**: Check work before moving to next phase
3. **Keep notes**: CC should document decisions in progress file
4. **Test incrementally**: Verify each change works before continuing
5. **Stay flexible**: Adjust the plan based on what CC discovers

This setup gives you maximum control while leveraging CC's capabilities effectively!
