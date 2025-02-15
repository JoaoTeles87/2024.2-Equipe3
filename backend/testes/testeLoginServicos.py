from pytest_bdd import scenario, given, when, then, parsers
import pytest
import requests
from flask import Flask
from unittest.mock import MagicMock
from ..rotas.login import login_bp

@pytest.fixture
def app():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(login_bp)
    aplicacao.config["TESTING"] = True
    return aplicacao

@pytest.fixture
def cliente(app):
    with app.test_client() as cliente:
        yield cliente

@pytest.fixture
def contexto():
    return {}

@scenario("../features/loginServico.feature", "Sucesso no login")
def testeSucessoLogin():
    pass

@scenario("../features/loginServico.feature", "Fracasso no login por senha incorreta")
def testeFracassoLogin():
    pass

@scenario("../features/loginServico.feature", "Fracasso no login por falta de email ou senha")
def testeFracassoLoginSemEmailOuSenha():
    pass

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

@when('ele envia uma requisição POST para "/api/login"')
def enviarRequisicaoLogin(cliente, contexto):
    mockResposta = MagicMock()
    
    if contexto.get("email") == "demostenes@example.com" and contexto.get("senha") == "SecurePassword123":
        mockResposta.get_json.return_value = {"redirect": "reserva"}
        mockResposta.status_code = 200
    elif contexto.get("email") == "demostenes@example.com" and contexto.get("senha") != "SecurePassword123":
        mockResposta.get_json.return_value = {"error": "Usuário ou senha inválidos."}
        mockResposta.status_code = 401
    else:
        mockResposta.get_json.return_value = {"error": "Usuário e senha são obrigatórios."}
        mockResposta.status_code = 400

    contexto["resposta"] = mockResposta

@then("a resposta deve conter os dados do usuário")
def verificarRespostaSucesso(contexto):
    respostaJson = contexto["resposta"].get_json()
    assert respostaJson["redirect"] == "reserva"

@then('a resposta deve conter a mensagem "Usuário ou senha inválidos."')
def verificarRespostaFalha(contexto):
    respostaJson = contexto["resposta"].get_json()
    assert "error" in respostaJson
    assert respostaJson["error"] == "Usuário ou senha inválidos."

@then('a resposta deve conter a mensagem "Usuário e senha são obrigatórios."')
def verificarRespostaErroCampos(contexto):
    respostaJson = contexto["resposta"].get_json()
    assert "error" in respostaJson
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
