from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()

    usuarios_json = [
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "professor": usuario.professor
        }
        for usuario in usuarios
    ]

    return jsonify(usuarios_json), 200


@usuarios_bp.route("/api/usuarios/<int:usuario_id>", methods=["DELETE"])
def deletar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"menssagem": "Usuário deletado com sucesso"}), 200