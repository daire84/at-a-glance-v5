# Public Calendar Sharing System Implementation Guide

## 🎯 OBJECTIVE
Enable production admins to publish calendars with auto-generated access codes and shareable links, allowing crew members to view schedules without creating accounts.

## 📋 PRE-IMPLEMENTATION REQUIREMENTS

- [ ] User authentication system fully implemented and tested
- [ ] All tests from Phase 1 are passing
- [ ] Understanding of current publishing system (`workspace.json` → `versions.json`)
- [ ] Understanding of current viewer routes in `routes/main.py`

## 🎬 TARGET WORKFLOW

### Admin Workflow:
1. Admin edits calendar in workspace
2. Admin clicks "Publish Calendar"
3. System generates **Access Code** (`HAMLET24`) and **Share Link** (`/calendar/abc123`)
4. Admin copies code/link to share with crew via email/text
5. Crew members access calendar without accounts

### Crew Workflow:
```
Option A: crew@email.com receives: "Schedule updated! Link: yourapp.com/calendar/abc123"
         → Clicks link → Sees calendar immediately

Option B: crew@email.com receives: "Schedule updated! Code: HAMLET24"
         → Visits yourapp.com/access → Enters code → Sees calendar
```

## 🏗️ IMPLEMENTATION STEPS

### Step 1: Create Access Management System

**File to Create: `utils/access_manager.py`**

**Core Functions Required:**
```python
class ProjectAccessManager:
    def generate_access_code(length=8):
        """Generate human-friendly code like 'HAMLET24'"""
        
    def generate_access_token():
        """Generate URL-safe token for direct links"""
        
    def publish_calendar_with_access(user_id, project_id, calendar_data, project_data):
        """Publish calendar and create public access"""
        
    def get_calendar_by_code(access_code):
        """Retrieve calendar data by access code"""
        
    def get_calendar_by_token(access_token):
        """Retrieve calendar data by access token"""
        
    def revoke_access(user_id, project_id):
        """Revoke public access for a project"""
        
    def update_access_stats(access_identifier):
        """Track view counts and last access"""
```

**Technical Requirements:**
- Access codes: 8 characters, uppercase letters + numbers, avoid confusing chars (0,O,1,I)
- Access tokens: URL-safe, 16 characters minimum
- Both code and token point to same calendar data
- Track usage statistics (view count, last accessed)
- Support access revocation
- Auto-cleanup expired access (optional)

### Step 2: Create Public Data Storage

**Directory Structure to Create:**
```
data/
├── public/                   # New public access directory
│   ├── {access_code}/        # e.g., "HAMLET24"
│   │   └── calendar.json     # Public calendar data
│   └── {access_token}/       # e.g., "abc123def456"
│       └── calendar.json     # Same data, different access method
```

**Public Calendar Data Format:**
```json
{
  "project": {
    "name": "Hamlet - Feature Film",
    "id": "project-uuid",
    "published_at": "2024-01-15T10:30:00Z"
  },
  "calendar": {
    "days": [...],
    "departments": [...],
    "locations": [...]
  },
  "access": {
    "access_code": "HAMLET24",
    "access_token": "abc123def456",
    "created_at": "2024-01-15T10:30:00Z",
    "expires_at": null,
    "view_count": 42,
    "last_accessed": "2024-01-16T14:22:00Z"
  }
}
```

### Step 3: Create Public Access Routes

**File to Create: `routes/public.py`**

**Routes Required:**
```python
@public_bp.route('/calendar/<access_token>')
def view_calendar_by_token(access_token):
    """Direct calendar access via shareable link"""

@public_bp.route('/access', methods=['GET', 'POST'])
def access_code_entry():
    """Access code entry page"""

@public_bp.route('/production/<project_name>')  # Future feature
def production_landing(project_name):
    """Branded production landing pages"""
```

**Critical Requirements:**
- No authentication required for these routes
- Mobile-optimized templates
- Error handling for invalid codes/tokens
- Usage tracking on each access
- SEO-friendly for production pages

### Step 4: Enhanced Publishing System

**File to Modify: `routes/admin.py`**

**New Routes to Add:**
```python
@admin_bp.route('/project/<project_id>/publish', methods=['POST'])
@login_required
def publish_project(project_id):
    """Publish project calendar with public access generation"""

@admin_bp.route('/project/<project_id>/access')
@login_required  
def manage_project_access(project_id):
    """Manage public access settings for project"""

@admin_bp.route('/project/<project_id>/access/revoke', methods=['POST'])
@login_required
def revoke_project_access(project_id):
    """Revoke public access for project"""
```

