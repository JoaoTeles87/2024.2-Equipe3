from backend.rotas.login import login_bp
from backend.rotas.cadastro import cadastro_bp
from backend.rotas.logout import logout_bp

# Registra os Blueprints
def registrarBlueprints(app):
    blueprints = [
       login_bp, cadastro_bp, logout_bp
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)