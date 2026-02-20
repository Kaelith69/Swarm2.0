#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# install_pi.sh — bootstrap the agentic assistant on Raspberry Pi 5 (64-bit)
#
# Run as the 'pi' (or your user) user, NOT as root.  The script uses sudo only
# where required (apt, mkdir, chown).
#
# Usage:
#   cd /opt/agentic-assistant
#   bash deploy/install_pi.sh
# ---------------------------------------------------------------------------
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/agentic-assistant}"
LLAMA_DIR="${LLAMA_DIR:-/home/pi/llama.cpp}"
MODEL_DIR="${MODEL_DIR:-/home/pi/models}"
NPROC=$(nproc)   # use all cores for the cmake build

echo "==> [1/6] Installing system packages"
sudo apt-get update -q
sudo apt-get install -y \
  python3 python3-pip python3-venv python3-dev \
  git build-essential cmake \
  libopenblas-dev libffi-dev libssl-dev \
  nginx curl

echo "==> [2/6] Creating application directory"
if [ ! -d "$APP_DIR" ]; then
  sudo mkdir -p "$APP_DIR"
fi
sudo chown -R "$USER":"$USER" "$APP_DIR"

echo "==> [3/6] Creating model storage directory: $MODEL_DIR"
mkdir -p "$MODEL_DIR"

echo "==> [4/6] Setting up Python virtual environment"
python3 -m venv "$APP_DIR/.venv"
# shellcheck disable=SC1091
source "$APP_DIR/.venv/bin/activate"
pip install --upgrade pip --quiet
pip install -r "$APP_DIR/requirements.txt" --quiet
deactivate

echo "==> [5/6] Building llama.cpp"
if [ ! -d "$LLAMA_DIR" ]; then
  echo "     Cloning llama.cpp..."
  git clone --depth 1 https://github.com/ggerganov/llama.cpp "$LLAMA_DIR"
fi

cmake -S "$LLAMA_DIR" -B "$LLAMA_DIR/build" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_NATIVE=ON \
  -DLLAMA_CURL=OFF
cmake --build "$LLAMA_DIR/build" --config Release -j"$NPROC"

echo "==> [6/6] Verifying llama-cli binary"
LLAMA_CLI="$LLAMA_DIR/build/bin/llama-cli"
if [ ! -f "$LLAMA_CLI" ]; then
  echo "[ERROR] llama-cli not found at $LLAMA_CLI — build may have failed"
  exit 1
fi
echo "     llama-cli found: $LLAMA_CLI"
"$LLAMA_CLI" --version 2>/dev/null || true

echo ""
echo "==> Install complete!"
echo ""
echo "  Next steps:"
echo "  1. Download a quantized GGUF model to $MODEL_DIR/"
echo "     e.g. gemma-2-2b-it-Q4_K_M.gguf"
echo "  2. Copy .env.example to .env and set MODEL_PATH, LLAMA_MAIN_PATH,"
echo "     and optional API keys (Groq / Gemini / Kimi / Telegram / Discord)"
echo "  3. cp .env.example .env && chmod 600 .env"
echo "  4. Run: bash scripts/pi_start_and_check.sh"
echo "  5. (Optional) Enable systemd: sudo cp deploy/agent.service /etc/systemd/system/"
echo "                                sudo systemctl enable --now agent"
