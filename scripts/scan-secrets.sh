#!/usr/bin/env bash
set -euo pipefail

fail=0

while IFS= read -r path; do
  case "$path" in
    *.pem|*.ppk|*.key|.env|.env.*|*/.aws/*)
      if [[ "$path" != ".env.example" ]]; then
        echo "FAIL: 추적하면 안 되는 파일: $path" >&2
        fail=1
      fi
      ;;
  esac
done < <(git ls-files)

scan() {
  local label="$1"
  local pattern="$2"
  if git grep -nE "$pattern" -- . ':!scripts/scan-secrets.sh' >/tmp/b6-1-secret-scan.txt 2>/dev/null; then
    echo "FAIL: ${label} 형태 문자열 발견" >&2
    cat /tmp/b6-1-secret-scan.txt >&2
    fail=1
  fi
}

scan "AWS Access Key ID" 'AKIA[0-9A-Z]{16}'
scan "Private key" 'BEGIN ([A-Z]+ )?PRIVATE KEY'
scan "AWS secret 설정" 'aws_secret_access_key[[:space:]]*='
scan "평문 Authorization" 'Authorization:[[:space:]]*Bearer[[:space:]]+[A-Za-z0-9._-]{20,}'

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "SECRET SCAN: PASS"
