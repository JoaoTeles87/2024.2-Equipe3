import pytest
from flask import Flask
from backend.rotas.criar_solicitacao_manutencao import criar_manutencao_bp
from backend.rotas.criar_solicitacao_recursos import criar_recursos_bp
from backend.rotas.editar_solicitacao_manutencao import editar_manutencao_bp
from backend.rotas.editar_solicitacao_recursos import editar_recursos_bp
from backend.rotas.excluir_solicitacao_manutencao import excluir_manutencao_bp
from backend.rotas.excluir_solicitacao_recursos import excluir_recursos_bp
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def app():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(criar_manutencao_bp)
    aplicacao.register_blueprint(criar_recursos_bp)
    aplicacao.register_blueprint(editar_manutencao_bp)
    aplicacao.register_blueprint(editar_recursos_bp)
    aplicacao.register_blueprint(excluir_manutencao_bp)
    aplicacao.register_blueprint(excluir_recursos_bp)
    aplicacao.config["TESTING"] = True
    aplicacao.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    aplicacao.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with aplicacao.app_context():
        db.init_app(aplicacao)
        db.create_all()
        yield aplicacao
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_database(app):
    """Popula o banco de dados com manutenções de teste antes dos testes rodarem."""
    with app.app_context():
        db.create_all()
        
        manutencao1 = SolicitacaoManutencao(
            reserva_id=1,
            descricao="Mesa quebrada."
        )

        # Criando solicitações de recursos
        recurso1 = SolicitacaoRecursos(
            reserva_id=2,
            recursos="Projetor, Teclado",
            itens_nao_listados="Extensão elétrica",
            observacoes="Para aula prática"
        )
#        recurso2 = SolicitacaoRecursos(
#            reserva_id=3,
#            descricao="Necessidade de cadeiras extras.",
#            quantidade=5
#        )

        db.session.add_all([manutencao1, recurso1])
        db.session.commit()
        yield 
        db.session.remove()
        db.drop_all()

@pytest.fixture
def contexto():
    return {}