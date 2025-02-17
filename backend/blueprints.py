from rotas.login import login_bp
from rotas.cadastro import cadastro_bp
from rotas.logout import logout_bp
from rotas.testecookies import protegida_bp
from rotas.perfil import perfil_bp
from rotas.exclusao_perfil import exclusao_perfil_bp
from rotas.atualizar_perfil import atualizar_perfil_bp
from rotas.reservas_ativas import reservas_ativas_bp
from rotas.historico_reserva import historico_reservas_bp
from rotas.exclusao_reserva import exclusao_reserva_bp


# Registra os Blueprints
def registrarBlueprints(app):
    blueprints = [
       login_bp, cadastro_bp, logout_bp, protegida_bp, perfil_bp, reservas_ativas_bp, historico_reservas_bp, exclusao_perfil_bp, atualizar_perfil_bp, exclusao_reserva_bp,
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
