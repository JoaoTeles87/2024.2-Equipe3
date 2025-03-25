from flask import Flask, jsonify  # Adicionei jsonify aqui
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
from backend.rotas.criarReview import criar_review_bp
from backend.rotas.atualizarReview import atualizar_review_bp
from backend.rotas.deletarReview import deletar_review_bp
from backend.rotas.obterReview import obter_review_bp
from backend.rotas.listarReview import listar_reviews_bp
from backend.rotas.perfil import perfil_bp 
from backend.rotas.reservas_ativas import reservas_ativas_bp
from backend.rotas.exclusao_perfil import exclusao_perfil_bp
from backend.rotas.atualizar_perfil import atualizar_perfil_bp 
from backend.rotas.historico_reserva import historico_reservas_bp
from flask_cors import CORS

def registrarBlueprints(app):
    blueprints = [
        perfil_bp,         
        exclusao_perfil_bp, 
        atualizar_perfil_bp,
        historico_reservas_bp,
        login_bp,
        cadastro_bp,
        logout_bp,
        criar_manutencao_bp,
        criar_recursos_bp,
        excluir_manutencao_bp,
        excluir_recursos_bp,
        editar_recursos_bp,
        editar_manutencao_bp,
        salas_bp,
        usuarios_bp,
        reservas_bp,
        criar_review_bp,
        listar_reviews_bp,
        obter_review_bp,
        deletar_review_bp,
        atualizar_review_bp,
        reservas_ativas_bp
    ]
    
    # Configuração global do CORS
    CORS(app, 
         supports_credentials=True,
         resources={
             r"/api/*": {
                 "origins": "*",
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"]
             }
         })
    
    # Registra os blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
        
    # Debug route to list all endpoints
    @app.route("/routes")
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "path": str(rule)
            })
        return jsonify(routes)