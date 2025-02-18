from flask import Blueprint, jsonify
from flask_jwt_extended import unset_jwt_cookies

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logout realizado com sucesso."})
    unset_jwt_cookies(response)  # Remove o cookie do JWT
    return response, 200
