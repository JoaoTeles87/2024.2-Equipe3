from backend.rotas.login import login_bp
from backend.rotas.cadastro import cadastro_bp
from backend.rotas.logout import logout_bp
from backend.rotas.testecookies import protegida_bp
from backend.rotas.criar_solicitacao_manutencao import criar_manutencao_bp
from backend.rotas.criar_solicitacao_recursos import criar_recursos_bp
from backend.rotas.excluir_solicitacao_manutencao import excluir_manutencao_bp
from backend.rotas.excluir_solicitacao_recursos import excluir_recursos_bp
from backend.rotas.editar_solicitacao_manutencao import editar_manutencao_bp
from backend.rotas.editar_solicitacao_recursos import editar_recursos_bp

# Registra os Blueprints
def registrarBlueprints(app):
    blueprints = [
       login_bp, cadastro_bp, logout_bp, protegida_bp, criar_manutencao_bp, criar_recursos_bp, excluir_manutencao_bp, excluir_recursos_bp, editar_recursos_bp, editar_manutencao_bp
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)