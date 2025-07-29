from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_refresh_token, jwt_required, create_access_token, get_jwt_identity,
    decode_token, get_jwt)

from src.core.models.user import User
from src.core.extensions import db, jwt, limiter


user_auth_apis = Blueprint("auth_api", __name__, url_prefix="/api")


revoked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Check for token revoked
    """
    jti = jwt_payload["jti"]
    return jti in revoked_tokens


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
@limiter.limit("5 per minute")  # Allow max 5 attempts per minute per IP
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
    refresh_token = create_refresh_token(username)
    response = jsonify(
        {
            "access_token": access_token,
        }
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite='Strict'
    )
    return response


# @user_auth_apis.route("/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh():
#     """refresh the access token
#     Token Refresh Flow:
#         1. User logs in → gets both access_token and refresh_token
#         2. After access_token expires, the client sends the refresh_token to /refresh
#         3. If the refresh token is valid → the server sends a new access_token
#     """
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     return jsonify({"access_token": access_token})

@user_auth_apis.route("/refresh", methods=["POST"])
def refresh():
    """Refresh token
    """
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return jsonify({"message": "No refresh token found"}), 401

    try:
        decoded = decode_token(refresh_token, allow_expired=False)
        username = decoded['sub']
    except Exception:
        return jsonify({"message": "Invalid or expired token"}), 401

    new_access_token = create_access_token(identity=username)
    return jsonify({"access_token": new_access_token})


@user_auth_apis.route("/data", methods=["GET"])
@jwt_required()
def get_user_data():
    """Retrieves a test data
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"Dear {current_user}, you have accessed a secure route."})


@user_auth_apis.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change Password
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    user = User.query.filter_by(username=current_user).first()
    if not user or not check_password_hash(user.password, old_password):
        return jsonify({"message": "Old password is incorrect"}), 403

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password changed successfully"})


@user_auth_apis.route('/reset-password-token', methods=['POST'])
def request_reset_token():
    """Requests reset token
    """
    data = request.get_json()
    username = data.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    reset_token = create_access_token(identity=username, expires_delta=False)
    return jsonify({
        "reset_token": reset_token,
        "message": "Use this token to reset password."
    })


@user_auth_apis.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    """Reset password
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    new_password = data.get('new_password')

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password has been reset successfully"})


@user_auth_apis.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout
    """
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)

    response = jsonify({"message": "Logged out"})
    response.delete_cookie("refresh_token")
    return response
