"""
Configuration file for Flask app
"""
import os

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    MODEL_PATH = "model.pkl"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CORS_ORIGINS = ["*"]  # Allow all origins in development

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    CORS_ORIGINS = ["*"]

# Get config from environment
config_name = os.getenv("FLASK_ENV", "development")
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
CONFIG = config_dict.get(config_name, DevelopmentConfig)
