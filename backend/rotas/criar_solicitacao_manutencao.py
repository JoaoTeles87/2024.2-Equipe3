from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos

criar_manutencao_bp = Blueprint("criarmanutencao", __name__)

@criar_manutencao_bp.route("/solicitacoes/manutencao", methods=["POST"])
def criar_solicitacao_manutencao():
    dados = request.json

    # Verifica se 'descricao' está vazio ou None
    if not dados.get("descricao").strip():
        return jsonify({"erro": "O campo 'descricao' não pode estar vazio."}), 400

    solicitacao = SolicitacaoManutencao(
        reserva_id=dados.get("reserva_id"),
        descricao=dados.get("descricao")
    )
    db.session.add(solicitacao)
    db.session.commit()
    return jsonify({"id": solicitacao.id, "mensagem": "Parabéns, sua solicitação de manutenção foi criada!"}), 201