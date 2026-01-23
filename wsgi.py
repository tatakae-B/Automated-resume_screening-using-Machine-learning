"""WSGI entrypoint for Vercel"""
import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.index import app

# Export app for Vercel
if __name__ == '__main__':
    app.run()

