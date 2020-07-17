import os

class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True