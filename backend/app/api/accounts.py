from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.models import Account

accounts_bp = Blueprint("accounts_bp", __name__)

@accounts_bp.route("/", methods=["GET"])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in accounts])

@accounts_bp.route("/", methods=["POST"])
@jwt_required()
def create_account():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    account = Account(
        user_id=current_user_id,
        account_type=data.get("account_type"),
        balance=data.get("balance", 0.0)
    )
    db.session.add(account)
    db.session.commit()
    return jsonify({"id": account.id, "account_type": account.account_type, "balance": account.balance}), 201
