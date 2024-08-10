import os

class Config:
    # Flask settings
    # SECRET_KEY = os.environ.get('SQLlite_KEY')
    DEBUG = False
    TESTING = False

    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///disaster_response.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_disaster_response.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production_disaster_response.db'