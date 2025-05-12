/**
 * Version Manager for Film Scheduler
 * Handles version creation, listing, and management
 */

class VersionManager {
    constructor(projectId) {
        this.projectId = projectId;
        this.currentVersions = [];
        this.isVersioned = false;
        this.container = null;
    }

    /**
     * Initialize the version manager
     */
    async initialize(projectData = null) {
        try {
            // Use provided project data or fetch from API
            const project = projectData ? projectData : await this.getProject();
            this.isVersioned = project.isVersioned || false;
    
            if (!this.isVersioned) {
                console.log('Project is not versioned yet - but will show UI anyway');
            }
    
            // Create the version UI container regardless of versioned status
            this.createVersionUI();
    
            // Only load versions if project is versioned
            if (this.isVersioned) {
                // Load versions
                await this.loadVersions();
    
                // Check for workspace changes
                this.checkWorkspaceStatus();
            }
    
        } catch (error) {
            console.error('Error initializing version manager:', error);
            // Still create the UI even on error
            this.isVersioned = false;
            this.createVersionUI();
        }
    }

    /**
     * Get project data
     */
    async getProject() {
        const response = await fetch(`/api/projects/${this.projectId}`);
        if (!response.ok) {
            throw new Error('Failed to load project');
        }
        return await response.json();
    }

    /**
     * Create the version UI container
     */
    createVersionUI() {
        // Find or create container
        this.container = document.getElementById('version-manager');
        
        if (!this.container) {
            // Create container in the calendar page
            const calendarContainer = document.querySelector('.calendar-container');
            if (calendarContainer) {
                const versionSection = document.createElement('div');
                versionSection.id = 'version-manager';
                versionSection.className = 'version-manager-section';
                versionSection.innerHTML = `
                    <div class="version-manager-header">
                        <h3>Version Management</h3>
                        <div class="version-actions">
                            <button id="create-version-btn" class="button small ${!this.isVersioned ? 'hidden' : ''}">Save as Version</button>
                            <button id="migrate-project-btn" class="button small secondary ${this.isVersioned ? 'hidden' : ''}">Enable Versioning</button>
                        </div>
                    </div>
                    <div id="workspace-indicator" class="workspace-indicator ${!this.isVersioned ? 'hidden' : ''}">
                        <span class="draft-badge">Draft</span>
                        <span class="draft-message">Working in draft mode - changes not yet versioned</span>
                    </div>
                    <div id="version-list" class="version-list">
                        <div class="loading">Loading versions...</div>
                    </div>
                `;
                
                // Insert before the calendar table
                calendarContainer.insertBefore(versionSection, calendarContainer.firstChild);
                this.container = versionSection;
            }
        } else {
            // Update existing container
            this.container.className = 'version-manager-section';
            this.container.innerHTML = `
                <div class="version-manager-header">
                    <h3>Version Management</h3>
                    <div class="version-actions">
                        <button id="create-version-btn" class="button small ${!this.isVersioned ? 'hidden' : ''}">Save as Version</button>
                        <button id="migrate-project-btn" class="button small secondary ${this.isVersioned ? 'hidden' : ''}">Enable Versioning</button>
                    </div>
                </div>
                <div id="workspace-indicator" class="workspace-indicator ${!this.isVersioned ? 'hidden' : ''}">
                    <span class="draft-badge">Draft</span>
                    <span class="draft-message">Working in draft mode - changes not yet versioned</span>
                </div>
                <div id="version-list" class="version-list">
                    <div class="loading">Loading versions...</div>
                </div>
            `;
        }

        // Add event listeners
        this.attachEventListeners();
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        const createBtn = document.getElementById('create-version-btn');
        const migrateBtn = document.getElementById('migrate-project-btn');

        if (createBtn) {
            createBtn.addEventListener('click', () => this.showCreateVersionModal());
        }

        if (migrateBtn) {
            migrateBtn.addEventListener('click', () => this.migrateProject());
        }
    }

    /**
     * Load versions from API
     */
    async loadVersions() {
        try {
            const response = await fetch(`/api/projects/${this.projectId}/versions`);
            if (!response.ok) {
                throw new Error('Failed to load versions');
            }

            this.currentVersions = await response.json();
            this.renderVersionList();

        } catch (error) {
            console.error('Error loading versions:', error);
            this.showError('Failed to load versions');
        }
    }

    /**
     * Render the version list
     */
    renderVersionList() {
        const listContainer = document.getElementById('version-list');
        if (!listContainer) return;

        if (this.currentVersions.length === 0) {
            listContainer.innerHTML = '<div class="empty-state">No versions created yet</div>';
            return;
        }

        // Sort versions by created date (newest first)
        const sortedVersions = [...this.currentVersions].sort((a, b) => 
            new Date(b.createdAt) - new Date(a.createdAt)
        );

        const versionHTML = sortedVersions.map(version => {
            const createdDate = new Date(version.createdAt).toLocaleString();
            const publishedDate = version.publishedAt ? 
                new Date(version.publishedAt).toLocaleString() : 'Not published';

            return `
                <div class="version-item ${version.isLatestPublished ? 'published' : ''}" data-version-id="${version.id}">
                    <div class="version-info">
                        <div class="version-number">
                            Version ${version.versionNumber}
                            ${version.isLatestPublished ? '<span class="published-badge">Published</span>' : ''}
                        </div>
                        <div class="version-dates">
                            Created: ${createdDate}
                            ${version.isPublished ? `<br>Published: ${publishedDate}` : ''}
                        </div>
                        ${version.notes ? `<div class="version-notes">${version.notes}</div>` : ''}
                    </div>
                    <div class="version-actions">
                        ${!version.isPublished ? 
                            `<button class="button small publish-btn" data-version-id="${version.id}">Publish</button>` : 
                            ''
                        }
                        <button class="button small secondary view-btn" data-version-id="${version.id}">View</button>
                    </div>
                </div>
            `;
        }).join('');

        listContainer.innerHTML = versionHTML;

        // Add event listeners to buttons
        this.attachVersionButtonListeners();
    }

