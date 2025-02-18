from flask import Blueprint, jsonify

# Simulação de dados do usuário
usuario = {
    "email": "teste@email.com",
    "nome": "esse caralho Teste",
    "cpf": "000.000.000-00",
    "professor": "S",
    "siape": "123456"
}

perfil_bp = Blueprint("perfil", __name__)

@perfil_bp.route("/api/perfil", methods=["POST"])
def obter_perfil():
    # Simulando a autenticação do usuário
    if usuario["email"] != "teste@email.com":
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    perfil_data = {
        "nome": usuario["nome"],
        "cpf": usuario["cpf"],
        "email": usuario["email"]
    }
    
    # Se o usuário for professor, adicionar o campo siape
    if usuario["professor"] == "S":
        perfil_data["siape"] = usuario["siape"]
    
    return jsonify(perfil_data), 200
