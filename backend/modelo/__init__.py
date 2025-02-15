from flask import Flask
from .extensao import db
from .reviewSala import ReviewSala
from .usuario import Usuario

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  

    # Registrando blueprints ou rotas aqui
    from rotas.atualizarReview import atualizar_review_bp
    app.register_blueprint(atualizar_review_bp)

    from rotas.deletarReview import deletar_review_bp
    app.register_blueprint(deletar_review_bp)

    from rotas.obterReview import obter_review_bp
    app.register_blueprint(obter_review_bp)

    from rotas.listarReview import listar_reviews_bp
    app.register_blueprint(listar_reviews_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404
    
    return app
