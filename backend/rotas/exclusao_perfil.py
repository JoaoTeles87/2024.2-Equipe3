from flask import Blueprint, jsonify, request
from flask_cors import CORS

exclusao_perfil_bp = Blueprint("exclusao_perfil", __name__)
CORS(exclusao_perfil_bp)

# Mock de usuários
mock_usuarios = [
    {
        "id": 1,
        "nome": "Professor Teste",
        "email": "professor@email.com",
        "cpf": "123.456.789-00",
        "professor": "S",
        "siape": "123456",
        "senha": "123456"
    }
]

# Mock de reservas
mock_reservas = [
    {
        "id": 1,
        "usuario_id": 1,
        "sala_id": 1,
        "data": "2024-03-20",
        "start_time": "14:00",
        "end_time": "16:00",
        "status": "inativa"  
    }
]

@exclusao_perfil_bp.route("/api/perfil", methods=["DELETE"])
def excluir_perfil():
    try:
        dados = request.get_json()
        user_id = dados.get("id")
        senha = dados.get("senha")

        if not user_id or not senha:
            return jsonify({"error": "O campo 'senha' é obrigatório."}), 400

        # Busca usuário
        usuario = next((u for u in mock_usuarios if u["id"] == user_id), None)
        if not usuario:
            return jsonify({"error": "Perfil não encontrado"}), 404

        # Verifica senha
        if senha != usuario["senha"]:
            return jsonify({"error": "Senha incorreta"}), 401

        # Verifica reservas ativas
        reservas_ativas = [r for r in mock_reservas 
                         if r["usuario_id"] == user_id 
                         and r["status"] == "ativa"]
        
        if reservas_ativas:
            return jsonify({
                "error": "Não é possível excluir o perfil com reservas ativas. Cancele todas as reservas primeiro."
            }), 400

        # Remove usuário
        mock_usuarios.remove(usuario)
        return jsonify({"message": "Perfil excluído com sucesso!"}), 200

    except Exception as e:
        print(f"Erro ao excluir perfil: {str(e)}")
        return jsonify({"error": "Erro interno ao processar a requisição"}), 500