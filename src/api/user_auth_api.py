from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from src.core.models.user import User
from src.core.extensions.sql_alchemy_extension import db


user_auth_apis = Blueprint("auth_api", __name__, url_prefix="/api")


@user_auth_apis.route("/register", methods = ["POST"])
def register():
    """Register the User
    """
    data = request.get_json()
    username=data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exist!!"}), 400

    hash_pass = generate_password_hash(password)
    user = User(username=username, password=hash_pass)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@user_auth_apis.route("/login", methods=["POST"])
def login():
    """Login the user
    """
    data = request.get_json()
    username=data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid Credentils"}), 401

    access_token = create_access_token(username)
    return jsonify({"access_token": access_token})


@user_auth_apis.route("/data", methods=["GET"])
@jwt_required()
def get_user_data():
    """Retrieves a test data
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"Dear {current_user}, you have accessed a secure route."})
