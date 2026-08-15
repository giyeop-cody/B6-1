#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="b6-1-web:local"
CONTAINER_NAME="b6-1-web-local"
PORT="${B6_LOCAL_PORT:-8080}"

if ! command -v docker >/dev/null 2>&1; then
  echo "FAIL: Docker가 설치되어 있지 않습니다." >&2
  echo "Docker Desktop 또는 Docker Engine 설치 후 다시 실행하세요." >&2
  exit 2
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "FAIL: curl이 필요합니다." >&2
  exit 2
fi

cleanup() {
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup

echo "[1/4] Docker image build"
docker build -t "$IMAGE_NAME" .

echo "[2/4] Container start: http://localhost:${PORT}"
docker run -d --name "$CONTAINER_NAME" -p "${PORT}:80" "$IMAGE_NAME" >/dev/null

for _ in $(seq 1 20); do
  if curl -fsS "http://127.0.0.1:${PORT}/health" >/tmp/b6-1-health.txt 2>/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/4] HTTP response check"
test "$(tr -d '\r\n' </tmp/b6-1-health.txt)" = "OK"
curl -fsS "http://127.0.0.1:${PORT}/" | grep -q "인터넷에서"

echo "[4/4] Docker health check"
for _ in $(seq 1 20); do
  status="$(docker inspect --format '{{.State.Health.Status}}' "$CONTAINER_NAME")"
  [ "$status" = "healthy" ] && break
  sleep 1
done
[ "${status:-}" = "healthy" ]

printf '%s\n' "LOCAL DOCKER TEST: ALL PASS" "health=http://127.0.0.1:${PORT}/health" "container_status=${status}"
