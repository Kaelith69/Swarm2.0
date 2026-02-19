#!/usr/bin/env bash
set -euo pipefail

APP_DIR=${APP_DIR:-/opt/agentic-assistant}
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8000}

cd "$APP_DIR"

if [ ! -f ".env" ]; then
  echo "[ERROR] .env not found at $APP_DIR/.env"
  exit 1
fi

if [ ! -f ".venv/bin/activate" ]; then
  echo "[ERROR] Python venv not found at $APP_DIR/.venv"
  exit 1
fi

source .venv/bin/activate
export PYTHONPATH="$APP_DIR/src"

python -m assistant.agent >/tmp/agentic-assistant.log 2>&1 &
SERVER_PID=$!
cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[INFO] Waiting for API startup..."
READY=0
for _ in $(seq 1 30); do
  if curl -fsS "http://${HOST}:${PORT}/health" >/tmp/agentic-health.json; then
    READY=1
    break
  fi
  sleep 1
done

if [ "$READY" -ne 1 ]; then
  echo "[ERROR] API did not become healthy. Last logs:"
  tail -n 80 /tmp/agentic-assistant.log || true
  exit 1
fi

echo "[OK] /health"
cat /tmp/agentic-health.json

echo "[INFO] Running /query smoke test..."
if ! curl -fsS -X POST "http://${HOST}:${PORT}/query" \
  -H "Content-Type: application/json" \
  -d '{"message":"Who is Sayanth?"}' >/tmp/agentic-query.json; then
  echo "[ERROR] /query failed. Last logs:"
  tail -n 120 /tmp/agentic-assistant.log || true
  exit 1
fi

echo "[OK] /query"
cat /tmp/agentic-query.json

echo "[DONE] Launch + checks completed successfully."
