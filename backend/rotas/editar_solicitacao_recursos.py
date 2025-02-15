from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

editar_recursos_bp = Blueprint("editarrecursos", __name__)

@editar_recursos_bp.route("/solicitacoes/recursos/<int:id>", methods=["PUT"])
def editar_solicitacao_recursos(id):
    solicitacao = SolicitacaoRecursos.query.get_or_404(id)
    dados = request.json

     # Verifica se ambos os campos estão vazios
    recursos = dados.get("recursos", "").strip()
    itens_nao_listados = dados.get("itens_nao_listados", "").strip()

    if not recursos and not itens_nao_listados:
        return jsonify({"error": "Você deve preencher pelo menos 'recursos' ou 'itens_nao_listados'."}), 400
   
    # Atualiza os campos apenas se foram passados na requisição
    solicitacao.recursos = recursos if "recursos" in dados else solicitacao.recursos
    solicitacao.itens_nao_listados = itens_nao_listados if "itens_nao_listados" in dados else solicitacao.itens_nao_listados
    solicitacao.observacoes = dados.get("observacoes", solicitacao.observacoes)

    db.session.commit()
    return jsonify({"message": "Solicitação de recursos atualizada com sucesso"}), 200