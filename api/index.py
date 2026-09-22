# Vercel serverless entry for Flask - Krushak
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import app

# Vercel expects `app` or `handler`
# Flask app is already configured with SQLite / Postgres via config.py
# No extra code needed - Vercel will call app
