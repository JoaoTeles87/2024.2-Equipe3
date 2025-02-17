from flask import Blueprint, jsonify

# Simulação de dados do usuário autenticado
usuario = {
    "email": "joao@email.com",
    "nome": "João",
    "id": 1
}

# Lista de reservas, com algumas ativas e outras inativas
reservas = [
    {"id": 1, "usuario_id": 1, "sala": {"nome": "Sala A"}, "data": "2025-01-15", "horario_inicio": "10:00", "horario_fim": "12:00", "ativa": True},
    {"id": 2, "usuario_id": 1, "sala": {"nome": "Sala B"}, "data": "2025-01-16", "horario_inicio": "14:00", "horario_fim": "16:00", "ativa": True}
]

# Blueprint para as rotas do histórico de reservas
historico_reservas_bp = Blueprint("historico_reservas", __name__)

@historico_reservas_bp.route("/api/reservas/historico", methods=["POST"])
def consultar_historico_reservas():
    # Simulando que o usuário está autenticado
    if usuario["email"] != "joao@email.com":
        return jsonify({"error": "Usuário não encontrado."}), 404

    # Filtrando as reservas do usuário com base no status 'ativa'
    reservas_historico = [{
        "id": r["id"],
        "sala": r["sala"]["nome"],
        "data": r["data"],
        "horario_inicio": r["horario_inicio"],
        "horario_fim": r["horario_fim"]
    } for r in reservas if r["usuario_id"] == usuario["id"] and not r["ativa"]]  # Filtrando apenas as inativas

    # Se não houver reservas históricas e todas as reservas forem ativas ou não existirem
    if not reservas_historico and all(r["ativa"] for r in reservas if r["usuario_id"] == usuario["id"]):
        return jsonify({"message": "Nenhuma reserva histórica encontrada."}), 200

    # Caso contrário, retorna as reservas históricas
    return jsonify(reservas_historico), 200

# Função para simular a alteração no estado das reservas
def alterar_reservas_ativas(estado_ativo=True):
    for reserva in reservas:
        reserva["ativa"] = estado_ativo
