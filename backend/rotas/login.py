from flask import Blueprint, jsonify, request, make_response
from backend.modelo.usuario import Usuario
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    # Pegando os valores com `.get()` para evitar erro caso estejam ausentes
    email = data.get("email", "").strip()
    senha = data.get("senha", "").strip()

    if not email or not senha:
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    # Buscar usuário no banco
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.senha, senha):
        return jsonify({"error": "Usuário ou senha inválidos."}), 401

    return jsonify({
        "usuario": {
            "email": usuario.email
        },
        "redirect": "/api/reservas"
    }), 200