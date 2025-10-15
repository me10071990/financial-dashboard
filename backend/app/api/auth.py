from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token
from sqlalchemy import or_
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("username") or data.get("email")
    password = data.get("password")

    user = User.query.filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200