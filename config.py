"""Application configuration settings"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ai_learning.db')
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    # Video Configuration
    VIDEO_FORMAT = os.getenv('VIDEO_FORMAT', 'mp4')
    VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', '1080p')
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', '30'))
    VIDEO_DURATION_MIN = int(os.getenv('VIDEO_DURATION_MIN', '5'))
    VIDEO_DURATION_MAX = int(os.getenv('VIDEO_DURATION_MAX', '30'))
    
    # Output Directories
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', './outputs')
    VIDEO_OUTPUT_DIR = os.getenv('VIDEO_OUTPUT_DIR', './outputs/videos')
    CONTENT_OUTPUT_DIR = os.getenv('CONTENT_OUTPUT_DIR', './outputs/content')
    
    # Text-to-Speech
    TTS_ENGINE = os.getenv('TTS_ENGINE', 'pyttsx3')
    TTS_VOICE_RATE = int(os.getenv('TTS_VOICE_RATE', '150'))
    TTS_VOICE_VOLUME = float(os.getenv('TTS_VOICE_VOLUME', '0.9'))
    
    # Caching
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_REFRESH_EACH_REQUEST = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
