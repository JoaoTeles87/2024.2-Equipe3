from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos
import flask

excluir_recursos_bp = Blueprint("excluirrecursos", __name__)

@excluir_recursos_bp.route("/solicitacoes/recursos/<int:id>", methods=["DELETE"])
def excluir_solicitacao_recursos(id):
    solicitacao = db.session.get(SolicitacaoRecursos, id) or flask.abort(404)
    db.session.delete(solicitacao)
    db.session.commit()
    return jsonify({"message": "Solicitação excluída"}), 204
