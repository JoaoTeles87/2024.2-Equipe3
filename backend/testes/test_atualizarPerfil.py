# testes/teste.py

import sys
import os
from pathlib import Path
import json
import pytest
from pytest_bdd import scenarios, given, when, then
import random
from flask import Flask

# Adiciona o diretório raiz do projeto ao PATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importações do projeto
from backend.modelo.extensao import db  # Aqui é onde o db é importado corretamente
from backend.modelo.usuario import Usuario
from backend.rotas.atualizar_perfil import atualizar_perfil_bp  # Importa o Blueprint corretamente

# Função para gerar um e-mail único para cada execução de teste
def gerar_email_unico():
    return f"test_{random.randint(1000, 9999)}@email.com"

# Cenários definidos no arquivo .feature
scenarios('features/atualizarPerfil.feature')

@pytest.fixture(scope="session")  # Criar uma única instância para todos os testes
def app():
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    app.config['TESTING'] = True
    app.register_blueprint(atualizar_perfil_bp)  

    db.init_app(app)  # Inicializa o db com o app

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco em memória

        # Geração de um usuário para os testes
        email_unico = gerar_email_unico()
        usuario = Usuario(
            email=email_unico,
            nome="João Teste",
            cpf="123.456.789-00",
            senha="senha123",
            professor="N"
        )
        db.session.add(usuario)
        db.session.commit()

    yield app

    with app.app_context():  
        db.drop_all()  # Remove todas as tabelas após os testes

@pytest.fixture
def client(app):
    return app.test_client()

# Fixture para enviar requisição de atualizar perfil
@pytest.fixture
def enviar_requisicao_atualizar_perfil(client, app):
    with app.app_context():  
        usuario = Usuario.query.first()  # Busca o usuário gerado para o teste
    
    dados_atualizados = {
        "nome": "João Pereira",
        "cpf": "987.654.321-00",
        "email": "email@email.com", 
        "nova_senha": "novaSenha123"
    }
    return client.put("/api/perfil", json=dados_atualizados)

# Fixture para enviar requisição com CPF inválido
@pytest.fixture
def enviar_requisicao_com_cpf_invalido(client):
    dados_invalidos = {
        "nome": "João Teste",
        "cpf": "123",  # CPF inválido
        "email": "teste@email.com",
        "nova_senha": "senha123"
    }
    return client.put("/api/perfil", json=dados_invalidos)

# Fixture para enviar requisição com nome inválido (corrigido CPF para ser válido)
@pytest.fixture
def enviar_requisicao_com_nome_invalido(client):
    dados_invalidos_nome = {
        "nome": "A",  # Nome inválido
        "cpf": "987.654.321-00",  # CPF válido para evitar erro de CPF primeiro
        "email": "teste@email.com",
        "nova_senha": "senha123"
    }
    return client.put("/api/perfil", json=dados_invalidos_nome)

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

# Cenário 2 - Atualizar perfil com CPF inválido
@given('o aluno João deseja editar seu perfil')
def dado_usuario_joao_para_cpf_invalido():
    pass

@when('ele envia uma requisição PUT para "/api/perfil" especificando CPF "123"')  
def quando_enviar_requisicao_com_cpf_invalido(enviar_requisicao_com_cpf_invalido):
    return enviar_requisicao_com_cpf_invalido

@then('o sistema retorna a mensagem "O CPF fornecido é inválido." e o status 400 BAD REQUEST')
def verificar_mensagem_erro(enviar_requisicao_com_cpf_invalido):
    response = enviar_requisicao_com_cpf_invalido 
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["error"] == "O CPF fornecido é inválido."

# Cenário 3 - Atualizar perfil com nome inválido
@given('o aluno João deseja editar seu perfil')
def dado_usuario_joao_para_nome_invalido():
    pass

@when('ele envia uma requisição PUT para "/api/perfil" especificando o nome "A"')  # Ajuste no texto do step
def quando_enviar_requisicao_com_nome_invalido(enviar_requisicao_com_nome_invalido):
    return enviar_requisicao_com_nome_invalido

@then('o sistema retorna a mensagem "O nome é inválido. Deve conter apenas letras e espaços, e ter pelo menos 2 caracteres." e o status 400 BAD REQUEST')
def entao_validar_nome_invalido(enviar_requisicao_com_nome_invalido):
    response = enviar_requisicao_com_nome_invalido
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "O nome é inválido. Deve conter apenas letras e espaços, e ter pelo menos 2 caracteres."
