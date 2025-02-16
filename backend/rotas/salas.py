from flask import Blueprint, request, jsonify
from modelo.reservas import mock_reservas
from modelo.salas import mock_salas, EQUIPAMENTOS
from datetime import datetime

salas_bp = Blueprint('salas', __name__)

# Convert "HH:MM" string to datetime.time
def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

# Get salas
@salas_bp.route('/api/salas', methods=['GET'])
def get_salas_disponiveis():
    equipamentos_filtro = request.args.getlist("equipamentos")  # Get filter from query params
    data = request.args.get("data")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    if not equipamentos_filtro and not data and not start_time and not end_time:
        return jsonify(mock_salas), 200
    elif not data:
        return jsonify({'erro': 'data não informada'}), 400
    elif not start_time or not end_time:
        return jsonify({'erro': 'tempo não informado'}), 400


    salas_filtradas = [
        sala for sala in mock_salas
        if not equipamentos_filtro or all(eq in sala["equipamentos"] for eq in equipamentos_filtro)
    ]

    if data and start_time and end_time:
        salas_disponiveis = []
        for sala in salas_filtradas:
            reservas_existentes = [
                reserva for reserva in mock_reservas
                if reserva["sala_id"] == sala["id"] and reserva["data"] == data and
                   not (parse_time(reserva["end_time"]) <= parse_time(start_time) or
                        parse_time(reserva["start_time"]) >= parse_time(end_time)) and
                   reserva["status"] == "ativa"
            ]

            if not reservas_existentes:
                salas_disponiveis.append(sala)
    else:
        salas_disponiveis = salas_filtradas

    if not salas_disponiveis:
        return jsonify({'mensagem': 'nenhuma sala encontrada'}), 404

    return jsonify(salas_disponiveis), 200