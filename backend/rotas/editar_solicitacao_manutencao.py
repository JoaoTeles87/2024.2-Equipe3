from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos
import flask

editar_manutencao_bp = Blueprint("editarmanutencao", __name__)

@editar_manutencao_bp.route("/solicitacoes/manutencao/<int:id>", methods=["PUT"])
def editar_solicitacao_manutencao(id):
    solicitacao = db.session.get(SolicitacaoManutencao, id) or flask.abort(404)

    dados = request.json

        # Verifica se a nova descrição é vazia ou apenas espaços em branco
    nova_descricao = dados.get("descricao", solicitacao.descricao)
    if not nova_descricao.strip():
        return jsonify({"erro": "A descrição da manutenção não pode ser vazia"}), 400

    solicitacao.descricao = nova_descricao
    db.session.commit()
    return jsonify({
    "mensagem": "Solicitação de manutenção atualizada com sucesso",
    "id": solicitacao.id,
    #"reserva_id": solicitacao.reserva_id,
    "descricao": solicitacao.descricao
}), 200