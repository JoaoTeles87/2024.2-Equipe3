import pytest
from flask import Flask
from backend.rotas.criar_solicitacao_manutencao import criar_manutencao_bp
from backend.rotas.criar_solicitacao_recursos import criar_recursos_bp
from backend.rotas.editar_solicitacao_manutencao import editar_manutencao_bp
from backend.rotas.editar_solicitacao_recursos import editar_recursos_bp
from backend.rotas.excluir_solicitacao_manutencao import excluir_manutencao_bp
from backend.rotas.excluir_solicitacao_recursos import excluir_recursos_bp
from backend.rotas.criarReview import criar_review_bp
from backend.rotas.atualizarReview import atualizar_review_bp
from backend.rotas.deletarReview import deletar_review_bp
from backend.rotas.obterReview import obter_review_bp
from backend.modelo.extensao import db
from backend.modelo.solicitacaomanutencao import SolicitacaoManutencao
from backend.modelo.solicitacaorecursos import SolicitacaoRecursos
from backend.modelo.reviewSala import ReviewSala
from backend.modelo.sala import Sala
from backend.modelo.reserva import Reserva
from ..rotas.cadastro import cadastro_bp
from ..rotas.login import login_bp
from ..modelo.extensao import db
from ..modelo.usuario import Usuario
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
    aplicacao.register_blueprint(cadastro_bp)
    aplicacao.register_blueprint(login_bp)
    aplicacao.register_blueprint(criar_review_bp)
    aplicacao.register_blueprint(atualizar_review_bp)
    aplicacao.register_blueprint(deletar_review_bp)
    aplicacao.register_blueprint(obter_review_bp)
    aplicacao.config["TESTING"] = True
    aplicacao.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
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
    """Popula o banco de dados com usuários de teste antes dos testes rodarem."""
    with app.app_context():
        db.create_all()
        
        usuario1 = Usuario(
            nome="Demosténes",
            cpf="126.456.789-00",
            email="demostenes@example.com",
            professor="N",
            siape=None,
            senha=generate_password_hash("SecurePassword123"),
        )

        usuario2 = Usuario(
            nome="Vanessa",
            cpf="321.879.789-33",
            email="vanessa@example.com",
            professor="S",
            siape="101010",
            senha=generate_password_hash("12345678"),
        )
        
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
        db.session.add_all([usuario1, usuario2])
        db.session.commit()        
        yield 
        db.session.remove()
        db.drop_all()

@pytest.fixture
def contexto():
    return {}

@pytest.fixture
def criar_review(app):
    with app.app_context():
        review = ReviewSala(
            reserva_id=1,
            sala_id=2,
            usuario_id=3,
            nota=4,
            comentario="Sala boa, mas com algumas falhas.",
        )
        db.session.add(review)
        db.session.commit()
        db.session.refresh(review)
        return review