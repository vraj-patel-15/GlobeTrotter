import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "..", ".env"))


class Config:
    """Base Configuration Class."""

    # Secret Key for signing cookies and session security
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # PostgreSQL Database Configuration
    # Falls back to local SQLite if DATABASE_URL is not set
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, '..', 'app.db')}"
    )

    # Adjust PostgreSQL URI prefix for SQLAlchemy compatibility if coming from Heroku/Render
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    # Disable SQLAlchemy event system modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration (for user avatars or trip cover photos)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    UPLOAD_FOLDER = os.path.join(basedir, "static", "images", "uploads")

    # Session & Security Settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    """Development Environment Configuration."""

    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Testing Environment Configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Environment Configuration."""

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Enforce HTTPS cookies in production


# Dictionary mapping environments to configuration classes
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}