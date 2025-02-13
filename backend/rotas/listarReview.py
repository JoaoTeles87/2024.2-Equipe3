from flask import Blueprint, jsonify
from modelo.reviewSala import ReviewSala

listar_reviews_bp = Blueprint("listar_reviews", __name__)

@listar_reviews_bp.route("/api/reviews", methods=["GET"])
def listar_reviews():
    reviews = ReviewSala.query.all()
    resultado = []
    for review in reviews:
        resultado.append({
            "id": review.id,
            "reserva_id": review.reserva_id,
            "sala_id": review.sala_id,
            "usuario_id": review.usuario_id,
            "nota": review.nota,
            "comentario": review.comentario,
            "data_avaliacao": review.data_avaliacao
        })
    return jsonify(resultado)
