# Claude Code Shortcuts

## Quick Launch Options

### From Unraid Terminal:
```bash
cd /mnt/user/appdata/film-scheduler-v6

# Method 1: Full script (with status messages)
./claude-code

# Method 2: Super simple (silent launch)
./cc

# Method 3: Manual but reliable
./dev-shell
node /usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js
```

### Inside Dev Container:
```bash
# After running ./dev-shell

# Method 1: Fixed claude command
claude

# Method 2: Short alias
cc

# Method 3: Direct node (always works)
node /usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js
```

## Recommended Workflow

### Quick Start:
```bash
cd /mnt/user/appdata/film-scheduler-v6
./cc
```

### Development Session:
```bash
cd /mnt/user/appdata/film-scheduler-v6
./dev-shell
cc  # or claude
```

## Troubleshooting

If any method fails:
```bash
# Always works:
./dev-shell
node /usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js
```

## Container Management

```bash
# Check status
docker ps | grep claude-code-dev

# Restart if needed
docker restart claude-code-dev

# Check logs
docker logs claude-code-dev
```
