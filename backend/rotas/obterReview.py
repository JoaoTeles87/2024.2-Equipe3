from flask import Blueprint, jsonify
from modelo.reviewSala import ReviewSala

obter_review_bp = Blueprint("obter_review", __name__)

@obter_review_bp.route("/api/reviews/<int:id>", methods=["GET"])
def obter_review(id):
    review = ReviewSala.query.get(id)
    #Verifica o ID
    if not review:
        return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404

    return jsonify({
        "id": review.id,
        "reserva_id": review.reserva_id,
        "sala_id": review.sala_id,
        "usuario_id": review.usuario_id,
        "nota": review.nota,
        "comentario": review.comentario,
        "data_avaliacao": review.data_avaliacao
    })
