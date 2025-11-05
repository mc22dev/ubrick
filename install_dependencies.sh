#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Check if the virtual environment directory exists.
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r breakout/requirements.txt

echo "Installation complete. The virtual environment is ready."
echo "To activate it in your shell, run: source .venv/bin/activate"
