from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

editar_recursos_bp = Blueprint("editarrecursos", __name__)

@editar_recursos_bp.route("/solicitacoes/recursos/<int:id>", methods=["PUT"])
def editar_solicitacao_recursos(id):
    solicitacao = SolicitacaoRecursos.query.get_or_404(id)
    dados = request.json
    solicitacao.recursos = dados.get("recursos", solicitacao.recursos)
    solicitacao.itens_nao_listados = dados.get("itens_nao_listados", solicitacao.itens_nao_listados)
    solicitacao.observacoes = dados.get("observacoes", solicitacao.observacoes)
    db.session.commit()
    return jsonify({"message": "Solicitação de recursos atualizada com sucesso"})