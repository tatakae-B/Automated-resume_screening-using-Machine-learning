#!/bin/bash
set -e
echo "Installing Python dependencies with pip..."
pip install --no-cache-dir Flask==3.0.0 numpy==1.24.3 pdfplumber==0.9.0 Werkzeug==3.0.0
echo "Build complete!"
