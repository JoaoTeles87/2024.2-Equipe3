from backend.rotas.login import login_bp
from backend.rotas.cadastro import cadastro_bp
from backend.rotas.logout import logout_bp
from backend.rotas.testecookies import protegida_bp
from backend.rotas.criarReview import criar_review_bp
from backend.rotas.listarReview import listar_reviews_bp
from backend.rotas.obterReview import obter_review_bp
from backend.rotas.atualizarReview import atualizar_review_bp
from backend.rotas.deletarReview import deletar_review_bp

# Registra os Blueprints
def registrarBlueprints(app):
    blueprints = [
       login_bp, cadastro_bp, logout_bp, protegida_bp
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    app.register_blueprint(criar_review_bp)
    app.register_blueprint(listar_reviews_bp)
    app.register_blueprint(obter_review_bp)
    app.register_blueprint(atualizar_review_bp)
    app.register_blueprint(deletar_review_bp)