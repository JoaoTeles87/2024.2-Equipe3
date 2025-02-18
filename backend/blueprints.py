from backend.rotas.login import login_bp
from backend.rotas.cadastro import cadastro_bp
from backend.rotas.logout import logout_bp
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
       login_bp, cadastro_bp, logout_bp, reservas_bp, salas_bp, usuarios_bp, perfil_bp, reservas_ativas_bp, historico_reservas_bp, exclusao_perfil_bp, atualizar_perfil_bp, exclusao_reserva_bp,
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
