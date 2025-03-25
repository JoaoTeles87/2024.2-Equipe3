from flask import Blueprint, jsonify, request
from flask_cors import CORS

historico_reservas_bp = Blueprint("historico_reservas", __name__)
CORS(historico_reservas_bp)

# Mock de dados com mensagens e avaliações
mock_reservas = [
    {
        "id": 1,
        "usuario_id": 1,
        "sala": {
            "id": 1,
            "nome": "Sala E005",
            "tipo": "Laboratório",
            "lugares": 30
        },
        "data": "2024-03-25",
        "start_time": "14:00",
        "end_time": "16:00",
        "status": "inativa",
        "comentario": "Ótima sala, muito bem equipada!", 
        "avaliacao": 5
    },
    {
        "id": 2,
        "usuario_id": 1,
        "sala": {
            "id": 2,
            "nome": "Sala E002",
            "tipo": "Auditório",
            "lugares": 50
        },
        "data": "2024-03-26",
        "start_time": "10:00",
        "end_time": "12:00",
        "status": "inativa",
        "comentario": "Bom espaço, mas o som não estava muito bom.",  
        "avaliacao": 3
    }
]

@historico_reservas_bp.route("/api/reservas/historico/<int:usuario_id>", methods=["GET"])
def obter_historico_reservas(usuario_id):
    print(f"Rota GET /api/reservas/historico/{usuario_id} foi acessada!")
    
    try:
        # Filtra reservas inativas do usuário
        historico = [
            {
                "id": r["id"],
                "sala": r["sala"],
                "data": r["data"],
                "start_time": r["start_time"],
                "end_time": r["end_time"],
                "horario": f"{r['start_time']} às {r['end_time']}",  
                "status": r["status"],
                "avaliacao": r.get("avaliacao", 0), 
                "comentario": r.get("comentario", "")  
            }
            for r in mock_reservas 
            if r["usuario_id"] == usuario_id and r["status"] == "inativa"
        ]

        return jsonify({
            "message": "Histórico encontrado com sucesso",
            "total": len(historico),
            "historico": historico
        }), 200

    except Exception as e:
        print(f"Erro ao obter histórico: {str(e)}")
        return jsonify({
            "error": "Erro interno ao buscar histórico",
            "detalhes": str(e)
        }), 500