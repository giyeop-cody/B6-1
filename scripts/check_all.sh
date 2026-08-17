#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 scripts/validate_project.py
for script in scripts/*.sh; do
  bash -n "$script"
done
echo "SHELL SYNTAX: PASS"

scripts/scan-secrets.sh
git diff --check
echo "GIT DIFF CHECK: PASS"

if [[ "${1:-}" == "--with-docker" ]]; then
  scripts/test-local.sh
elif command -v docker >/dev/null 2>&1; then
  echo "Docker가 발견됐지만 기본 정적 검사에서는 실행하지 않습니다."
  echo "실제 검사: scripts/check_all.sh --with-docker"
else
  echo "LOCAL DOCKER TEST: SKIP (Docker not installed)"
fi

echo "B6-1 STATIC CHECKS: ALL PASS"
