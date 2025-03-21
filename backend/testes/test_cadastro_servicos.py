from pytest_bdd import scenario, given, when, then, parsers
import pytest

# Cenários de teste_
@scenario("../features/CadastroServico.feature", "Sucesso no cadastro de usuário")
def teste_SucessoUsuario():
    pass

@scenario("../features/CadastroServico.feature", "Sucesso no cadastro de professor")
def teste_SucessoProfessor():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por campos obrigatórios não preenchidos")
def teste_ErroObrigatorio():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por siape já registrado")
def teste_ErroSiapeRegistrado():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por duplicação de ID única")
def teste_ErroCadastroDuplo():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por senhas que não coincidem")
def teste_ErroCadastroSenha():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por formato inválido de email")
def teste_ErroEmailInvalido():
    pass

@scenario("../features/CadastroServico.feature", "Fracasso no cadastro por formato inválido de CPF")
def teste_ErroCpfInvalido():
    pass

# Given
@given("o usuário deseja se cadastrar")
def usuarioInicioCadastro(contexto):
    contexto["dados_cadastro"] = {}

# When
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

@when(parsers.parse('ele envia uma requisição POST para "/cadastro"'))
def enviarCadastro(client, contexto):
    resposta = client.post("/cadastro", json=contexto["dados_cadastro"])
    contexto["resposta"] = resposta
    
@when(parsers.parse('ele deixa o campo "Confirmar Senha" com ""'))
def senhaVazio(contexto):
    pass
# Then
@then(parsers.parse('a resposta deve conter a mensagem "{mensagem}"'))
def verificarMensagem(contexto, mensagem):
    resposta_json = contexto["resposta"].get_json()
    mensagem_real = resposta_json.get("message") or resposta_json.get("error")
    assert mensagem_real == mensagem, f"Esperado: {mensagem}, Recebido: {mensagem_real}"

@then(parsers.parse('o status code deve ser "{status_code}"'))
def verificarStatusCode(contexto, status_code):
    status_code = int(status_code)
    assert contexto["resposta"].status_code == status_code, f"Esperado: {status_code}, Recebido: {contexto['resposta'].status_code}"
