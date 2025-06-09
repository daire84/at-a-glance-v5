# v5 to v6 Transition Documentation

## Transition Summary
- **Transition Date**: 20250609_213625
- **v5 Backup Location**: /mnt/user/appdata/film-scheduler-v5/../backups/film-scheduler-v5-stable-20250609_213625
- **v6 Location**: /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6

## Port Configuration
- **v5 (stable)**: http://localhost:5075
- **v6 (development)**: http://localhost:5076

## Quick Commands

### Start v6
```bash
cd /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6
./start-v6.sh
```

### Check Status
```bash
cd /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6
./status.sh
```

### View Logs
```bash
cd /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6
./logs-v6.sh
```

## Backup Information
Full v5 backup available at: /mnt/user/appdata/film-scheduler-v5/../backups/film-scheduler-v5-stable-20250609_213625

To restore v5 if needed:
```bash
cd /mnt/user/appdata/film-scheduler-v5/../backups/film-scheduler-v5-stable-20250609_213625
./restore-v5.sh /path/to/restore/location
```

## Claude Code Setup
1. Install Claude Code CLI
2. Navigate to: /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6
3. Start Claude Code session
4. Begin development on 'claude-code-development' branch

## Data Migration
When v6 is stable and ready for production:
```bash
cp -R /path/to/v5/data/* /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6/data/
cd /mnt/user/appdata/film-scheduler-v5/../film-scheduler-v6
docker-compose restart
```
