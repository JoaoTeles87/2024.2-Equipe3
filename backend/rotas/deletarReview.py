from flask import Blueprint, jsonify
from modelo.extensao import db
from modelo.reviewSala import ReviewSala

deletar_review_bp = Blueprint("deletar_review", __name__)

@deletar_review_bp.route("/api/reviews/<int:id>", methods=["DELETE"])
def deletar_review(id):
    review = ReviewSala.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({"mensagem": "Avaliação deletada com sucesso!"})