**Publishing Workflow:**
1. Get current workspace data
2. Create new version (existing system)
3. Generate access code + token
4. Save public calendar data
5. Update project access metadata
6. Show success page with sharing options

### Step 5: Create Public Calendar Templates

**File to Create: `templates/public/calendar.html`**

**Requirements:**
- Standalone template (not extending admin base.html)
- Mobile-first responsive design
- Simplified navigation for crew members
- Print-optimized styling
- No admin functionality visible
- Clear production branding area

**Key Elements:**
```html
<div class="public-header">
    <h1>{{ project_name }}</h1>
    <div class="production-meta">
        <span>Updated: {{ published_date }}</span>
        <span>Code: {{ access_code }}</span>
    </div>
    <div class="public-actions">
        <button onclick="window.print()">Print</button>
        <button onclick="goToToday()">Today</button>
    </div>
</div>

<div class="calendar-container">
    <!-- Reuse existing calendar display components -->
</div>

<div class="public-footer">
    <p>Read-only production calendar</p>
    <p>Contact production office for questions</p>
</div>
```

### Step 6: Create Access Entry Interface

**File to Create: `templates/public/access_entry.html`**

**Requirements:**
- Simple, crew-friendly interface
- Large, clear code entry field
- Auto-uppercase input
- Clear error messages
- Help text for getting codes
- Mobile-optimized form

**Form Features:**
- 8-character limit with formatting
- Real-time validation
- Submit on enter
- Clear success/error feedback
- "Don't have a code?" help section

### Step 7: Create Publishing Success Interface

**File to Create: `templates/admin/publish_success.html`**

**Purpose:** Show sharing options after successful publishing

**Content Required:**
```html
<div class="sharing-options">
    <h3>Share with Crew</h3>
    
    <div class="share-method">
        <h4>Access Code</h4>
        <div class="access-code-display">
            <code>HAMLET24</code>
            <button onclick="copyToClipboard()">Copy</button>
        </div>
        <p>Crew enters this at: yourapp.com/access</p>
    </div>
    
    <div class="share-method">
        <h4>Direct Link</h4>
        <div class="share-link-display">
            <input readonly value="yourapp.com/calendar/abc123">
            <button onclick="copyToClipboard()">Copy Link</button>
        </div>
    </div>
    
    <div class="email-template">
        <h4>Email Template</h4>
        <textarea readonly>
Subject: Hamlet Schedule Update
        
Updated schedule is now available:
🔗 Link: yourapp.com/calendar/abc123
📧 Code: HAMLET24 (enter at yourapp.com/access)

Questions? Contact production office.
        </textarea>
    </div>
</div>
```

### Step 8: Update Admin Project Interface

**Files to Modify:**
- `templates/admin/project.html` - Add "Publish Calendar" button
- `templates/admin/calendar.html` - Add publishing controls
- `templates/admin/dashboard.html` - Show access status for projects

**New Elements:**
```html
<!-- In calendar editor -->
<div class="publishing-controls">
    <button id="publish-calendar" class="button primary">
        Publish Calendar
    </button>
    <span class="publish-status">
        <!-- Show current access code if published -->
    </span>
</div>

<!-- Publishing modal -->
<div id="publish-modal" class="modal">
    <form action="/admin/project/{id}/publish" method="POST">
        <input name="version_number" placeholder="1.0">
        <textarea name="notes" placeholder="Version notes"></textarea>
        <button type="submit">Publish & Generate Access</button>
    </form>
</div>
```

### Step 9: Access Management Interface

**File to Create: `templates/admin/project_access.html`**

**Features:**
- Display current access code and link
- View usage statistics
- Revoke access button
- Generate new access codes
- QR code display (future feature)

```html
<div class="access-management">
    <h3>Public Access</h3>
    
    {% if access_info %}
    <div class="current-access">
        <div class="access-details">
            <strong>Access Code:</strong> {{ access_info.access_code }}
            <strong>Direct Link:</strong> /calendar/{{ access_info.access_token }}
            <strong>Created:</strong> {{ access_info.created_at }}
            <strong>Views:</strong> {{ access_info.view_count }}
            <strong>Last Accessed:</strong> {{ access_info.last_accessed }}
        </div>
        
        <div class="access-actions">
            <button onclick="copyAccessCode()">Copy Code</button>
            <button onclick="copyShareLink()">Copy Link</button>
            <button onclick="revokeAccess()" class="danger">Revoke Access</button>
        </div>
    </div>
    {% else %}
    <p>This project is not published for public access.</p>
    <a href="/admin/project/{{ project.id }}/calendar">Publish Calendar</a>
    {% endif %}
</div>
```

