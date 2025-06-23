# 🤖 CLAUDE CODE: START HERE

## 📢 INITIAL INSTRUCTIONS FOR CLAUDE CODE

**Human Message:** "I have loaded multiple .md files into this project. Please read `START_HERE_CLAUDE_CODE.md` first to understand the full scope and implementation order."

## 🎯 PROJECT MISSION

Transform the existing Film Production Scheduler from a single-admin system into a **production-ready tool** that serves:
1. **Admin Users** (1st ADs, Producers) - Full editing with user accounts
2. **Crew Members** - Public view-only access via codes/links (no accounts)

## 📚 DOCUMENT READING ORDER

**CRITICAL:** Read these documents in this exact order:

### 1. FIRST - Understanding the Project
- **`START_HERE_CLAUDE_CODE.md`** ← You are here
- **`CLAUDE_CODE_IMPLEMENTATION_OVERVIEW.md`** ← Read this next for full context

### 2. IMPLEMENTATION GUIDES (Read before coding)
- **`USER_AUTHENTICATION_GUIDE.md`** ← Phase 1 detailed implementation
- **`PUBLIC_SHARING_GUIDE.md`** ← Phase 2 detailed implementation  
- **`DATA_MIGRATION_GUIDE.md`** ← Critical for data safety

### 3. QUALITY ASSURANCE (Reference during coding)
- **`TESTING_CHECKLIST.md`** ← Use throughout implementation
- **`DEPLOYMENT_GUIDE.md`** ← For production deployment

### 4. COORDINATION (Working methodology)
- **`CLAUDE_CODE_COORDINATION.md`** ← How to work effectively
- **`IMPLEMENTATION_SUMMARY.md`** ← Final overview

## 🚨 CRITICAL FIRST ACTIONS

Before writing any code, Claude Code must:

### Step 1: Analyze Current System
```
1. Review the existing Flask application structure
2. Understand current routes/auth.py implementation
3. Map utils/helpers.py data patterns
4. Examine data/ directory structure
5. Identify existing authentication flow
```

### Step 2: Confirm Understanding
After reading all documents, respond with:
```
✅ Current system analysis complete
✅ Implementation phases understood  
✅ Data migration risks identified
✅ Testing strategy confirmed
✅ Ready to proceed with Phase 1
```

### Step 3: Implementation Approach
```
PHASE 1: User Authentication (6-8 hours)
- Create utils/user_helpers.py
- Update routes/auth.py for registration
- Modify utils/decorators.py
- Update admin routes for user scoping
- Create migration script

PHASE 2: Public Sharing (4-6 hours)  
- Create utils/access_manager.py
- Create routes/public.py
- Update publishing workflow
- Create crew-optimized templates
- Implement access management
```

## 🛡️ IMPLEMENTATION RULES

### Data Safety (NON-NEGOTIABLE)
- ❌ **NEVER modify existing data structure without backup**
- ❌ **NEVER implement everything at once**
- ❌ **NEVER skip testing after each component**
- ✅ **ALWAYS follow migration guide for data changes**
- ✅ **ALWAYS test with sample data first**

### Code Quality (MANDATORY)
- ✅ **Follow existing code patterns exactly**
- ✅ **Use same imports and structure as current files**
- ✅ **Maintain Flask blueprint organization**
- ✅ **Keep existing logging and error handling style**
- ✅ **Preserve all existing functionality**

### Security (CRITICAL)
- ✅ **Hash passwords with werkzeug.security**
- ✅ **Validate all user inputs**
- ✅ **Implement proper session management**
- ✅ **Ensure user data isolation**
- ✅ **Secure public routes against abuse**

## 🔄 IMPLEMENTATION WORKFLOW

### Phase 1A: Foundation (2 hours)
```
1. Create utils/user_helpers.py
   - User registration/login functions
   - Password hashing
   - User directory management

2. Test user creation and authentication
   - Sample user creation
   - Login verification
   - Password validation
```

