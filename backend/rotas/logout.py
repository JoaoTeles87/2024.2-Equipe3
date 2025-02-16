from flask import Blueprint, jsonify

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logout realizado com sucesso."})
    return response, 200
