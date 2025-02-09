from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

protegida_bp = Blueprint("protegida", __name__)

@protegida_bp.route("/api/area_restrita", methods=["GET"])
@jwt_required()
def area_restrita():
    user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    mensagem = {"message": f"Acesso permitido para o usuário {str(user_id)}"}

    # 🔥 Usando `json.dumps(..., ensure_ascii=False)` para evitar Unicode
    response = make_response(json.dumps(mensagem, ensure_ascii=False), 200)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    
    return response
