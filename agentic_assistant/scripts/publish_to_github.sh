#!/usr/bin/env bash
set -euo pipefail

usage(){
  echo "Usage: $0 --repo-name <name> [--private]"
  exit 1
}

REPO_NAME=""
PRIVATE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-name) REPO_NAME="$2"; shift 2;;
    --private) PRIVATE=1; shift;;
    *) usage;;
  esac
done

if [[ -z "$REPO_NAME" ]]; then
  usage
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh (GitHub CLI) not found. Install and run 'gh auth login' first." >&2
  exit 2
fi

git init 2>/dev/null || true
git add .
git commit -m "chore: publish repository" || true

if [[ $PRIVATE -eq 1 ]]; then
  gh repo create "$REPO_NAME" --private --source=. --push
else
  gh repo create "$REPO_NAME" --public --source=. --push
fi

echo "Repository published: $REPO_NAME"
