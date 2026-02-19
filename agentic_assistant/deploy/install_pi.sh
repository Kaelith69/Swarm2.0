#!/usr/bin/env bash
set -euo pipefail

APP_DIR=/opt/agentic-assistant
LLAMA_DIR=/home/ubuntu/llama.cpp

sudo apt update
sudo apt install -y python3 python3-pip python3-venv git build-essential cmake nginx

if [ ! -d "$APP_DIR" ]; then
  sudo mkdir -p "$APP_DIR"
  sudo chown -R "$USER":"$USER" "$APP_DIR"
fi

python3 -m venv "$APP_DIR/.venv"
source "$APP_DIR/.venv/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

if [ ! -d "$LLAMA_DIR" ]; then
  git clone https://github.com/ggerganov/llama.cpp "$LLAMA_DIR"
fi

cmake -S "$LLAMA_DIR" -B "$LLAMA_DIR/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$LLAMA_DIR/build" --config Release -j4

echo "Install complete. Copy .env.example to .env and set local + cloud API keys (Groq/Gemini/Kimi) and messaging tokens."
