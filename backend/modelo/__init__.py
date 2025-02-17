from flask import Flask, jsonify
from .extensao import db
from .usuario import Usuario

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  

    # Registrando blueprints ou rotas aqui
    from rotas.atualizar_perfil import atualizar_perfil_bp
    app.register_blueprint(atualizar_perfil_bp)

    from rotas.exclusao_perfil import exclusao_perfil_bp
    app.register_blueprint(exclusao_perfil_bp)

    from rotas.exclusao_reserva import exclusao_reserva_bp
    app.register_blueprint(exclusao_reserva_bp)

    # Corrigir a importação duplicada
    from rotas.historico_reserva import historico_reservas_bp 
    app.register_blueprint(historico_reservas_bp)

    from rotas.reservas_ativas import reservas_ativas_bp 
    app.register_blueprint(reservas_ativas_bp)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404
    
    return app
