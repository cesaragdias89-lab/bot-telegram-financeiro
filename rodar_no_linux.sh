#!/usr/bin/env bash
set -e
# === Preparar ambiente e rodar o bot no Telegram ===
cd "$(dirname "$0")"
python3 -m venv .venv || python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
if [ ! -f ".env" ]; then
  echo "Copie .env.example para .env e edite seu TELEGRAM_TOKEN."
  exit 1
fi
python main.py telegram