    /**
     * Attach listeners to version action buttons
     */
    attachVersionButtonListeners() {
        // Publish buttons
        document.querySelectorAll('.publish-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const versionId = e.target.dataset.versionId;
                this.publishVersion(versionId);
            });
        });

        // View buttons
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const versionId = e.target.dataset.versionId;
                this.viewVersion(versionId);
            });
        });
    }

    /**
     * Show create version modal
     */
    showCreateVersionModal() {
        // Get the next version number
        const nextVersionNumber = this.getNextVersionNumber();

        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Create New Version</h3>
                    <button class="close-button" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="create-version-form">
                        <div class="form-group">
                            <label for="version-number">Version Number</label>
                            <input type="text" id="version-number" value="${nextVersionNumber}" required>
                        </div>
                        <div class="form-group">
                            <label for="version-notes">Version Notes (optional)</label>
                            <textarea id="version-notes" rows="3" 
                                placeholder="Describe what changed in this version..."></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="button secondary" onclick="this.closest('.modal').remove()">Cancel</button>
                    <button class="button" onclick="versionManager.createVersion()">Create Version</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Get next version number
     */
    getNextVersionNumber() {
        if (this.currentVersions.length === 0) {
            return '1.0';
        }

        // Get the highest version number and increment
        const latestVersion = this.currentVersions
            .map(v => v.versionNumber)
            .sort((a, b) => this.compareVersionNumbers(b, a))[0];

        const parts = latestVersion.split('.');
        const major = parseInt(parts[0]);
        const minor = parseInt(parts[1] || 0);

        return `${major}.${minor + 1}`;
    }

    /**
     * Compare version numbers
     */
    compareVersionNumbers(a, b) {
        const aParts = a.split('.').map(n => parseInt(n));
        const bParts = b.split('.').map(n => parseInt(n));

        for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
            const aPart = aParts[i] || 0;
            const bPart = bParts[i] || 0;

            if (aPart > bPart) return 1;
            if (aPart < bPart) return -1;
        }

        return 0;
    }

    /**
     * Create a new version
     */
    async createVersion() {
        const versionNumber = document.getElementById('version-number').value;
        const notes = document.getElementById('version-notes').value;

        try {
            const response = await fetch(`/api/projects/${this.projectId}/versions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    versionNumber: versionNumber,
                    notes: notes
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to create version');
            }

            // Close modal
            document.querySelector('.modal').remove();

            // Reload versions
            await this.loadVersions();

            // Update workspace indicator
            this.checkWorkspaceStatus();

            // Show success message
            this.showSuccess(`Version ${versionNumber} created successfully`);

        } catch (error) {
            console.error('Error creating version:', error);
            this.showError(error.message || 'Failed to create version');
        }
    }

    /**
     * Publish a version
     */
    async publishVersion(versionId) {
        if (!confirm('Are you sure you want to publish this version? This will make it visible to viewers.')) {
            return;
        }

        try {
            const response = await fetch(`/api/projects/${this.projectId}/versions/${versionId}/publish`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to publish version');
            }

            // Reload versions
            await this.loadVersions();

            this.showSuccess('Version published successfully');

        } catch (error) {
            console.error('Error publishing version:', error);
            this.showError(error.message || 'Failed to publish version');
        }
    }

    /**
     * View a specific version
     */
    viewVersion(versionId) {
        // Open viewer page with version parameter
        window.open(`/viewer/${this.projectId}?version=${versionId}`, '_blank');
    }

    /**
     * Check workspace status
     */
    async checkWorkspaceStatus() {
        try {
            const response = await fetch(`/api/projects/${this.projectId}/workspace`);
            if (!response.ok) {
                throw new Error('Failed to check workspace');
            }

            const workspace = await response.json();
            const indicator = document.getElementById('workspace-indicator');
            
            if (indicator && workspace.isDraft) {
                indicator.classList.remove('hidden');
            } else if (indicator) {
                indicator.classList.add('hidden');
            }

        } catch (error) {
            console.error('Error checking workspace:', error);
        }
    }

    /**
     * Migrate project to versioned structure
     */
    async migrateProject() {
        if (!confirm('This will enable versioning for this project. Continue?')) {
            return;
        }

        try {
            const response = await fetch(`/api/projects/${this.projectId}/migrate-to-versioned`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to migrate project');
            }

            // Reload page to show versioned UI
            window.location.reload();

        } catch (error) {
            console.error('Error migrating project:', error);
            this.showError(error.message || 'Failed to migrate project');
        }
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    /**
     * Show error message
     */
    showError(message) {
        this.showNotification(message, 'error');
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="close-button" onclick="this.parentElement.remove()">&times;</button>
        `;

        // Add to page
        const container = document.querySelector('.notification-container') || 
            (() => {
                const nc = document.createElement('div');
                nc.className = 'notification-container';
                document.body.appendChild(nc);
                return nc;
            })();

        container.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Initialize version manager when page loads
let versionManager;

document.addEventListener('DOMContentLoaded', function() {
    // Only initialize on admin calendar page
    const projectIdElement = document.getElementById('project-id');
    const isAdminCalendar = document.querySelector('.admin-calendar');
    
    if (projectIdElement && isAdminCalendar) {
        const projectId = projectIdElement.value;
        // Don't initialize here - let calendar.html do it with project data
        // versionManager = new VersionManager(projectId);
        // versionManager.initialize();
    }
});