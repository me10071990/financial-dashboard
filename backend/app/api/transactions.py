from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Transaction, Account
from datetime import datetime
from sqlalchemy import desc, asc, func

transactions_bp = Blueprint("transactions_bp", __name__)


# -----------------------
# ✅ 1. Create transaction @jwt_required(): Ensures only logged-in users can make transactions.
# -----------------------
@transactions_bp.route("/", methods=["POST"])
@jwt_required()
def create_transaction():

    #Reads JSON body from the request.
    #Fetches the current logged-in user's ID from the JWT token.

    data = request.get_json()
    user_id = get_jwt_identity()

    #Extract transaction details
    account_id = data.get("account_id")
    amount = data.get("amount")
    transaction_type = data.get("transaction_type")
    description = data.get("description", "")
    
    #Validate input
    if not all([account_id, amount, transaction_type]):
        return jsonify({"message": "Missing required fields"}), 400
    
    #Fetch the user’s account
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    #Validate funds for withdrawals

    if transaction_type == "withdraw" and account.balance < amount:
        return jsonify({"message": "Insufficient funds"}), 400

    #Update balance

    if transaction_type == "deposit":
        account.balance += amount
    elif transaction_type == "withdraw":
        account.balance -= amount

    #Save the transaction
    transaction = Transaction(
    account_id=account.id,
    amount=float(amount),  # ensure it's a number
    transaction_type=transaction_type,
    description=description,
    created_at=datetime.utcnow(),  # always datetime
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
    "message": f"{transaction_type.capitalize()} successful",
    "transaction": {
        "id": transaction.id,
        "account_id": transaction.account_id,
        "amount": transaction.amount,
        "type": transaction.transaction_type,
        "description": transaction.description,
        "created_at": transaction.created_at.isoformat()  # convert to string
    },
    "balance": account.balance  # return updated balance
    }), 201


# -----------------------
# ✅ 2. Get transaction history (with sorting)
# -----------------------
@transactions_bp.route("/", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    account_id = request.args.get("account_id", type=int)
    txn_type = request.args.get("type")
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 10, type=int)

    query = Transaction.query.join(Account).filter(Account.user_id == user_id)

    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    if txn_type in ["deposit", "withdraw"]:
        query = query.filter(Transaction.transaction_type == txn_type)

    # Sorting logic
    sort_column = getattr(Transaction, sort_by, Transaction.created_at)
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    transactions = [
        {
            "id": txn.id,
            "account_id": txn.account_id,
            "amount": txn.amount,
            "type": txn.transaction_type,
            "description": txn.description,
            "created_at": txn.created_at.isoformat(),
        }
        for txn in pagination.items
    ]

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "transactions": transactions
    }), 200


# -----------------------
# ✅ 3. Summary endpoint
# -----------------------
@transactions_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_summary():
    user_id = get_jwt_identity()

    # Aggregate totals for user
    total_deposits = db.session.query(func.sum(Transaction.amount))\
        .join(Account)\
        .filter(Account.user_id == user_id, Transaction.transaction_type == "deposit")\
        .scalar() or 0

    total_withdrawals = db.session.query(func.sum(Transaction.amount))\
        .join(Account)\
        .filter(Account.user_id == user_id, Transaction.transaction_type == "withdraw")\
        .scalar() or 0

    balance = total_deposits - total_withdrawals

    return jsonify({
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "current_balance": balance
    }), 200
