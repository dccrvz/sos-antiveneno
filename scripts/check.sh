#!/usr/bin/env bash
# Pre-deploy check. Runs locally (./scripts/check.sh) and in CI (.github/workflows/check.yml).
# It must pass before every deploy. Edit the PROJECT CHECKS section for this project.
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "✗ $*" >&2; exit 1; }
ok()   { echo "✓ $*"; }

# 1. No secret files or obvious secret values tracked by git.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  tracked_env=$(git ls-files | grep -E '(^|/)\.env(\.[^/]*)?$' | grep -vE '\.env\.example$' || true)
  [ -z "$tracked_env" ] || fail "secret file tracked by git: $tracked_env (git rm --cached it, rotate the values)"
  pattern='-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|sk_live_[0-9A-Za-z]{10,}|sk-(ant-|proj-)?[A-Za-z0-9_-]{30,}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}|xox[baprs]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}'
  hits=$(git grep -nIE -e "$pattern" -- . ':(exclude)scripts/check.sh' ':(exclude)*.example' || true)
  [ -z "$hits" ] || { echo "$hits" | cut -c1-120 >&2; fail "possible secret in tracked files (move it to the vault, rotate it)"; }
  ok "no secrets tracked"
fi

# 2. PROJECT CHECKS (SoroJá). Mirrors .github/workflows/ci.yml; keep the two in sync.
#    Static app: there is no build step. Vercel serves app/ as-is.
PY=${PYTHON:-python3}
$PY -c "import pytest" 2>/dev/null || $PY -m pip install -q pytest
$PY scripts/canonicalize_antivenoms.py --self-test >/dev/null
ok "canonicalizer self-test"
$PY -m pytest -q scripts/tests/
ok "pytest suite (includes security config tests)"
$PY scripts/validate_community_notes.py
$PY scripts/validate_location_overrides.py
$PY scripts/apply_official_state_corrections.py --check
$PY scripts/rebuild_final_artifacts.py --check
$PY scripts/build_app_hospitals_json.py
git diff --quiet -- app/hospitals.json hospitals.json \
  || fail "app/hospitals.json is stale: commit the output of scripts/build_app_hospitals_json.py"
$PY scripts/validate_hospitals_json.py app/hospitals.json
ok "dataset validation"
if [ "${SKIP_FORMAT:-0}" != 1 ]; then
  [ -d node_modules/prettier ] || npm ci --silent
  # Tracked files only (CI sees nothing else); .prettierignore still applies.
  git ls-files -z -- '*.json' '*.md' '*.yml' '*.yaml' | xargs -0 npx --no-install prettier --check --log-level warn
  ok "prettier format check"
fi
ok "check passed"
