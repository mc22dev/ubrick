#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Run the game using the virtual environment's Python interpreter.
echo "Starting the game..."
.venv/bin/python breakout/main.py
