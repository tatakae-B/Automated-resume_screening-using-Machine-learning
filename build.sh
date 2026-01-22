#!/bin/bash
set -e
echo "Installing Python dependencies with pip..."
pip install --no-cache-dir -r requirements.txt
echo "Build complete!"
