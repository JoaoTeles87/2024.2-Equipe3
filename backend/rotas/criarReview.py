from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.reviewSala import ReviewSala

criar_review_bp = Blueprint('criar_review', __name__)

@criar_review_bp.route('/api/reviews', methods=['POST'])
def criar_review():
    dados = request.get_json()

    reserva_id = dados.get("reserva_id")
    sala_id = dados.get("sala_id")
    usuario_id = dados.get("usuario_id")
    nota = dados.get("nota")
    comentario = dados.get("comentario")

    if reserva_id is None:
        return jsonify({"error": "O ID da Reserva é obrigatório para avaliar a sala."}), 400
    if sala_id is None:
        return jsonify({"error": "O ID da Sala é obrigatório para avaliar a sala."}), 400
    if usuario_id is None:
        return jsonify({"error": "O ID do Usuário é obrigatório para avaliar a sala."}), 400
    if nota is None:
        return jsonify({"error": "A nota é obrigatória para avaliar a sala."}), 400

    try:
        nova_review = ReviewSala(
            reserva_id=reserva_id,
            sala_id=sala_id,
            usuario_id=usuario_id,
            nota=nota,
            comentario=comentario,
        )
        db.session.add(nova_review)
        db.session.commit()
    except Exception as e:
        # Log a exceção para depuração
        app.logger.error("Erro ao criar review: %s", e)
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({
        "mensagem": "Avaliação criada com sucesso!",
        "review": {
            "id": nova_review.id,
            "reserva_id": nova_review.reserva_id,
            "sala_id": nova_review.sala_id,
            "usuario_id": nova_review.usuario_id,
            "nota": nova_review.nota,
            "comentario": nova_review.comentario,
        }
    }), 201