### Phase 1B: Authentication Enhancement (2 hours)
```
1. Update routes/auth.py
   - Add registration route
   - Enhance login route
   - Update templates

2. Update utils/decorators.py  
   - User-based authentication
   - Session management
   - Access control
```

### Phase 1C: User Scoping (2-3 hours)
```
1. Modify utils/helpers.py
   - User-scoped data operations
   - Project filtering by user
   - Data isolation

2. Update admin routes
   - Filter projects by current user
   - Ensure data security
   - Maintain functionality
```

### Phase 1D: Migration (1-2 hours)
```
1. Create migrate_to_users.py
   - Backup existing data
   - Create user structure
   - Move projects to admin user
   - Verify migration success
```

## 🧪 TESTING AFTER EACH STEP

After implementing each phase component:

```bash
# Basic functionality test
1. Can application start without errors?
2. Can existing functionality still work?
3. Are new features working as expected?
4. Is data integrity maintained?
5. Are security measures in place?
```

## 🚦 PROCEED/STOP CRITERIA

### ✅ PROCEED when:
- Current phase testing passes
- No existing functionality broken
- Data integrity verified
- Security measures confirmed
- Human approves next phase

### 🛑 STOP if:
- Any existing functionality breaks
- Data corruption detected
- Security vulnerabilities found
- Tests fail
- Human requests pause

## 💬 COMMUNICATION PROTOCOL

### Before Starting Each Phase:
```
Claude Code should say:
"Ready to implement [PHASE NAME]. 
Current status: [summary of completed work]
Next steps: [list of specific tasks]
Estimated time: [time estimate]
Proceed? (y/n)"
```

### After Completing Each Component:
```
Claude Code should report:
"Completed: [component name]
✅ Functionality verified
✅ Tests passed  
✅ No regressions detected
Ready for next component: [next component name]"
```

### If Issues Arise:
```
Claude Code should immediately report:
"⚠️ Issue detected: [description]
Impact: [what's affected]
Recommended action: [suggestion]
Awaiting human guidance before proceeding."
```

## 🎯 SUCCESS CRITERIA

### Phase 1 Complete When:
- [ ] Users can register and login
- [ ] Each user sees only their projects
- [ ] All existing functionality preserved  
- [ ] Migration completed successfully
- [ ] All Phase 1 tests pass

### Phase 2 Complete When:
- [ ] Admins can publish with access codes
- [ ] Crew can access via codes/links
- [ ] Mobile interface optimized
- [ ] Access can be managed/revoked
- [ ] All Phase 2 tests pass

## 🚀 FINAL VALIDATION

Project complete when this workflow works:
```
1. 1st AD registers account
2. Creates project and builds calendar
3. Publishes calendar → generates access code
4. Shares code with crew via email
5. Crew enters code → sees mobile-optimized schedule
6. 1st AD updates schedule → crew sees changes immediately
```

## 📞 HUMAN INTERACTION POINTS

Claude Code should ask for human approval at:
1. **Before starting implementation** - After reading all docs
2. **Before data migration** - Critical data safety point
3. **Before Phase 2** - After Phase 1 testing complete
4. **If any errors occur** - Immediate escalation
5. **Before deployment** - Final approval

---

## 🎬 REMEMBER THE GOAL

This isn't just a coding exercise - you're building a **professional film industry tool** that will be used on real movie sets to coordinate schedules for 100+ crew members.

**Quality and reliability are paramount.**

## ✅ CLAUDE CODE ACKNOWLEDGMENT REQUIRED

Please respond with:
```
✅ I have read START_HERE_CLAUDE_CODE.md
✅ I understand this is a film industry production tool
✅ I will read all documentation before coding
✅ I will follow the implementation phases exactly
✅ I will prioritize data safety and existing functionality
✅ I will test thoroughly after each component
✅ I am ready to read the remaining documentation

Next action: Reading CLAUDE_CODE_IMPLEMENTATION_OVERVIEW.md
```

**Only proceed with implementation after human confirms you've read and understood all documentation.**