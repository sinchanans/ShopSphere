from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

from app.extensions import bcrypt, db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# -------------------------------
# Register User
# -------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data"}), 400

    required_fields = ["first_name", "last_name", "email", "password"]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field} is required"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=hashed_password,
        role="customer",
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201


# -------------------------------
# Login User
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "email": user.email,
            "role": user.role,
        },
        expires_delta=timedelta(hours=2),
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
    }), 200


# -------------------------------
# Logged-in User Profile
# -------------------------------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
    }), 200