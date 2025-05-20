from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user_model import User
from app import db
from app.utils.jwt_helper import generate_token
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login to receive JWT token
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Token generated
    """

    @auth_bp.route('/login', methods=['POST', 'OPTIONS'])
    def login():
        try:
            data = request.get_json()
            print("Login attempt with data:", data)  # Debug log

            if not data or 'username' not in data or 'password' not in data:
                return jsonify({"msg": "Missing credentials"}), 400

            user = User.query.filter_by(username=data['username'], password=data['password']).first()

            if not user:
                return jsonify({"msg": "Invalid credentials"}), 401

            access_token = create_access_token(identity=user.username)

            return jsonify({
                "access_token": access_token,
                "username": user.username,
                "role": user.role
            }), 200

        except Exception as e:
            print("Login error:", str(e))
            return jsonify({"msg": "Internal server error"}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user (Customer)
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username, password=password, role="customer")
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201
