import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "replace_me_with_random_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "replace_me_jwt_secret")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:aitest123@localhost:5432/fin_db_dev"
    )
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/fin_db_prod"
    )

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
