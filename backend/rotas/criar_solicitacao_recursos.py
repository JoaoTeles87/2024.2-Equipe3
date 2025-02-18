from flask import Blueprint, request, jsonify
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos

criar_recursos_bp = Blueprint("criarrecursos", __name__)

@criar_recursos_bp.route("/solicitacoes/recursos", methods=["POST"])
def criar_solicitacao_recursos():
    dados = request.json
    
    recursos = dados.get("recursos", "").strip()
    itens_nao_listados = dados.get("itens_nao_listados", "").strip()

    # Validação: se recursos estiver vazio, itens_nao_listados deve estar preenchido
    if not recursos and not itens_nao_listados:
        return jsonify({"erro": "Você deve selecionar um recurso ou especificar itens não listados."}), 400

    # Verifica se 'recursos' é None ou uma string vazia
    #if not dados.get("recursos"):  
        #return jsonify({"error": "O campo 'recursos' não pode estar vazio."}), 400

    #solicitacao = SolicitacaoRecursos(
        #reserva_id=dados.get("reserva_id"),
        #recursos=dados.get("recursos"),
        #itens_nao_listados=dados.get("itens_nao_listados"),
        #observacoes=dados.get("observacoes")
    #)

    solicitacao = SolicitacaoRecursos(
    reserva_id=dados.get("reserva_id"),
    recursos=recursos,
    itens_nao_listados=itens_nao_listados,
    observacoes=dados.get("observacoes", "").strip()
    )
    db.session.add(solicitacao)
    db.session.commit()
    return jsonify({"id": solicitacao.id, "mensagem": "Parabéns, sua solicitação de recursos foi criada!"}), 201