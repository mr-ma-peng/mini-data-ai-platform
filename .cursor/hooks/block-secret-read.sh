#!/bin/bash
# Prevent reading .env and other secret files.
input=$(cat)

if echo "$input" | grep -qE '\.env(\.|$)|credentials|secrets\.json|\.pem'; then
  cat <<'EOF'
{
  "permission": "deny",
  "user_message": "已拦截读取敏感文件（.env / 密钥）。请使用 .env.example 或 config.settings。",
  "agent_message": "Project hook blocked read of a sensitive file. Use .env.example or config.settings instead."
}
EOF
  exit 0
fi

echo '{"permission": "allow"}'
exit 0
