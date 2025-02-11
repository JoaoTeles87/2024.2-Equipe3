from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

criar_recursos_bp = Blueprint("criarrecursos", __name__)

@criar_recursos_bp.route("/solicitacoes/recursos", methods=["POST"])
def criar_solicitacao_recursos():
    dados = request.json
    solicitacao = SolicitacaoRecursos(
        reserva_id=dados.get("reserva_id"),
        recursos=dados.get("recursos"),
        itens_nao_listados=dados.get("itens_nao_listados"),
        observacoes=dados.get("observacoes")
    )
    db.session.add(solicitacao)
    db.session.commit()
    #return jsonify({"id": solicitacao.id}), 201
    return jsonify({"message":"Parabéns, sua solicitação foi criada"}), 201