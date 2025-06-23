# Production Deployment Guide

## 🎯 DEPLOYMENT OVERVIEW

This guide covers deploying the enhanced Film Production Scheduler with user authentication and public sharing capabilities in a production environment.

**Target Deployment:** Self-hosted on Unraid server with Docker containerization

## 📋 PRE-DEPLOYMENT CHECKLIST

### System Requirements
- [ ] **Hardware**: Minimum 2GB RAM, 10GB storage, dual-core CPU
- [ ] **Operating System**: Unraid 6.9+ (or Docker-compatible Linux)
- [ ] **Network**: Static IP address or domain name
- [ ] **SSL Certificate**: For HTTPS (recommended for production)
- [ ] **Backup Strategy**: Automated backup solution configured

### Software Prerequisites
- [ ] Docker and Docker Compose installed
- [ ] Reverse proxy configured (Nginx Proxy Manager, Traefik, etc.)
- [ ] Domain name configured (optional but recommended)
- [ ] Firewall rules configured
- [ ] Monitoring solution prepared

## 🏗️ DEPLOYMENT ARCHITECTURE

### Recommended Production Setup
```
┌─────────────────────────────────────────────────────────────┐
│                        UNRAID SERVER                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────────────────────┐  │
│  │ Nginx Proxy     │    │   Film Scheduler Container      │  │
│  │ Manager         │────│                                 │  │
│  │ (SSL/Domain)    │    │  ┌─────────────────────────────┐ │  │
│  └─────────────────┘    │  │     Flask Application      │ │  │
│                         │  │   - User Authentication    │ │  │
│  ┌─────────────────┐    │  │   - Public Sharing         │ │  │
│  │ File Browser    │    │  │   - Calendar Management    │ │  │
│  │ (Backup Access) │    │  └─────────────────────────────┘ │  │
│  └─────────────────┘    │                                 │  │
│                         │  ┌─────────────────────────────┐ │  │
│  ┌─────────────────┐    │  │      Data Volume            │ │  │
│  │ Monitoring      │    │  │   /app/data → /mnt/user/   │ │  │
│  │ (Uptime Kuma)   │    │  │               appdata/     │ │  │
│  └─────────────────┘    │  │               scheduler/    │ │  │
│                         │  └─────────────────────────────┘ │  │
│                         └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🐳 DOCKER CONFIGURATION

### Production docker-compose.yml
**File: `docker-compose.prod.yml`**

```yaml
version: '3.8'

services:
  film-scheduler:
    build: .
    container_name: film-scheduler-prod
    restart: unless-stopped
    
    environment:
      # Flask Configuration
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      TZ: ${TZ:-UTC}
      
      # User Authentication
      DEFAULT_ADMIN_USERNAME: ${DEFAULT_ADMIN_USERNAME:-admin}
      DEFAULT_ADMIN_EMAIL: ${DEFAULT_ADMIN_EMAIL}
      
      # Security Settings
      SESSION_COOKIE_SECURE: "true"
      SESSION_COOKIE_HTTPONLY: "true"
      SESSION_COOKIE_SAMESITE: "Lax"
      
      # Application Settings
      MAX_CONTENT_LENGTH: "16777216"  # 16MB
      PUBLIC_ACCESS_ENABLED: "true"
      ACCESS_CODE_LENGTH: "8"
      MAX_DAILY_VIEWS: "10000"
      
      # Logging
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
      
    volumes:
      # Data persistence
      - /mnt/user/appdata/scheduler/data:/app/data
      - /mnt/user/appdata/scheduler/logs:/app/logs
      
      # Backup directory (optional)
      - /mnt/user/backups/scheduler:/app/backups
      
    ports:
      - "5075:5000"
      
    networks:
      - scheduler-network
      - proxy-network  # For reverse proxy
      
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
      
    labels:
      # Traefik labels (if using Traefik)
      - "traefik.enable=true"
      - "traefik.http.routers.scheduler.rule=Host(`scheduler.yourdomain.com`)"
      - "traefik.http.routers.scheduler.tls=true"
      - "traefik.http.routers.scheduler.tls.certresolver=cloudflare"
      
      # For backup automation
      - "backup.enable=true"
      - "backup.path=/app/data"
      
