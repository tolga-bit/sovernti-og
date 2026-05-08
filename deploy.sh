#!/bin/bash
# deploy.sh — One-command deploy for sovernti-og
#
# Usage:
#   ./deploy.sh                    # uses default commit message
#   ./deploy.sh "Add SVN-S10"      # custom commit message
#
# What this does:
#   1. Rebuilds all 9 wrapper HTMLs from build.py (in case build.py changed)
#   2. Stages all changes
#   3. Commits with the provided message (or default)
#   4. Pushes to origin/main
#
# After push: Cloudflare Pages auto-deploys in ~30-60 seconds.
# Verify at https://og.sovernti.com/svn-sNN.html

set -e

cd "$(dirname "$0")"

# 1. Rebuild wrappers from template + metadata
echo "→ Rebuilding wrappers from build.py..."
python3 build.py

# 2. Check if there are any changes
if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
  echo ""
  echo "No changes to deploy. (build.py output is identical to current files.)"
  exit 0
fi

# 3. Show what changed
echo ""
echo "→ Changes to be committed:"
git status --short

# 4. Stage + commit + push
MESSAGE="${1:-Update OG wrappers}"
echo ""
echo "→ Committing: \"$MESSAGE\""
git add .
git commit -m "$MESSAGE"

echo ""
echo "→ Pushing to origin/main..."
git push

# 5. Done
echo ""
echo "✅ Pushed to GitHub."
echo "   Cloudflare Pages will deploy in ~30-60 seconds."
echo "   Verify at https://og.sovernti.com/svn-s08.html (or any updated wrapper)."
echo ""
echo "Per Verification Evidence Standard, capture Post Inspector screenshot before"
echo "flipping any Deployment Ledger row to VERIFIED:"
echo "   https://www.linkedin.com/post-inspector/"
