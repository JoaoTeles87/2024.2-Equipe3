from flask import Blueprint, jsonify, request, make_response
from backend.modelo.usuario import Usuario
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("Email")
    senha = data.get("Senha")

    if not email or not senha:
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    user = Usuario.query.filter(Usuario.email==email).first()
    if not user or not check_password_hash(user.senha, senha):
        return jsonify({"error": "Usuário ou senha inválidos."}), 401
    

    return user, 200
