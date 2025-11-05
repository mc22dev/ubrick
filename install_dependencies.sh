#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Remove the existing virtual environment if it exists.
if [ -d ".venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf .venv
fi

# Create a new virtual environment.
echo "Creating virtual environment..."
python3 -m venv .venv

echo "Installing dependencies..."
.venv/bin/pip install -r breakout/requirements.txt

echo "Installation complete."