### Step 10: Register Public Blueprint

**File to Modify: `app.py`**

**Add to blueprint registration:**
```python
from routes.public import public_bp
app.register_blueprint(public_bp)
```

**URL patterns will be:**
- `/calendar/<token>` - Direct calendar access
- `/access` - Code entry page
- `/production/<name>` - Production landing pages

## 🧪 TESTING REQUIREMENTS

### Functional Testing
- [ ] Admin can publish calendar and generate access
- [ ] Access code entry works correctly
- [ ] Direct links work correctly
- [ ] Invalid codes show appropriate errors
- [ ] Mobile interface works on actual devices
- [ ] Print functionality works properly

### Security Testing
- [ ] Invalid tokens return 404, not errors
- [ ] Access codes can't be guessed easily
- [ ] No sensitive admin data exposed in public views
- [ ] Access revocation works immediately
- [ ] No cross-project data leakage

### Performance Testing
- [ ] Public pages load quickly
- [ ] Large calendars render efficiently
- [ ] Multiple concurrent access works
- [ ] File system performance acceptable

### Integration Testing
- [ ] Publishing updates existing public access
- [ ] Version updates reflected in public view
- [ ] User isolation maintained
- [ ] Backup/restore includes public data

## 📱 MOBILE OPTIMIZATION

### CSS Requirements
```css
/* Public calendar mobile styles */
@media (max-width: 768px) {
    .public-header {
        flex-direction: column;
        text-align: center;
    }
    
    .calendar-table {
        font-size: 0.8em;
        overflow-x: auto;
    }
    
    .access-code-display {
        font-size: 1.2em;
        padding: 1rem;
    }
}
```

### JavaScript Requirements
- Touch-friendly interactions
- Simplified navigation
- Auto-scroll to current date
- Copy-to-clipboard functionality
- Offline-friendly (future)

## 🔒 SECURITY CONSIDERATIONS

### Access Control
- Codes should be unguessable (entropy check)
- Tokens should be cryptographically secure
- No enumeration attacks possible
- Rate limiting for code attempts
- Access logs for security monitoring

### Data Privacy
- Only published data exposed publicly
- No admin interfaces accessible from public routes
- No personal user data in public calendars
- Clear data retention policies

### Production Security
- HTTPS required for shareable links
- Secure session configuration
- Input validation on all public endpoints
- XSS protection on user-generated content

## 📊 ANALYTICS & MONITORING

### Usage Statistics
- Track access frequency per project
- Monitor most popular access times
- Geographic access patterns (if IP logging enabled)
- Mobile vs desktop usage
- Print usage statistics

### Admin Dashboard Metrics
- Projects with public access
- Total crew access count
- Most accessed projects
- Access growth over time

## ✅ COMPLETION CHECKLIST

### Core Functionality
- [ ] Access code generation working
- [ ] Direct link access working
- [ ] Code entry page functional
- [ ] Public calendar display correct
- [ ] Mobile interface tested
- [ ] Publishing workflow complete

### Admin Features
- [ ] Publish button integrated
- [ ] Success page with sharing options
- [ ] Access management interface
- [ ] Usage statistics display
- [ ] Revocation functionality

### Security & Performance
- [ ] Security testing complete
- [ ] Performance benchmarks met
- [ ] Error handling robust
- [ ] Mobile optimization verified
- [ ] Print functionality tested

### Documentation
- [ ] Admin user guide created
- [ ] Crew access instructions written
- [ ] Troubleshooting guide available
- [ ] API documentation updated

## 🚀 DEPLOYMENT CONSIDERATIONS

### Environment Variables
```bash
# Add to .env
PUBLIC_ACCESS_ENABLED=true
ACCESS_CODE_LENGTH=8
ACCESS_TOKEN_LENGTH=16
MAX_DAILY_VIEWS=1000
```

### Monitoring
- Set up access logging
- Monitor storage usage in `data/public/`
- Track error rates on public endpoints
- Monitor performance of public calendar loads

### Backup Strategy
- Include `data/public/` in backup routine
- Regular cleanup of expired access codes
- Archive old access statistics
- Test restore procedures

## 🎉 SUCCESS METRICS

### User Adoption
- Number of admins using public sharing
- Frequency of calendar publishing
- Crew member engagement (view counts)
- Reduction in "Where's the schedule?" requests

### Technical Success
- Zero data loss during implementation
- Public page load times < 2 seconds
- Mobile usability score > 90%
- Error rate < 1% on public endpoints

This implementation creates a production-ready crew sharing system that transforms the scheduler into a comprehensive production tool.