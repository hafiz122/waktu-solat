#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  refresh_site.sh --repo-dir <path> --branch <branch> [options]

Required:
  --repo-dir <path>       Absolute or relative repository path.
  --branch <branch>       Branch to pull from and push to.

Options:
  --remote <name>         Git remote name. Default: origin
  --python <bin>          Python executable. Default: python3
  --min-days-ahead <n>    Freshness threshold for validator. Default: 7
  --dry-run               Run generation + validation but skip commit/push.
  -h, --help              Show this help.

Environment:
  GIT_AUTHOR_NAME         Commit author name (required when commit is needed,
                          unless already configured in git config user.name)
  GIT_AUTHOR_EMAIL        Commit author email (required when commit is needed,
                          unless already configured in git config user.email)
EOF
}

REPO_DIR=""
BRANCH=""
REMOTE="origin"
PYTHON_BIN="python3"
MIN_DAYS_AHEAD="7"
DRY_RUN="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-dir)
      REPO_DIR="${2:-}"
      shift 2
      ;;
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --remote)
      REMOTE="${2:-}"
      shift 2
      ;;
    --python)
      PYTHON_BIN="${2:-}"
      shift 2
      ;;
    --min-days-ahead)
      MIN_DAYS_AHEAD="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="1"
      shift 1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$REPO_DIR" || -z "$BRANCH" ]]; then
  echo "--repo-dir and --branch are required." >&2
  usage
  exit 2
fi

if ! [[ "$MIN_DAYS_AHEAD" =~ ^[0-9]+$ ]]; then
  echo "--min-days-ahead must be a non-negative integer." >&2
  exit 2
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found: $PYTHON_BIN" >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "git not found in PATH." >&2
  exit 1
fi

REPO_DIR="$(cd "$REPO_DIR" && pwd)"
cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository: $REPO_DIR" >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree is dirty. Aborting to avoid mixing unrelated changes." >&2
  exit 1
fi

echo "[1/6] Fetch + fast-forward branch"
git fetch "$REMOTE" "$BRANCH"
git checkout "$BRANCH"
git pull --ff-only "$REMOTE" "$BRANCH"

echo "[2/6] Generate prayer JSON"
"$PYTHON_BIN" generate_prayer_data.py

echo "[3/6] Generate HTML pages"
"$PYTHON_BIN" generate_html.py

echo "[4/6] Validate generated output"
"$PYTHON_BIN" scripts/validate_generated_site.py \
  --repo-dir "$REPO_DIR" \
  --min-days-ahead "$MIN_DAYS_AHEAD"

echo "[5/6] Stage generated artifacts"
git add -A data en zh ta ar *.html

if git diff --cached --quiet; then
  echo "No generated changes to commit."
  exit 0
fi

if [[ "$DRY_RUN" == "1" ]]; then
  echo "Dry run enabled. Skipping commit and push."
  git reset
  exit 0
fi

AUTHOR_NAME="${GIT_AUTHOR_NAME:-$(git config user.name || true)}"
AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-$(git config user.email || true)}"

if [[ -z "$AUTHOR_NAME" || -z "$AUTHOR_EMAIL" ]]; then
  echo "Missing Git identity. Set GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL, or git config user.name/user.email." >&2
  exit 1
fi

TS_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
COMMIT_MSG="chore(data): refresh generated prayer data and static pages (${TS_UTC})"

echo "[6/6] Commit + push updates"
git -c user.name="$AUTHOR_NAME" -c user.email="$AUTHOR_EMAIL" commit -m "$COMMIT_MSG"
git push "$REMOTE" "HEAD:$BRANCH"

echo "Refresh pipeline completed successfully."
