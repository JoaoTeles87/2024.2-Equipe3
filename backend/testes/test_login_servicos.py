from pytest_bdd import scenario, given, when, then, parsers
import pytest

# Cenários de teste_
@scenario("../features/loginServico.feature", "Sucesso no login")
def teste_SucessoLogin():
    pass

@scenario("../features/loginServico.feature", "Fracasso no login por senha incorreta")
def teste_FracassoLogin():
    pass

@scenario("../features/loginServico.feature", "Fracasso no login por falta de email ou senha")
def teste_FracassoLoginSemEmailOuSenha():
    pass

# Given
@given(parsers.parse('o usuário possui o email "{email}" e a senha "{senha}" válidos'))
def usuarioCredenciais(contexto, email, senha):
    contexto["email"] = email
    contexto["senha"] = senha

@given(parsers.parse('o usuário possui o email "{email}" válido e a senha "{senha}" inválida'))
def usuarioSenhaInvalida(contexto, email, senha):
    contexto["email"] = email
    contexto["senha"] = senha

@given("o usuário envia uma requisição sem email ou senha")
def usuarioSemCredenciais(contexto):
    contexto["email"] = ""
    contexto["senha"] = ""

# When
@when(parsers.parse('ele envia uma requisição POST para "/api/login" com os dados "{email}" e "{senha}"'))
def enviarRequisicaoLogin(client, contexto, email, senha):
    resposta = client.post("/api/login", json={"email": email, "senha": senha})
    contexto["resposta"] = resposta


                                
# Then
@then(parsers.parse('a resposta deve conter o email "{email}" e a mensagem "success" igual a True'))
def verificarRespostaSucesso(contexto, email):
    respostaJson = contexto["resposta"].get_json()
    assert respostaJson["usuario"]["email"] == email, f"Esperado: {email}, Recebido: {respostaJson}"
    assert respostaJson["success"] == True, f"Esperado: True, Recebido: {respostaJson['success']}"

@then(parsers.parse('a resposta deve conter a mensagem "{mensagem}"'))
def verificarRespostaFalha(contexto, mensagem):
    respostaJson = contexto["resposta"].get_json()
    assert respostaJson["error"] == mensagem, f"Esperado: {mensagem}, Recebido: {respostaJson}"
    

@then(parsers.parse('o status code deve ser "{status_code}"'))
def verificarStatusCode(contexto, status_code):
    status_code = int(status_code)
    assert contexto["resposta"].status_code == status_code, f"Esperado: {status_code}, Recebido: {contexto['resposta'].status_code}"
