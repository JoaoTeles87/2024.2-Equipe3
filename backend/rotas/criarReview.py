from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.reviewSala import ReviewSala

criar_review_bp = Blueprint("criar_review", __name__)

@criar_review_bp.route("/api/reviews", methods=["POST"])
def criar_review():
    data = request.get_json()

    # Aqui tá verificando se os campos obrigatórios foram preenchidos
    # se faltar o comentário, ainda vai passar (campo não obrigatório)

    if data.get("nota") is None:
        return jsonify({"error": "A nota é obrigatória para avaliar a sala."}), 400

    elif data.get("sala_id") is None:
        return jsonify({"error": "O ID da Sala é obrigatório para avaliar a sala."}), 400
    
    elif data.get("usuario_id") is None:
        return jsonify({"error": "O ID do Usuário é obrigatório para avaliar a sala."}), 400
    
    elif data.get("reserva_id") is None:
        return jsonify({"error": "O ID da Reserva é obrigatório para avaliar a sala."}), 400
    
    # Verifica tudo e prossegue pra avaliação!  
    nova_review = ReviewSala(
        reserva_id=data.get("reserva_id"),
        sala_id=data.get("sala_id"),
        usuario_id=data.get("usuario_id"),
        nota=data.get("nota"),
        comentario=data.get("comentario"),
    )
    db.session.add(nova_review)
    db.session.commit()
    return jsonify({"mensagem": "Avaliação criada com sucesso!"}), 201
