import pytest
from flask import Flask
from ..rotas.cadastro import cadastro_bp
from ..rotas.login import login_bp
from ..modelo.extensao import db
from ..modelo.usuario import Usuario
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def app():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(cadastro_bp)
    aplicacao.register_blueprint(login_bp)
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

        db.session.add_all([usuario1, usuario2])
        db.session.commit()        
        yield 
        db.session.remove()
        db.drop_all()

@pytest.fixture
def contexto():
    return {}
