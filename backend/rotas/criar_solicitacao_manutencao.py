from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

criar_manutencao_bp = Blueprint("criarmanutencao", __name__)

@criar_manutencao_bp.route("/solicitacoes/manutencao", methods=["POST"])
def criar_solicitacao_manutencao():
    dados = request.json
    solicitacao = SolicitacaoManutencao(
        reserva_id=dados.get("reserva_id"),
        descricao=dados.get("descricao")
    )
    db.session.add(solicitacao)
    db.session.commit()
    return jsonify({"id": solicitacao.id}), 201