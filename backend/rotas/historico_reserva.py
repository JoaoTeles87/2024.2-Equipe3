from flask import Blueprint, jsonify, request

historico_reservas_bp = Blueprint("historico_reservas", __name__)

# Simulação de dados do usuário autenticado
usuarios = [
    {"id": 1, "email": "joao@email.com", "nome": "João"},
    {"id": 2, "email": "maria@email.com", "nome": "Maria"}
]

# Lista de reservas, com algumas ativas e outras inativas
reservas = [
    {"id": 1, "usuario_id": 1, "sala": {"nome": "Sala A"}, "data": "2025-01-15", "horario_inicio": "10:00", "horario_fim": "12:00", "ativa": True},
    {"id": 2, "usuario_id": 1, "sala": {"nome": "Sala B"}, "data": "2025-01-16", "horario_inicio": "14:00", "horario_fim": "16:00", "ativa": False},
    {"id": 3, "usuario_id": 2, "sala": {"nome": "Sala C"}, "data": "2025-01-17", "horario_inicio": "09:00", "horario_fim": "11:00", "ativa": False}
]

@historico_reservas_bp.route("/api/reservas/historico", methods=["POST"])
def consultar_historico_reservas():
    # Obtém o email do usuário autenticado (simulando um token JWT, por exemplo)
    email_usuario = request.json.get("email")  

    # Busca o usuário na lista de usuários simulada
    usuario = next((u for u in usuarios if u["email"] == email_usuario), None)
    
    if not usuario:
        return jsonify({"error": "Usuário não encontrado."}), 404

    # Filtra as reservas do usuário autenticado que são históricas (não ativas)
    reservas_historico = [
        {
            "id": r["id"],
            "sala": r["sala"]["nome"],
            "data": r["data"],
            "horario_inicio": r["horario_inicio"],
            "horario_fim": r["horario_fim"]
        }
        for r in reservas if r["usuario_id"] == usuario["id"] and not r["ativa"]
    ]

    if not reservas_historico:
        return jsonify({"message": "Nenhuma reserva histórica encontrada."}), 200

    return jsonify(reservas_historico), 200
