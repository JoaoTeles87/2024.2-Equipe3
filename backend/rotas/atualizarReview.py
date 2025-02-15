from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.reviewSala import ReviewSala

atualizar_review_bp = Blueprint("atualizar_review", __name__)

@atualizar_review_bp.route("/api/reviews/<int:id>", methods=["PUT"])
def atualizar_review(id):
    review = ReviewSala.query.get(id)
    #Verifica o ID
    if not review:
        return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404

    data = request.get_json()
    # Atualiza a nota e o comentário se estiverem presentes no JSON
    review.nota = data.get("nota", review.nota)
    review.comentario = data.get("comentario", review.comentario)
    
    db.session.commit()
    return jsonify({"mensagem": "Avaliação atualizada com sucesso!"})
