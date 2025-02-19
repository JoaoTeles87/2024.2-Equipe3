from flask import Blueprint, jsonify
from backend.modelo.reviewSala import ReviewSala

listar_reviews_bp = Blueprint("listar_reviews", __name__)

@listar_reviews_bp.route("/api/reviews", methods=["GET"])
def listar_reviews():
    reviews = ReviewSala.query.all()
    #Verifica as avaliações
    if not reviews:
        return jsonify({"error": "Nenhuma avaliação encontrada."}), 404
    
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
    return jsonify(resultado), 200
