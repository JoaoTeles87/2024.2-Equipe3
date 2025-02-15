from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

editar_manutencao_bp = Blueprint("editarmanutencao", __name__)

@editar_manutencao_bp.route("/solicitacoes/manutencao/<int:id>", methods=["PUT"])
def editar_solicitacao_manutencao(id):
    solicitacao = SolicitacaoManutencao.query.get_or_404(id)
    dados = request.json

        # Verifica se a nova descrição é vazia ou apenas espaços em branco
    nova_descricao = dados.get("descricao", solicitacao.descricao)
    if not nova_descricao.strip():
        return jsonify({"error": "A descrição da manutenção não pode ser vazia"}), 400

    solicitacao.descricao = nova_descricao
    db.session.commit()
    return jsonify({"message": "Solicitação de manutenção atualizada com sucesso"}), 200