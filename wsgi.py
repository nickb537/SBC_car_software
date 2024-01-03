# wsgi.py
from flask_app import app  # Import your Flask app instance

application = app  # Rename it to 'application' (Gunicorn/uWSGI expects this)

