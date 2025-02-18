import sys
import os
from pathlib import Path
import json
import pytest
from pytest_bdd import scenarios, given, when, then
import random

# Adiciona o diretório raiz do projeto ao PATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importações do projeto
from modelo.extensao import db
from modelo.usuario import Usuario

# Função para gerar um e-mail único para cada execução de teste
def gerar_email_unico():
    return f"test_{random.randint(1000, 9999)}@email.com"

# Cenários definidos no arquivo .feature
scenarios('features/atualizarPerfil.feature')


@pytest.fixture
def client(app):
    return app.test_client()

# Fixture para enviar requisição de atualizar perfil
@pytest.fixture
def enviar_requisicao_atualizar_perfil(client, app):
    with app.app_context():  
        usuario = Usuario.query.first()  # Pega o primeiro usuário (o único, pois estamos usando banco em memória)
    
    dados_atualizados = {
        "nome": "João Pereira",
        "cpf": "987.654.321-00",
        "email": "email@email.com", 
        "nova_senha": "novaSenha123"
    }
    return client.put("/api/perfil", json=dados_atualizados)

# Fixture para enviar requisição com dados inválidos
@pytest.fixture
def enviar_requisicao_com_dados_invalidos(client):
    dados_invalidos = {
        "nome": "A",  # Nome inválido
        "cpf": "123",  # CPF inválido
        "email": "teste@email.com",
        "nova_senha": "senha123"
    }
    return client.put("/api/perfil", json=dados_invalidos)

# Cenário 1 - Atualizar perfil existente
@given('o aluno João deseja editar seu perfil')
def dado_usuario_joao():
    pass

@when('ele envia uma requisição PUT para "/api/perfil" especificando as informações de perfil a serem editadas')
def quando_enviar_requisicao_atualizar_perfil(enviar_requisicao_atualizar_perfil):
    return enviar_requisicao_atualizar_perfil

@then('o sistema retorna a mensagem "Perfil atualizado com sucesso." e o status 200 OK')
def entao_validar_resposta_perfil_atualizado(enviar_requisicao_atualizar_perfil):
    response = enviar_requisicao_atualizar_perfil
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Perfil atualizado com sucesso!"

# Cenário 2 - Atualizar perfil com dados inválidos
@given('o aluno João deseja editar seu perfil')
def dado_usuario_joao_para_dados_invalidos():
    pass

@when('ele envia uma requisição PUT para "/api/perfil" especificando o nome "A" e o CPF "123"')
def quando_enviar_requisicao_com_dados_invalidos(enviar_requisicao_com_dados_invalidos):
    return enviar_requisicao_com_dados_invalidos

@then('o sistema retorna a mensagem "O CPF fornecido é inválido. Use o formato XXX.XXX.XXX-XX." e o status 400 BAD REQUEST')
def entao_validar_dados_invalidos(enviar_requisicao_com_dados_invalidos):
    response = enviar_requisicao_com_dados_invalidos
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "O CPF fornecido é inválido. Use o formato XXX.XXX.XXX-XX."
