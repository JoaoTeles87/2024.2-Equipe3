from pytest_bdd import scenario, given, when, then, parsers
import pytest
from flask import Flask
from ..rotas.login import login_bp
from ..modelo.extensao import db
from ..modelo.usuario import Usuario
from werkzeug.security import generate_password_hash

# Criando um app Flask para testar a API
@pytest.fixture(scope="module")  # Agora com escopo de módulo
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
@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_database(app):
    """Popula o banco de dados com um usuário de teste antes dos testes rodarem."""
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
        yield
        db.session.remove()
        db.drop_all()

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
@given(parsers.parse('o usuário possui o email "{email}" e a senha "{senha}" válidos'))
def usuarioCredenciais(contexto, email, senha):
    contexto["email"] = email
    contexto["senha"] = senha
    print(f"\n✅ [DEBUG] Configurando usuário para login: Email: {email}, Senha: {senha}")

@given(parsers.parse('o usuário possui o email "{email}" válido e a senha "{senha}" inválida'))
def usuarioSenhaInvalida(contexto, email, senha):
    contexto["email"] = email
    contexto["senha"] = senha

@given("o usuário envia uma requisição sem email ou senha")
def usuarioSemCredenciais(contexto):
    contexto["email"] = ""
    contexto["senha"] = ""

# WHEN: Envio da requisição de login
@when(parsers.parse('ele envia uma requisição POST para "/api/login" com os dados "{email}" e "{senha}"'), converters={"email": str, "senha": str})
def enviarRequisicaoLogin(client, contexto, email, senha):
    """Realiza uma requisição POST para a API de login, garantindo que valores vazios sejam tratados corretamente"""
    
    email = email if email else ''  # Garante string vazia se necessário
    senha = senha if senha else ''  

    print(f"\n🚀 [DEBUG] Enviando requisição para login | Email: {email if email else 'NÃO INFORMADO'} | Senha: {senha if senha else 'NÃO INFORMADO'}")

    resposta = client.post("/api/login", json={"email": email, "senha": senha})
    contexto["resposta"] = resposta

    print(f"🔹 [DEBUG] Status Code recebido: {resposta.status_code}")
    print(f"🔹 [DEBUG] Resposta JSON recebida: {resposta.get_json()}")


# THEN: Validações das respostas
@then("a resposta deve conter os dados do usuário")
def verificarRespostaSucesso(contexto):
    respostaJson = contexto["resposta"].get_json()
    print(f"✅ [DEBUG] Resposta esperada: redirect='reserva'")
    print(f"✅ [DEBUG] Resposta recebida: {respostaJson}")
    
    assert respostaJson["redirect"] == "reserva", f"Esperado: reserva, Recebido: {respostaJson}"

@then(parsers.parse('a resposta deve conter a mensagem "{mensagem}"'))
def verificarRespostaFalha(contexto, mensagem):
    respostaJson = contexto["resposta"].get_json()
    print(f"✅ [DEBUG] Verificando erro esperado: {mensagem}")
    print(f"✅ [DEBUG] Resposta recebida: {respostaJson}")

    assert respostaJson["error"] == mensagem, f"Esperado: {mensagem}, Recebido: {respostaJson}"

@then(parsers.parse('o status code deve ser "{status_code}"'))
def verificarStatusCode(contexto, status_code):
    status_code = int(status_code)  # Converte string para inteiro
    print(f"✅ [DEBUG] Verificando status code esperado: {status_code}")
    print(f"✅ [DEBUG] Status code recebido: {contexto['resposta'].status_code}")

    assert contexto["resposta"].status_code == status_code, f"Esperado: {status_code}, Recebido: {contexto['resposta'].status_code}"