networks:
  scheduler-network:
    driver: bridge
  proxy-network:
    external: true

# Optional: Backup service
  backup:
    image: alpine:latest
    container_name: scheduler-backup
    restart: "no"
    volumes:
      - /mnt/user/appdata/scheduler/data:/source:ro
      - /mnt/user/backups/scheduler:/backup
    command: |
      sh -c "
        tar -czf /backup/scheduler-backup-$$(date +%Y%m%d_%H%M%S).tar.gz -C /source .
        find /backup -name 'scheduler-backup-*.tar.gz' -mtime +30 -delete
      "
```

### Production Environment Variables
**File: `.env.production`**

```bash
# === CRITICAL SECURITY SETTINGS ===
SECRET_KEY=your-very-long-random-secret-key-change-this
DEFAULT_ADMIN_EMAIL=admin@yourproduction.com

# === APPLICATION SETTINGS ===
FLASK_ENV=production
TZ=America/Los_Angeles
LOG_LEVEL=INFO

# === DOMAIN CONFIGURATION ===
DOMAIN_NAME=scheduler.yourproduction.com
BASE_URL=https://scheduler.yourproduction.com

# === SECURITY SETTINGS ===
FORCE_HTTPS=true
SESSION_TIMEOUT=86400  # 24 hours
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900   # 15 minutes

# === PERFORMANCE SETTINGS ===
MAX_CONTENT_LENGTH=16777216
WORKERS=4
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100

# === PUBLIC ACCESS SETTINGS ===
PUBLIC_ACCESS_ENABLED=true
ACCESS_CODE_LENGTH=8
ACCESS_TOKEN_LENGTH=16
MAX_DAILY_VIEWS=10000
ACCESS_CODE_EXPIRY_DAYS=365

# === BACKUP SETTINGS ===
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
BACKUP_COMPRESSION=true

# === MONITORING ===
HEALTH_CHECK_ENABLED=true
METRICS_ENABLED=true
LOG_STRUCTURED=true
```

## 🔒 SECURITY CONFIGURATION

### SSL/TLS Setup
**Option 1: Nginx Proxy Manager (Recommended for Unraid)**
```yaml
# Nginx Proxy Manager configuration
# Access via: http://unraid-ip:81

# Add Proxy Host:
# Domain: scheduler.yourproduction.com
# Forward Hostname/IP: film-scheduler-prod
# Forward Port: 5000
# SSL: Request new certificate (Let's Encrypt)
```

**Option 2: Traefik (Advanced)**
```yaml
# Add to docker-compose.yml labels
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.scheduler.rule=Host(`scheduler.yourproduction.com`)"
  - "traefik.http.routers.scheduler.entrypoints=websecure"
  - "traefik.http.routers.scheduler.tls.certresolver=letsencrypt"
```

### Firewall Configuration
```bash
# Unraid firewall rules (if firewall enabled)
# Allow HTTPS traffic
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow specific IP ranges for admin access (optional)
iptables -A INPUT -p tcp --dport 443 -s 192.168.1.0/24 -j ACCEPT

# Block direct access to application port
iptables -A INPUT -p tcp --dport 5075 -j DROP
```

### Security Headers
**Add to Nginx configuration:**
```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self';" always;

# Remove server header
server_tokens off;
```

## 📊 MONITORING & LOGGING

### Application Monitoring
**File: `docker-compose.monitoring.yml`**

```yaml
version: '3.8'

services:
  # Uptime monitoring
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: scheduler-uptime
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - /mnt/user/appdata/uptime-kuma:/app/data
    networks:
      - scheduler-network

  # Log aggregation (optional)
  loki:
    image: grafana/loki:latest
    container_name: scheduler-loki
    restart: unless-stopped
    volumes:
      - /mnt/user/appdata/loki:/loki
    networks:
      - scheduler-network

networks:
  scheduler-network:
    external: true
```

### Log Configuration
**File: `logging.conf`**
```ini
[loggers]
keys=root,scheduler

[handlers]
keys=console,file,rotating

[formatters]
keys=standard,detailed

[logger_root]
level=INFO
handlers=console,rotating

[logger_scheduler]
level=INFO
handlers=file,rotating
qualname=scheduler
propagate=0

