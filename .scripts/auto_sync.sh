#!/bin/bash
# Auto-sync study repo to GitHub - called by cron job
# Silent when no changes (watchdog pattern)

REPO_DIR="/home/neyo/workspace/code/study"
cd "$REPO_DIR" || exit 1

# Check if there are any changes (tracked modifications or untracked files not in gitignore)
CHANGES=$(git status --porcelain 2>/dev/null)
if [ -z "$CHANGES" ]; then
    exit 0  # Nothing to commit, stay silent
fi

# We have changes - commit and push
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git add -A 2>/dev/null

# Count changed files
FILE_COUNT=$(echo "$CHANGES" | wc -l)
FILE_LIST=$(echo "$CHANGES" | awk '{print $2}' | sed 's|.*/||' | tr '\n' ', ' | sed 's/, $//' | head -c 200)

git commit -m "auto-sync: $FILE_COUNT file(s) updated ($TIMESTAMP)" 2>/dev/null
git push 2>&1

echo "[$TIMESTAMP] 已同步 $FILE_COUNT 个文件到 GitHub: $FILE_LIST"
