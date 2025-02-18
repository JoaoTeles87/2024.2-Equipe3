from flask import Blueprint, request, jsonify
from backend.modelo.reservas import mock_reservas
from backend.modelo.salas import mock_salas, EQUIPAMENTOS
from datetime import datetime

salas_bp = Blueprint('salas', __name__)

# Convert "HH:MM" string to datetime.time
def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

# Criar sala
@salas_bp.route('/api/salas', methods=['POST'])
def create_sala():
    """
    Exemplo de body:
    {
        "nome": "Sala E003",
        "tipo": "Reunião",
        "lugares": 20,
        "andar": 3,
        "equipamentos": ["Projetor", "Ar-condicionado"]
    }
    """

    dados = request.get_json()

    nome = dados.get("nome")
    tipo = dados.get("tipo")
    lugares = dados.get("lugares")
    andar = dados.get("andar")
    equipamentos = dados.get("equipamentos", [])


    if not nome or not tipo or not lugares or not andar:
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

    if tipo not in ["Reunião", "Auditório"]:
        return jsonify({"erro": "Tipo de sala inválido. Escolha entre 'Reunião' ou 'Auditório'"}), 400

    equipamentos_invalidos = [eq for eq in equipamentos if eq not in EQUIPAMENTOS]
    if equipamentos_invalidos:
        return jsonify({"erro": f"Equipamentos inválidos: {equipamentos_invalidos}"}), 400

    if any(sala["nome"] == nome for sala in mock_salas):
        return jsonify({"erro": "Já existe uma sala com esse nome"}), 409

    nova_sala = {
        "id": len(mock_salas) + 1,
        "nome": nome,
        "tipo": tipo,
        "lugares": lugares,
        "andar": andar,
        "equipamentos": equipamentos
    }
    mock_salas.append(nova_sala)

    return jsonify({"mensagem": "Sala criada com sucesso!", "sala": nova_sala}), 201


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

@salas_bp.route('/api/salas/<int:sala_id>', methods=['DELETE'])
def delete_sala(sala_id):

    sala = next((s for s in mock_salas if s["id"] == sala_id), None)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404

    reservas_ativas = [
        reserva for reserva in mock_reservas
        if reserva["sala_id"] == sala_id and reserva["status"] == "ativa"
    ]

    if reservas_ativas:
        return jsonify({"erro": "Sala possui reservas ativas e não pode ser deletada"}), 409

    mock_salas.remove(sala)

    return jsonify({"mensagem": "Sala deletada com sucesso!"}), 200