[handler_console]
class=StreamHandler
level=INFO
formatter=standard
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=INFO
formatter=detailed
args=('/app/logs/scheduler.log',)

[handler_rotating]
class=handlers.RotatingFileHandler
level=INFO
formatter=detailed
args=('/app/logs/scheduler.log', 'a', 10485760, 5)

[formatter_standard]
format=%(asctime)s [%(levelname)s] %(name)s: %(message)s

[formatter_detailed]
format=%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s
```

## 💾 BACKUP STRATEGY

### Automated Backup Script
**File: `backup-scheduler.sh`**

```bash
#!/bin/bash
# Automated backup script for Film Production Scheduler

# Configuration
BACKUP_DIR="/mnt/user/backups/scheduler"
DATA_DIR="/mnt/user/appdata/scheduler"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="scheduler-backup-${DATE}.tar.gz"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Stop container for consistent backup (optional)
echo "Creating backup: ${BACKUP_FILE}"
docker exec film-scheduler-prod python -c "print('Backup starting')"

# Create compressed backup
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" \
    -C "${DATA_DIR}" \
    data/ logs/

# Verify backup
if [ $? -eq 0 ]; then
    echo "✅ Backup created successfully: ${BACKUP_FILE}"
    
    # Calculate backup size
    BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo "📁 Backup size: ${BACKUP_SIZE}"
    
    # Remove old backups
    find "${BACKUP_DIR}" -name "scheduler-backup-*.tar.gz" -mtime +${RETENTION_DAYS} -delete
    echo "🧹 Cleaned up backups older than ${RETENTION_DAYS} days"
    
    # Optional: Upload to cloud storage
    # rsync "${BACKUP_DIR}/${BACKUP_FILE}" user@remote-server:/backups/
    
else
    echo "❌ Backup failed!"
    exit 1
fi
```

### Backup Automation with Cron
```bash
# Add to Unraid crontab
# Edit /boot/config/cron/root

# Daily backup at 2 AM
0 2 * * * /mnt/user/scripts/backup-scheduler.sh

# Weekly backup verification at 3 AM on Sundays
0 3 * * 0 /mnt/user/scripts/verify-backup.sh
```

### Backup Verification Script
**File: `verify-backup.sh`**

```bash
#!/bin/bash
# Verify backup integrity

BACKUP_DIR="/mnt/user/backups/scheduler"
LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/scheduler-backup-*.tar.gz | head -1)

if [ -f "${LATEST_BACKUP}" ]; then
    echo "🔍 Verifying backup: $(basename ${LATEST_BACKUP})"
    
    # Test archive integrity
    tar -tzf "${LATEST_BACKUP}" > /dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Backup verification passed"
        
        # Check for critical files
        tar -tzf "${LATEST_BACKUP}" | grep -q "data/users.json"
        if [ $? -eq 0 ]; then
            echo "✅ Critical files present"
        else
            echo "⚠️  Warning: users.json not found in backup"
        fi
    else
        echo "❌ Backup verification failed!"
        # Send alert (implement notification method)
    fi
else
    echo "❌ No backup files found!"
fi
```

## 🚀 DEPLOYMENT PROCESS

### Initial Deployment
```bash
# 1. Prepare directories
mkdir -p /mnt/user/appdata/scheduler/{data,logs}
mkdir -p /mnt/user/backups/scheduler
mkdir -p /mnt/user/scripts

# 2. Copy configuration files
cp .env.production /mnt/user/appdata/scheduler/.env
cp docker-compose.prod.yml /mnt/user/appdata/scheduler/docker-compose.yml

# 3. Set permissions
chown -R 1000:1000 /mnt/user/appdata/scheduler
chmod +x /mnt/user/scripts/backup-scheduler.sh

# 4. Build and deploy
cd /mnt/user/appdata/scheduler
docker-compose up -d

# 5. Run initial migration
docker exec -it film-scheduler-prod python migrate_to_users.py

# 6. Verify deployment
curl -f http://localhost:5075/health
```

### Update Deployment
```bash
# 1. Create backup before update
/mnt/user/scripts/backup-scheduler.sh

# 2. Stop container
docker-compose stop film-scheduler

# 3. Update image
docker-compose pull
docker-compose build

# 4. Start updated container
docker-compose up -d

