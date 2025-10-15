from flask import Flask
from .config import config_by_name
from .extensions import db, migrate, jwt, cors
from app.models import User, Account, Transaction  # Models imported once for migrations
import redis


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Initialize Redis client
    app.redis = redis.from_url(app.config["REDIS_URL"])

    # Register blueprints
    from .api import auth_bp, accounts_bp, transactions_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

    return app
