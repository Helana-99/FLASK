import os

class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    WTF_CSRF_ENABLED = True
    UPLOADED_IMAGES_DEST = os.path.join(os.getcwd(), 'static', 'uploads')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://helana:1993@localhost:5432/f_demo'
    UPLOADED_PHOTOS_DEST = 'app/static/'

config_options = {
    "dev": DevelopmentConfig,
    "prd": ProductionConfig
}
