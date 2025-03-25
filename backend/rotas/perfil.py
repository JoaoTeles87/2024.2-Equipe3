from flask import Blueprint, jsonify
from flask_cors import CORS

perfil_bp = Blueprint("perfil", __name__)
CORS(perfil_bp)

# Mock do perfil do usuário
mock_usuario = {
    "id": 1,
    "nome": "Professor Teste",
    "email": "teste@email.com",
    "cpf": "123.456.789-00",
    "professor": "S",
    "siape": "123456"
}

@perfil_bp.route("/api/perfil", methods=["POST"])
def obter_perfil():
    return jsonify(mock_usuario), 200