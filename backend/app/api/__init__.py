from .auth import auth_bp
from .accounts import accounts_bp
from .transactions import transactions_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")