"""Flask configuration"""
from pathlib import Path

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent

class Config:
    """Base config."""

    SECRET_KEY = 'SlHiRsP7wa4teLLGw1FwXQ'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        PROJECT_ROOT.joinpath("data", "cycling.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class ProdConfig(Config):
    """Production config not currently implemented."""

    pass

class DevConfig(Config):
    """Development config"""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True

class TestConfig(Config):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False
    # SERVER_NAME = "127.0.0.1:5000"