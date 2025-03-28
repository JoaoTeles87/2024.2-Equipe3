from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos
import flask

editar_recursos_bp = Blueprint("editarrecursos", __name__)

@editar_recursos_bp.route("/solicitacoes/recursos/<int:id>", methods=["PUT"])
def editar_solicitacao_recursos(id):
    solicitacao = db.session.get(SolicitacaoRecursos, id) or flask.abort(404)
    dados = request.json

     # Verifica se ambos os campos estão vazios
    recursos = dados.get("recursos", "").strip()
    itens_nao_listados = dados.get("itens_nao_listados", "").strip()

    if not recursos and not itens_nao_listados:
        return jsonify({"erro": "Você deve preencher pelo menos 'recursos' ou 'itens_nao_listados'."}), 400
   
    # Atualiza os campos apenas se foram passados na requisição
    solicitacao.recursos = recursos if "recursos" in dados else solicitacao.recursos
    solicitacao.itens_nao_listados = itens_nao_listados if "itens_nao_listados" in dados else solicitacao.itens_nao_listados
    solicitacao.observacoes = dados.get("observacoes", solicitacao.observacoes)

    db.session.commit()
    return jsonify({"mensagem": "Solicitação de recursos atualizada com sucesso"}), 200