from pytest_bdd import scenario, given, when, then, parsers
import pytest
from flask import Flask
import re
from ..rotas.cadastro import cadastro_bp
from ..modelo.extensao import db
from ..modelo.usuario import Usuario
from werkzeug.security import generate_password_hash


# 🏗 Criando um app Flask para testar a API
@pytest.fixture
def app():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(cadastro_bp)
    aplicacao.config["TESTING"] = True
    aplicacao.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Banco de testes
    aplicacao.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with aplicacao.app_context():
        db.init_app(aplicacao)  # Inicializa a extensão do banco
        db.create_all()
        yield aplicacao  # Executa os testes
        db.session.remove()
        db.drop_all()


@pytest.fixture
def setup_database(app):
    """Popula o banco de testes com usuários iniciais para os testes de duplicação."""
    with app.app_context():
        db.create_all()  # Certifica que as tabelas existem

        usuario1 = Usuario(
            nome="Demosténes",
            cpf="126.456.789-00",
            email="demostenes@example.com",
            professor="N",
            siape=None,
            senha=generate_password_hash("SecurePassword123")
        )

        usuario2 = Usuario(
            nome="Vanessa",
            cpf="321.879.789-33",
            email="vanessa@example.com",
            professor="S",
            siape="101010",
            senha=generate_password_hash("12345678")
        )

        db.session.add_all([usuario1, usuario2])
        db.session.commit()  # Confirma os cadastros no banco

        yield  # Libera para os testes rodarem

        db.session.remove()
        db.drop_all()  # Limpa o banco após os testes


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def contexto():
    return {}


@scenario("../features/CadastroServico.feature", "Sucesso no cadastro de usuário")
def testeSucessoUsuario():
    pass

@scenario("../features/CadastroServico.feature", "Sucesso no cadastro de professor")
def testeSucessoProfessor():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por campos obrigatórios não preenchidos")
def testeErroObrigatorio():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por senhas que não coincidem")
def testeErroCadastroSenha():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por formato inválido de email")
def testeErroEmailInvalido():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por formato inválido de CPF")
def testeErroCpfInvalido():
    pass


@pytest.mark.usefixtures("setup_database")
@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por siape já registrado")
def testeErroSiapeRegistrado():
    pass

@pytest.mark.usefixtures("setup_database")
@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por duplicação de ID única")
def testeErroCadastroDuplo():
    pass


@given("o usuário deseja se cadastrar")
def usuarioInicioCadastro(contexto):
    contexto["dados_cadastro"] = {}


@when(parsers.parse('ele informa o nome "{nome}"'))
def informarNome(contexto, nome):
    contexto["dados_cadastro"]["nome"] = nome

@when(parsers.parse('ele informa o CPF "{cpf}"'))
def informarCpf(contexto, cpf):
    contexto["dados_cadastro"]["cpf"] = cpf

@when(parsers.parse('ele informa o email "{email}"'))
def informarEmail(contexto, email):
    contexto["dados_cadastro"]["email"] = email

@when(parsers.parse('ele informa se é professor "{professor}"'))
def informarProfessor(contexto, professor):
    contexto["dados_cadastro"]["professor"] = professor

@when(parsers.parse('ele informa o SIAPE "{siape}"'))
def informarSiape(contexto, siape):
    contexto["dados_cadastro"]["siape"] = siape

@when(parsers.parse('ele informa a senha "{senha}"'))
def informarSenha(contexto, senha):
    contexto["dados_cadastro"]["senha"] = senha

@when(parsers.parse('ele informa a confirmação da senha "{confirmar_senha}"'))
def confirmarSenha(contexto, confirmar_senha):
    contexto["dados_cadastro"]["confirmarSenha"] = confirmar_senha

@when(parsers.parse('ele deixa o campo "Confirmar Senha" com ""'))
def senhaVazio(contexto):
    pass


@when(parsers.parse('ele envia uma requisição POST para "/api/cadastro"'))
def enviarCadastro(client, contexto):

    resposta = client.post("/api/cadastro", json=contexto["dados_cadastro"])
    contexto["resposta"] = resposta

@then(parsers.parse('a resposta deve conter a mensagem "{mensagem}"'))
def verificarMensagem(contexto, mensagem):
    resposta_json = contexto["resposta"].get_json()
    mensagem_real = resposta_json.get("message") or resposta_json.get("error")
    assert mensagem_real == mensagem, f"Esperado: {mensagem}, Recebido: {mensagem_real}"

@then("o status code deve ser 201")
def verificarStatus201(contexto):
    assert contexto["resposta"].status_code == 201

@then("o status code deve ser 400")
def verificarStatus400(contexto):
    assert contexto["resposta"].status_code == 400

@then("o status code deve ser 409")
def verificarStatus409(contexto):
    assert contexto["resposta"].status_code == 409
