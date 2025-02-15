from flask import Blueprint, request, jsonify
from modelo.extensao import db
from modelo.solicitacaomanutencao import SolicitacaoManutencao
from modelo.solicitacaorecursos import SolicitacaoRecursos

criar_manutencao_bp = Blueprint("criarmanutencao", __name__)

@criar_manutencao_bp.route("/solicitacoes/manutencao", methods=["POST"])
def criar_solicitacao_manutencao():
    dados = request.json

    # Verifica se 'descricao' está vazio ou None
    if not dados.get("descricao"):
        return jsonify({"error": "O campo 'descricao' não pode estar vazio."}), 400
        
    solicitacao = SolicitacaoManutencao(
        reserva_id=dados.get("reserva_id"),
        descricao=dados.get("descricao")
    )
    db.session.add(solicitacao)
    db.session.commit()
    return jsonify({"id": solicitacao.id, "message": "Parabéns, sua solicitação de manutenção foi criada!"}), 201