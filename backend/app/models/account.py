from app.extensions import db
from datetime import datetime


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    account_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship("Transaction", backref="account", lazy=True)

    def __repr__(self):
        return f"<Account {self.id} ({self.account_type})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "balance": self.balance,
            "account_type": self.account_type,
            "created_at": self.created_at.isoformat()
        }
