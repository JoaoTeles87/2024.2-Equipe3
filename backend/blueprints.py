from backend.rotas.criarReview import criar_review_bp
from backend.rotas.listarReview import listar_reviews_bp
from backend.rotas.obterReview import obter_review_bp
from backend.rotas.atualizarReview import atualizar_review_bp
from backend.rotas.deletarReview import deletar_review_bp
from backend.rotas.login import login_bp
from backend.rotas.cadastro import cadastro_bp
from backend.rotas.logout import logout_bp
from backend.rotas.criar_solicitacao_manutencao import criar_manutencao_bp
from backend.rotas.criar_solicitacao_recursos import criar_recursos_bp
from backend.rotas.excluir_solicitacao_manutencao import excluir_manutencao_bp
from backend.rotas.excluir_solicitacao_recursos import excluir_recursos_bp
from backend.rotas.editar_solicitacao_manutencao import editar_manutencao_bp
from backend.rotas.editar_solicitacao_recursos import editar_recursos_bp
from backend.rotas.reservas import reservas_bp
from backend.rotas.salas import salas_bp
from backend.rotas.usuario import usuarios_bp
from backend.rotas.login import login_bp
from backend.rotas.cadastro import cadastro_bp
from backend.rotas.logout import logout_bp
from backend.rotas.perfil import perfil_bp
from backend.rotas.exclusao_perfil import exclusao_perfil_bp
from backend.rotas.atualizar_perfil import atualizar_perfil_bp
from backend.rotas.reservas_ativas import reservas_ativas_bp
from backend.rotas.historico_reserva import historico_reservas_bp
from backend.rotas.exclusao_reserva import exclusao_reserva_bp

# Registra os Blueprints
def registrarBlueprints(app):
    blueprints = [
       login_bp, cadastro_bp, logout_bp, reservas_bp, usuarios_bp, salas_bp, criar_manutencao_bp, criar_recursos_bp, excluir_manutencao_bp, excluir_recursos_bp, editar_recursos_bp, 
       editar_manutencao_bp, perfil_bp, reservas_ativas_bp, historico_reservas_bp, exclusao_perfil_bp, atualizar_perfil_bp, exclusao_reserva_bp, criar_review_bp, listar_reviews_bp, obter_review_bp, atualizar_review_bp, deletar_review_bp
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
