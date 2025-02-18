from flask import Blueprint, jsonify, request
from modelo.extensao import db
from modelo.usuario import Usuario
from modelo.reserva import Reserva

exclusao_perfil_bp = Blueprint("exclusao_perfil", __name__)

@exclusao_perfil_bp.route("/api/perfil", methods=["DELETE"])
def excluir_perfil():
    data = request.get_json()
    user_id = data.get("id")
    senha = data.get("senha")

    # Verifica se o ID e a senha foram fornecidos
    if not user_id or not senha:
        return jsonify({"error": "Os campos 'id' e 'senha' são obrigatórios."}), 400

    # Busca o usuário no banco de dados
    usuario = db.session.get(Usuario, user_id)  # Usando db.session.get() em vez de Query.get()
    if not usuario:
        return jsonify({"error": "Perfil não encontrado para o ID fornecido"}), 404

    # Verifica se a senha está correta
    if usuario.senha != senha:
        return jsonify({"error": "Senha incorreta."}), 401  # Mudando para 401 para indicar erro de autenticação

    # Verifica se o usuário tem reservas ativas
    reservas_ativas = Reserva.query.filter_by(usuario_id=user_id, ativa=True).first()
    if reservas_ativas:
        return jsonify({"error": "Não é possível excluir o perfil com reservas ativas. Cancele todas as reservas primeiro."}), 400

    try:
        # Deleta o usuário
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Perfil excluído com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Houve um problema ao excluir sua conta. Tente novamente mais tarde."}), 500