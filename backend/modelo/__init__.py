from flask import Flask, jsonify
from .extensao import db
from .usuario import Usuario
import logging

def create_app():
    app = Flask(__name__)

    # Configuração de banco de dados e outras configurações
    app.config.from_object('config.DevelopmentConfig')  # ou TestingConfig / ProductionConfig

    # Inicializando o banco de dados
    db.init_app(app)

    # Registrando blueprints
    from rotas.atualizar_perfil import atualizar_perfil_bp
    app.register_blueprint(atualizar_perfil_bp)

    from rotas.exclusao_perfil import exclusao_perfil_bp
    app.register_blueprint(exclusao_perfil_bp)

    from rotas.exclusao_reserva import exclusao_reserva_bp
    app.register_blueprint(exclusao_reserva_bp)

    from rotas.historico_reserva import historico_reservas_bp
    app.register_blueprint(historico_reservas_bp)

    from rotas.reservas_ativas import reservas_ativas_bp
    app.register_blueprint(reservas_ativas_bp)
    
    # Tratamento de erros
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Recurso não encontrado."}), 404

    # Configuração de log
    logging.basicConfig(level=logging.DEBUG)

    return app
