#!/bin/bash
# Super simple Claude Code launcher
docker exec -it claude-code-dev node --no-warnings --enable-source-maps /usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js "$@"
