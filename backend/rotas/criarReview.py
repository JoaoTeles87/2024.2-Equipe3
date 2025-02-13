from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.reviewSala import ReviewSala

criar_review_bp = Blueprint("criar_review", __name__)

@criar_review_bp.route("/api/reviews", methods=["POST"])
def criar_review():
    dados = request.get_json()
    nova_review = ReviewSala(
        reserva_id=dados["reserva_id"],
        sala_id=dados["sala_id"],
        usuario_id=dados["usuario_id"],
        nota=dados["nota"],
        comentario=dados.get("comentario")
    )
    db.session.add(nova_review)
    db.session.commit()
    return jsonify({"mensagem": "Avaliação criada com sucesso!"}), 201
