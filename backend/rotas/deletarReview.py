from flask import Blueprint, jsonify, abort
from modelo.extensao import db
from modelo.reviewSala import ReviewSala

deletar_review_bp = Blueprint("deletar_review", __name__)

@deletar_review_bp.route("/api/reviews/<int:id>", methods=["DELETE"])
def deletar_review(id):
    review = db.session.get(ReviewSala, id)
    #Verifica o ID
    if not review:
        return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404
    
    db.session.delete(review)
    db.session.commit()
    return jsonify({"mensagem": "Avaliação deletada com sucesso!"})