# 5. Verify update
docker logs film-scheduler-prod
curl -f http://localhost:5075/health
```

### Rollback Procedure
```bash
# 1. Stop current container
docker-compose stop film-scheduler

# 2. Restore data from backup
LATEST_BACKUP=$(ls -t /mnt/user/backups/scheduler/scheduler-backup-*.tar.gz | head -1)
tar -xzf "${LATEST_BACKUP}" -C /mnt/user/appdata/scheduler/

# 3. Restart container
docker-compose up -d

# 4. Verify rollback
curl -f http://localhost:5075/health
```

## 📈 PERFORMANCE OPTIMIZATION

### Container Resource Limits
```yaml
# Add to docker-compose.yml
services:
  film-scheduler:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Application Optimization
```python
# Add to app.py for production
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure Gunicorn for production
# File: gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True
timeout = 120
keepalive = 5
```

### Nginx Optimization
```nginx
# nginx.conf optimization
worker_processes auto;
worker_connections 1024;

http {
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Caching
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=scheduler:10m rate=10r/s;
    limit_req zone=scheduler burst=20 nodelay;
}
```

## 📱 MOBILE OPTIMIZATION

### Progressive Web App (PWA) Configuration
**File: `static/manifest.json`**
```json
{
  "name": "Film Production Scheduler",
  "short_name": "Scheduler",
  "description": "Professional film production calendar management",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2c3e50",
  "icons": [
    {
      "src": "/static/images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Service Worker (Optional)
**File: `static/sw.js`**
```javascript
// Basic service worker for offline functionality
const CACHE_NAME = 'scheduler-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/calendar.js',
  '/static/images/icon-192.png'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
```

## 🔔 NOTIFICATION SYSTEM

### Email Notifications (Optional)
```python
# Add to requirements.txt
flask-mail==0.9.1

# Email configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

### Webhook Notifications
```bash
# Slack webhook for critical alerts
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Discord webhook (alternative)
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR/WEBHOOK"
```

## ✅ POST-DEPLOYMENT CHECKLIST

### Day 1 Verification
- [ ] Application accessible via domain name
- [ ] SSL certificate working correctly
- [ ] Admin user can login
- [ ] New user registration works
- [ ] Project creation functional
- [ ] Calendar publishing generates access codes
- [ ] Public access works via codes and links
- [ ] Mobile interface responsive
- [ ] Backup script executed successfully
- [ ] Monitoring alerts configured

### Week 1 Monitoring
- [ ] Performance metrics within acceptable ranges
- [ ] No critical errors in logs
- [ ] User adoption tracking
- [ ] Storage usage monitoring
- [ ] Security logs reviewed
- [ ] Backup integrity verified
- [ ] User feedback collected

### Month 1 Review
- [ ] Comprehensive performance analysis
- [ ] User satisfaction assessment
- [ ] Security audit completed
- [ ] Feature usage statistics reviewed
- [ ] Optimization opportunities identified
- [ ] Backup/restore procedures tested
- [ ] Documentation updated

## 🆘 TROUBLESHOOTING

### Common Issues

**Issue: Container won't start**
```bash
# Check logs
docker logs film-scheduler-prod

# Common fixes
docker-compose down
docker system prune -f
docker-compose up -d
```

**Issue: SSL certificate problems**
```bash
# Renew Let's Encrypt certificate
docker exec nginx-proxy-manager certbot renew

# Check certificate expiry
openssl s_client -connect scheduler.yourdomain.com:443 -servername scheduler.yourdomain.com | openssl x509 -noout -dates
```

**Issue: Database corruption**
```bash
# Restore from backup
LATEST_BACKUP=$(ls -t /mnt/user/backups/scheduler/scheduler-backup-*.tar.gz | head -1)
tar -xzf "${LATEST_BACKUP}" -C /mnt/user/appdata/scheduler/
docker-compose restart film-scheduler
```

**Issue: Performance degradation**
```bash
# Check resource usage
docker stats film-scheduler-prod

# Check disk space
df -h /mnt/user/appdata/scheduler

# Clean up logs
find /mnt/user/appdata/scheduler/logs -name "*.log" -mtime +7 -delete
```

This deployment guide ensures a robust, secure, and maintainable production environment for the Film Production Scheduler.