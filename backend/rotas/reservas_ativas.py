from flask import Blueprint, jsonify
from flask_cors import CORS

reservas_ativas_bp = Blueprint("reservas_ativas", __name__)
CORS(reservas_ativas_bp)

# Mock de usuários 
mock_usuarios = [
    {
        "id": 1,
        "nome": "Professor Teste",
        "email": "professor@email.com",
        "cpf": "123.456.789-00",
        "professor": "S",
        "siape": "123456"
    }
]

# Mock de reservas
mock_reservas = [
    {
        "id": 1,
        "sala_id": 1,
        "professor_id": 1,
        "data": "2025-04-02",
        "start_time": "14:00",
        "end_time": "16:00",
        "status": "ativa",
        "sala": {
            "nome": "Sala E001",
            "tipo": "Laboratório"
        }
    }
]

@reservas_ativas_bp.route("/api/reservas/ativas", methods=["GET", "POST"]) 
def get_reservas_ativas():
    print("Rota /api/reservas/ativas foi acessada!")
    
    usuario = mock_usuarios[0]
    
    reservas_ativas = [r for r in mock_reservas if r["professor_id"] == usuario["id"] and r["status"] == "ativa"]

    if not reservas_ativas:
        return jsonify({"message": "Não há reservas ativas para este usuário"}), 200

    return jsonify(reservas_ativas), 200

@reservas_ativas_bp.route("/api/reservas/ativas/<int:reserva_id>", methods=["DELETE"])
def excluir_reserva_ativa(reserva_id):
    print(f"Rota DELETE /api/reservas/ativas/{reserva_id} foi acessada!")

    reserva = next((r for r in mock_reservas if r["id"] == reserva_id and r["status"] == "ativa"), None)

    if not reserva:
        return jsonify({"error": "Reserva ativa não encontrada"}), 404

    reserva["status"] = "inativa"

    return jsonify({
        "message": "Reserva cancelada com sucesso",
        "reserva": reserva
    }), 200