from flask import Blueprint, jsonify

# Simulação de dados do usuário autenticado
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "id": 1  # Simulando ID do usuário
}

# Simulação de reservas ativas (dados estáticos)
reservas_ativas = [
    {"id": 1, "usuario_id": 1, "sala": {"nome": "porra A"}, "data": "2025-02-16", "horario_inicio": "09:00", "horario_fim": "11:00", "ativa": True},
    {"id": 2, "usuario_id": 1, "sala": {"nome": "Sala B"}, "data": "2025-02-17", "horario_inicio": "13:00", "horario_fim": "15:00", "ativa": True}
]

reservas_ativas_bp = Blueprint("reservasAtivas", __name__)

@reservas_ativas_bp.route("/api/reservas/ativas", methods=["POST"])
def consultar_reservas_ativas():
    # Simulando a autenticação do usuário
    if usuario["email"] != "teste@email.com":
        return jsonify({"error": "Usuário não encontrado."}), 404

    # Filtrando as reservas ativas para o usuário
    reservas_list = [{
        "id": r["id"],
        "sala": r["sala"]["nome"],
        "data": r["data"],
        "horario_inicio": r["horario_inicio"],
        "horario_fim": r["horario_fim"]
    } for r in reservas_ativas if r["usuario_id"] == usuario["id"] and r["ativa"]]

    # Caso não tenha reservas ativas
    if not reservas_list:
        return jsonify({"error": "Não há reservas ativas para este usuário."}), 404

    return jsonify(reservas_list), 200
