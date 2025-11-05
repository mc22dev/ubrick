#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Activate the virtual environment.
echo "Activating virtual environment..."
source .venv/bin/activate

# Run the game.
echo "Starting the game..."
python breakout/main.py
