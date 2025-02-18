from rotas.login import login_bp
from rotas.cadastro import cadastro_bp
from rotas.logout import logout_bp
from rotas.testecookies import protegida_bp
from rotas.reservas import reservas_bp
from rotas.salas import salas_bp
from rotas.usuario import usuarios_bp

# Registra os Blueprints
def registrarBlueprints(app):
    blueprints = [
       login_bp, cadastro_bp, logout_bp, protegida_bp, reservas_bp, salas_bp, usuarios_bp
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)