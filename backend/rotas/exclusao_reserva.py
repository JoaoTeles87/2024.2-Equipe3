from flask import Blueprint, jsonify

# Simulação de dados do usuário autenticado
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "id": 1  # Simulando ID do usuário
}

# Simulação de reservas (dados estáticos)
reservas = [
    {"id": 1, "usuario_id": 1, "detalhes": "Reserva de teste 1"},
    {"id": 2, "usuario_id": 1, "detalhes": "Reserva de teste 2"}
]

exclusao_reserva_bp = Blueprint("exclusao_reserva", __name__)

@exclusao_reserva_bp.route("/api/reservas/<int:reserva_id>", methods=["DELETE"])
def excluir_reserva(reserva_id):
    # Simulando que o usuário está autenticado
    if usuario["email"] != "teste@email.com":
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    # Encontrar a reserva pelo ID e usuário
    reserva = next((r for r in reservas if r["id"] == reserva_id and r["usuario_id"] == usuario["id"]), None)
    
    if not reserva:
        return jsonify({"error": "Reserva não encontrada."}), 404

    try:
        # Simula a exclusão da reserva
        reservas.remove(reserva)
        return jsonify({"message": "Reserva excluída com sucesso!"}), 200
    except:
        return jsonify({"error": "Erro ao excluir a reserva. Tente novamente."}), 500
