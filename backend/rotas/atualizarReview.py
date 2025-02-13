from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.reviewSala import ReviewSala

atualizar_review_bp = Blueprint("atualizar_review", __name__)

@atualizar_review_bp.route("/api/reviews/<int:id>", methods=["PUT"])
def atualizar_review(id):
    review = ReviewSala.query.get_or_404(id)
    dados = request.get_json()
    review.nota = dados.get("nota", review.nota)
    review.comentario = dados.get("comentario", review.comentario)
    db.session.commit()
    return jsonify({"mensagem": "Avaliação atualizada com sucesso!"})
