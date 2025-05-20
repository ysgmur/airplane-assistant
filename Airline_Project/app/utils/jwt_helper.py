from flask_jwt_extended import create_access_token, get_jwt
from flask import jsonify

def generate_token(identity: str, role: str) -> str:
    return create_access_token(
        identity=identity,
        additional_claims={"role": role}
    )

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"msg": "Admin privilege required"}), 403
