import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Support Render Postgres: if DATABASE_URL is set (postgres://), use it.
# Render provides postgres:// which needs to be converted to postgresql:// for SQLAlchemy
def get_database_uri():
    uri = os.environ.get('DATABASE_URL')
    if uri:
        # Render / Heroku postgres fix
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        return uri
    return f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'krishi.db')}"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'krushak-secret-2026-enterprise'
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
