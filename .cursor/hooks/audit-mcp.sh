#!/bin/bash
# Audit MCP tool calls (allow all, log for review).
input=$(cat)

mkdir -p logs
printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$input" >> logs/mcp-audit.log

echo '{"permission": "allow"}'
exit 0
