from flask import Blueprint, jsonify, request
from flask_cors import CORS

perfil_bp = Blueprint("perfil", __name__)
CORS(perfil_bp)

usuario = {
    "id": 1,
    "email": "teste@email.com",
    "nome": "esse caralho Teste",
    "cpf": "000.000.000-00",
    "professor": "S",
    "siape": "123456"
}

@perfil_bp.route("/api/perfil", methods=["GET"])  # Alterado para GET
def obter_perfil():
    return jsonify(usuario), 200