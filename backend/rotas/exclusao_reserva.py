from flask import Flask, Blueprint, jsonify, request

# Simulação de dados do usuário autenticado
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "id": 1
}

# Simulação de reservas (dados estáticos)
reservas = [
    {"id": 1, "usuario_id": 1, "detalhes": "Reserva de teste 1"},
    {"id": 2, "usuario_id": 1, "detalhes": "Reserva de teste 2"}
]

# Blueprint para exclusão de reserva
exclusao_reserva_bp = Blueprint("exclusao_reserva", __name__)

@exclusao_reserva_bp.route("/api/reservas/<int:reserva_id>", methods=["DELETE"])
def excluir_reserva(reserva_id):
    # Verifica se a reserva existe para o usuário
    reserva = next((r for r in reservas if r["id"] == reserva_id and r["usuario_id"] == usuario["id"]), None)
    
    if not reserva:
        return jsonify({"error": "Reserva não encontrada."}), 404
    
    try:
        reservas.remove(reserva)  
        return jsonify({"message": "Reserva excluída com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir a reserva. Tente novamente. {str(e)}"}), 500

# Função para criar a aplicação e registrar o blueprint
def create_app():
    app = Flask(__name__)
    app.register_blueprint(exclusao_reserva_bp) 
    return app
