import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "VerySecretKey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Development DB from env variable
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:example@localhost:5432/alerts-db"
    )


class ProductionConfig(Config):
    DEBUG = False
    # Default option for retrieving DB URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    # Separate database for testing
    # Prefer TEST_DATABASE_URL (for CI or Postgres-based tests). If not set,
    # fall back to a fast in-memory SQLite database so tests run locally
    # without requiring Postgres.
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL") or "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "127.0.0.1:5000"


# class TestingConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
#     WTF_CSRF_ENABLED = False
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SERVER_NAME = "127.0.0.1:5000"
