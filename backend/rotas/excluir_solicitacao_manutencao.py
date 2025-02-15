from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

excluir_manutencao_bp = Blueprint("excluirmanutencao", __name__)

@excluir_manutencao_bp.route("/solicitacoes/manutencao/<int:id>", methods=["DELETE"])
def excluir_solicitacao_manutencao(id):
    solicitacao = SolicitacaoManutencao.query.get_or_404(id)
    db.session.delete(solicitacao)
    db.session.commit()
    return jsonify({"message": "Solicitação excluída"}), 204
