from pytest_bdd import scenario, given, when, then, parsers
import pytest
from flask import Flask
from ..rotas.login import login_bp
from ..modelo.extensao import db
from ..modelo.usuario import Usuario
from werkzeug.security import generate_password_hash

# Criando um app Flask para testar a API
@pytest.fixture
def app():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(login_bp)
    aplicacao.config["TESTING"] = True
    aplicacao.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Banco de testes
    aplicacao.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with aplicacao.app_context():
        db.init_app(aplicacao)       
        db.create_all()  # Garante que as tabelas são criadas antes dos testes
        yield aplicacao  # Executa os testes
        db.session.remove()
        db.drop_all()


# Fixture para simular o cliente de testes
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_database(app):
    """Popula o banco de dados com um usuário de teste."""
    with app.app_context():
        usuario = Usuario(
            nome="Demosténes",
            cpf="126.456.789-00",
            email="demostenes@example.com",
            professor="N",
            siape=None,
            senha=generate_password_hash("SecurePassword123")
        )
        db.session.add(usuario)
        db.session.commit()
    

# Fixture para armazenar contexto entre os testes
@pytest.fixture
def contexto():
    return {}

# Cenários de teste
@scenario("../features/loginServico.feature", "Sucesso no login")
def testeSucessoLogin():
    pass

@scenario("../features/loginServico.feature", "Fracasso no login por senha incorreta")
def testeFracassoLogin():
    pass

@scenario("../features/loginServico.feature", "Fracasso no login por falta de email ou senha")
def testeFracassoLoginSemEmailOuSenha():
    pass

# GIVEN: Configuração inicial do teste
@given("o usuário possui um email e senha válidos")
def usuarioValido(contexto):
    contexto["email"] = "demostenes@example.com"
    contexto["senha"] = "SecurePassword123"

@given("o usuário possui um email válido, mas senha inválida")
def usuarioSenhaInvalida(contexto):
    contexto["email"] = "demostenes@example.com"
    contexto["senha"] = "SenhaIncorreta123"

@given("o usuário envia uma requisição sem email ou senha")
def usuarioSemCredenciais(contexto):
    contexto["email"] = ""
    contexto["senha"] = ""

# WHEN: Envio da requisição de login
@when('ele envia uma requisição POST para "/api/login"')
def enviarRequisicaoLogin(client, setup_database, contexto):
    """Realiza uma requisição POST real para a API de login"""

    resposta = client.post("/api/login", json={
        "email": contexto["email"],
        "senha": contexto["senha"]
    })
    contexto["resposta"] = resposta


# THEN: Validações das respostas
@then("a resposta deve conter os dados do usuário")
def verificarRespostaSucesso(contexto):
    respostaJson = contexto["resposta"].get_json()
   
    assert respostaJson["redirect"] == "reserva", f"Esperado: reserva, Recebido: {respostaJson}"

@then('a resposta deve conter a mensagem "Usuário ou senha inválidos."')
def verificarRespostaFalha(contexto):
    respostaJson = contexto["resposta"].get_json()
    assert respostaJson["error"] == "Usuário ou senha inválidos."

@then('a resposta deve conter a mensagem "Usuário e senha são obrigatórios."')
def verificarRespostaErroCampos(contexto):
    respostaJson = contexto["resposta"].get_json()
    assert respostaJson["error"] == "Usuário e senha são obrigatórios."

@then("o status code deve ser 200")
def verificarStatusCode200(contexto):
    assert contexto["resposta"].status_code == 200

@then("o status code deve ser 401")
def verificarStatusCode401(contexto):
    assert contexto["resposta"].status_code == 401

@then("o status code deve ser 400")
def verificarStatusCode400(contexto):
    assert contexto["resposta"].status_code == 400
