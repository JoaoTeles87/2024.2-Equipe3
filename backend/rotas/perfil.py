from flask import Blueprint, jsonify
from flask_cors import CORS

perfil_bp = Blueprint("perfil", __name__)
CORS(perfil_bp, resources={r"/api/*": {"origins": "*"}})

# Mock de usuários
mock_usuarios = [
    {
        "id": 1,
        "nome": "Osvaldo Albuquerque", 
        "email": "osvAl@gmail.com",
        "cpf": "123.456.789-00",
        "professor": "S",
        "siape": "1594506"
    }
]

@perfil_bp.route("/api/perfil", methods=["GET"])  
def obter_perfil():
    print("Rota GET /api/perfil foi acessada!")
    
    try:
        usuario = mock_usuarios[0]  
        
        perfil = {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "cpf": usuario["cpf"],
            "professor": usuario["professor"],
            "siape": usuario.get("siape")
        }
        
        return jsonify(perfil), 200
        
    except Exception as e:
        print(f"Erro ao obter perfil: {str(e)}")
        return jsonify({"error": "Erro interno ao buscar perfil"}), 500