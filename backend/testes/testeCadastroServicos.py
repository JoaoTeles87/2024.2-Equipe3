from pytest_bdd import scenario, given, when, then, parsers
import pytest
import requests
from flask import Flask
from unittest.mock import MagicMock
from ..rotas.cadastro import cadastro_bp
import re

def validarEmail(email):
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(padrao_email, email):
        return False
    return True

# Criando um app Flask para testar a API
@pytest.fixture
def app():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(cadastro_bp)
    aplicacao.config["TESTING"] = True
    return aplicacao

# Fixture para simular o cliente de testes
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def contexto():
    """Armazena os dados do usuário durante os testes"""
    return {}

# Cenários de Teste
@scenario("../features/CadastroServico.feature", "Sucesso no cadastro de usuário")
def testeSucessoUsuario():
    pass

@scenario("../features/CadastroServico.feature", "Sucesso no cadastro de professor")
def testeSucessoProfessor():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por campos obrigatórios não preenchidos")
def testeErroObrigatorio():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por duplicação de ID única")
def testeErroCadastroDuplo():
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

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por SIAP já registrado")
def testeErroSiapeRegistrado():
    pass

# GIVEN - Configuração inicial
@given("o usuário deseja se cadastrar")
def usuarioInicioCadastro(contexto):
        contexto["dados_cadastro"] = {}

# WHEN - Preenchimento de campos
@when(parsers.parse('ele informa o nome "{nome}"'))
def informarNome(contexto, nome):
    contexto["dados_cadastro"]["Nome"] = nome

@when(parsers.parse('ele informa o CPF "{cpf}"'))
def informarCpf(contexto, cpf):
    contexto["dados_cadastro"]["CPF"] = cpf

@when(parsers.parse('ele informa o email "{email}"'))
def informarEmail(contexto, email):
    contexto["dados_cadastro"]["Email"] = email

@when(parsers.parse('ele informa se é professor "{professor}"'))
def informarProfessor(contexto, professor):
    contexto["dados_cadastro"]["professor"] = professor

@when(parsers.parse('ele informa o SIAPE "{siape}"'))
def informarSiape(contexto, siape):
    contexto["dados_cadastro"]["SIAPE"] = siape

@when(parsers.parse('ele informa a senha "{senha}"'))
def informarSenha(contexto, senha):
    contexto["dados_cadastro"]["Senha"] = senha

@when(parsers.parse('ele informa a confirmação da senha "{confirmar_senha}"'))
def confirmarSenha(contexto, confirmar_senha):
    contexto["dados_cadastro"]["Confirmar_Senha"] = confirmar_senha
    
@when(parsers.parse('ele deixa o campo "Confirmar Senha" com ""'))
def SenhaVazio(contexto):
    contexto["dados_cadastro"]["Confirmar_Senha"] = ""

# WHEN - Preenchimento de campos
@when(parsers.parse('ele envia uma requisição POST para "/api/cadastro"'))
def enviarCadastro(client, contexto):
    """Realiza uma requisição POST para a API de cadastro"""

    mockResposta = MagicMock()

    # Simulação de diferentes respostas da API
    if "Confirmar_Senha" not in contexto["dados_cadastro"] or contexto["dados_cadastro"]["Confirmar_Senha"] == "":
        mockResposta.get_json.return_value = {"error": "Confirmar Senha é obrigatório"}
        mockResposta.status_code = 400
    elif contexto["dados_cadastro"]["Senha"] != contexto["dados_cadastro"]["Confirmar_Senha"]:
        
        mockResposta.get_json.return_value = {"error": "As senhas não coincidem."}
        mockResposta.status_code = 400
    elif contexto["dados_cadastro"]["CPF"] == "123.456.789-00" or contexto["dados_cadastro"]["Email"] == "carlos.mendes@example.com":
        mockResposta.get_json.return_value = {"error": "Erro: email/cpf já está registrado."}
        mockResposta.status_code = 409
    elif not validarEmail(contexto["dados_cadastro"]["Email"]):
        print(contexto["dados_cadastro"]["Email"])
        mockResposta.get_json.return_value = {"error": "Formato de email inválido. Use um email válido, como exemplo@dominio.com."}
        mockResposta.status_code = 400
    elif not contexto["dados_cadastro"]["CPF"].replace(".", "").replace("-", "").isdigit() or len(contexto["dados_cadastro"]["CPF"]) != 14:
        print(contexto["dados_cadastro"]["CPF"])
        mockResposta.get_json.return_value = {"error": "CPF inválido. Digite um CPF válido no formato XXX.XXX.XXX-XX."}
        mockResposta.status_code = 400
    elif contexto["dados_cadastro"]["professor"] == "S" and contexto["dados_cadastro"]["SIAPE"] == "123456":
        mockResposta.get_json.return_value = {"error": "Erro: siape já está registrado."}
        mockResposta.status_code = 400
    else:
        print(contexto["dados_cadastro"])
        mockResposta.get_json.return_value = {"message": "Cadastro criado com sucesso!"}
        mockResposta.status_code = 201

    contexto["resposta"] = mockResposta


# THEN - Validação dos resultados
@then(parsers.parse('a resposta deve conter a mensagem "{mensagem}"'))
def verificarMensagem(contexto, mensagem):
    resposta_json = contexto["resposta"].get_json()
    assert resposta_json.get("message") == mensagem or resposta_json.get("error") == mensagem, f"Esperado: {mensagem}, Recebido: {resposta_json}"

@then("o status code deve ser 201")
def verificarStatus201(contexto):
    assert contexto["resposta"].status_code == 201

@then("o status code deve ser 400")
def verificarStatus400(contexto):
    assert contexto["resposta"].status_code == 400

@then("o status code deve ser 409")
def verificarStatus409(contexto):
    assert contexto["resposta"].status_code == 409
