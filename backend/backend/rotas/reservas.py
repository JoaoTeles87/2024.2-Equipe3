from flask import Blueprint, request, jsonify
from modelo.reservas import mock_reservas
from datetime import datetime

reservas_bp = Blueprint('reservas', __name__)

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

# Get reservas
@reservas_bp.route('/api/reservas', methods=['GET'])
def get_reservas():
    return jsonify(mock_reservas), 200

# Get reservas para um usuário
@reservas_bp.route('/api/reservas/<int:professor_id>', methods=['GET'])
def get_reservas_professor(professor_id):
    user_reservas = [
        reserva for reserva in mock_reservas if reserva['professor_id'] == professor_id
    ]

    if not user_reservas:
        return jsonify({'mensagem': 'Nenhuma reserva encontrada'}), 404

    return jsonify(user_reservas), 200

# Create reserva
@reservas_bp.route('/api/reservas/<int:professor_id>', methods=['POST'])
def create_reserva(professor_id):
    """
    Exemplo de body
    {
        "sala_id": 3,
        "data": "2025-02-25",
        "start_time": "14:00",
        "end_time": "15:00"
    }
    """

    dados = request.get_json()
    sala_id = dados.get('sala_id')
    data = dados.get('data')
    start_time = dados.get('start_time')
    end_time = dados.get('end_time')
    status = "ativa"

    # Checa se o body inclui o que precisa
    if not sala_id or not data or not start_time or not end_time:
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

    parsed_start_time = parse_time(start_time)
    parsed_end_time = parse_time(end_time)

    for reserva in mock_reservas:
        if reserva['sala_id'] == sala_id and reserva['data'] == data and reserva['status'] == 'ativa':
            reserva_start = parse_time(reserva['start_time'])
            reserva_end = parse_time(reserva['end_time'])

            # Sobreposição de horários
            if not (reserva_end <= parsed_start_time or reserva_start >= parsed_end_time):
                return jsonify({'erro': 'Sala já reservada para esse horário'}), 409

    for reserva in mock_reservas:
        if reserva['professor_id'] == professor_id and reserva['data'] == data and reserva['status'] == 'ativa':
            professor_reserva_start = parse_time(reserva["start_time"])
            professor_reserva_end = parse_time(reserva["end_time"])

            if not (professor_reserva_end <= parsed_start_time or professor_reserva_start >= parsed_end_time):
                return jsonify({"erro": "Professor já possui uma reserva nesse horário"}), 409

    new_reserva = {
        "id": len(mock_reservas) + 1,
        "sala_id": sala_id,
        "professor_id": professor_id,
        "data": data,
        "start_time": start_time,
        "end_time": end_time,
        "status": status
    }
    mock_reservas.append(new_reserva)

    return jsonify({"mensagem": "Reserva criada com sucesso!", "reservation": new_reserva}), 201


# Cancela reserva
@reservas_bp.route('/api/reservas/<int:reserva_id>', methods=['DELETE'])
def cancel_reserva(reserva_id):
    for reserva in mock_reservas:
        if reserva['id'] == reserva_id:
            reserva['status'] = 'cancelada'
            return jsonify({"mensagem": "Reserva cancelada!", "reservation": reserva}), 200

    return jsonify({"erro": "Reserva não encontrada."}), 404