#!/bin/bash
# Block dangerous git operations in this project.
input=$(cat)

if echo "$input" | grep -qE 'git push[^;]*--force|git push[^;]*-f[^a-z]|git config'; then
  cat <<'EOF'
{
  "permission": "deny",
  "user_message": "已拦截危险 Git 操作（force push / git config 修改）。",
  "agent_message": "Project hook blocked a dangerous git command. Use normal push or ask the user explicitly."
}
EOF
  exit 0
fi

echo '{"permission": "allow"}'
exit 0
