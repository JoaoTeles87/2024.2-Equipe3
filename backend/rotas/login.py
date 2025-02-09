from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
import datetime
from modelo.usuario import Usuario
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    user = Usuario.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.senha, senha):
        return jsonify({"error": "Usuário ou senha inválidos."}), 401

    # Criar um token JWT com expiração de 1 hora
    expires = datetime.timedelta(hours=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)

    # Criar a resposta JSON
    response = jsonify({"message": "Login bem-sucedido!", "user": user.email})

    # 🚀 Definir o JWT no Cookie
    set_access_cookies(response, access_token)

    # 🚀 Imprimir os cookies da resposta no terminal
    print(f"🚀 Token JWT gerado: {access_token}")
    print(f"🚀 Cabeçalhos da resposta: {response.headers}")

    return response, 200
