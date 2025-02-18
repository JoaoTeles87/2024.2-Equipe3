import sys
import os
from pathlib import Path
import json
import pytest
from datetime import datetime, time, timezone
from pytest_bdd import scenarios, given, when, then
import random

# Adiciona o diretório raiz do projeto ao PATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importações do projeto
from modelo import create_app
from modelo.extensao import db
from modelo.reserva import Reserva
from modelo.usuario import Usuario
from modelo.sala import Sala

# Carrega os cenários do arquivo .feature
scenarios('features/deletarPerfil.feature')

# Função para limpar o banco de dados antes de cada teste
def setup_teardown():
    print("Limpando banco de dados...")
    db.session.query(Reserva).delete()
    db.session.query(Sala).delete()
    db.session.query(Usuario).delete()
    db.session.commit()

# Fixture para configurar a aplicação e o banco de dados
@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        setup_teardown()

# Fixture para criar um cliente de teste
@pytest.fixture
def client(app):
    with app.app_context():
        setup_teardown()
    return app.test_client()

# Cenário 1 - Deletar perfil com sucesso
@given('o aluno João deseja excluir seu perfil e não possui reservas ativas')
def aluno_sem_reservas_ativas(client):
    with client.application.app_context():
        usuario = Usuario(
            nome="João",
            email="joao@email.com",
            cpf="123.456.789-00",
            professor="N",
            senha="senha123"
        )
        db.session.add(usuario)
        db.session.commit()

@when('ele envia uma requisição DELETE para "/api/perfil" com o ID "1" e a senha "senha123"', target_fixture="enviar_requisicao_delete")
def enviar_requisicao_delete(client):
    data = {"id": 1, "senha": "senha123"}
    return client.delete("/api/perfil", json=data)

@then('o sistema retorna a mensagem "Perfil excluído com sucesso!" e o status 200 OK')
def validar_exclusao_sucesso(enviar_requisicao_delete):
    response = enviar_requisicao_delete
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Perfil excluído com sucesso" in data["message"]

# Cenário 2 - Tentativa de deletar perfil com reservas ativas
@given('o aluno João tem reservas ativas no sistema')
def aluno_com_reservas_ativas(client):
    with client.application.app_context():
        usuario = Usuario(
            nome="João",
            email="joao@email.com",
            cpf="123.456.789-00",
            professor="N",
            senha="senha123"
        )
        db.session.add(usuario)
        db.session.commit()

        sala = Sala(
            nome="Sala 1",
            capacidade=30,
            data_criacao=datetime.now()
        )
        db.session.add(sala)
        db.session.commit()

        reserva = Reserva(
            usuario_id=usuario.id,
            sala_id=sala.id,
            data=datetime.now().date(),
            horario_inicio=time(8, 0),
            horario_fim=time(10, 0),
            ativa=True
        )
        db.session.add(reserva)
        db.session.commit()

@when('ele tenta excluir seu perfil enviando uma requisição DELETE para "/api/perfil" com o ID "1" e a senha "senha123"', target_fixture="enviar_requisicao_delete_reservas_ativas")
def enviar_requisicao_delete_reservas_ativas(client):
    data = {"id": 1, "senha": "senha123"}
    return client.delete("/api/perfil", json=data)

@then('o sistema retorna a mensagem "Não é possível excluir o perfil com reservas ativas" e o status 400 BAD REQUEST')
def validar_exclusao_com_reservas_ativas(enviar_requisicao_delete_reservas_ativas):
    response = enviar_requisicao_delete_reservas_ativas
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Não é possível excluir o perfil com reservas ativas" in data["error"]

# Cenário 3 - Tentativa de deletar perfil com ID de usuário incorreto
@given('o aluno João tenta excluir o perfil com a senha errada')
def aluno_tenta_excluir_com_senha_errada(client):
    with client.application.app_context():
        usuario = Usuario(
            nome="João",
            email="joao@email.com",
            cpf="123.456.789-00",
            professor="N",
            senha="senha123"
        )
        db.session.add(usuario)
        db.session.commit()

@when('ele envia uma requisição DELETE para "/api/perfil" especificando o ID "999" e a senha errada "senhaErrada"', target_fixture="enviar_requisicao_delete_senha_errada")
def enviar_requisicao_delete_senha_errada(client):
    data = {"id": 999, "senha": "senhaErrada"}
    return client.delete("/api/perfil", json=data)

@then('o sistema retorna a mensagem "Perfil não encontrado para o ID fornecido" e o status 404 NOT FOUND')
def validar_exclusao_com_senha_errada(enviar_requisicao_delete_senha_errada):
    response = enviar_requisicao_delete_senha_errada
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"].strip() == "Perfil não encontrado para o ID fornecido"

# Cenário 4 - Tentativa de deletar perfil com senha errada
@given('o aluno João tenta excluir o perfil com a senha errada')
def aluno_tenta_excluir_com_senha_errada(client):
    with client.application.app_context():
        usuario = Usuario(
            nome="João",
            email="joao@email.com",
            cpf="123.456.789-00",
            professor="N",
            senha="senha123"
        )
        db.session.add(usuario)
        db.session.commit()

@when('ele envia uma requisição DELETE para "/api/perfil" especificando o ID "1" e a senha errada "senhaErrada"', target_fixture="enviar_requisicao_delete_senha_errada")
def enviar_requisicao_delete_senha_errada(client):
    data = {"id": 1, "senha": "senhaErrada"}  # ID correto, mas senha errada
    return client.delete("/api/perfil", json=data)

@then('o sistema retorna a mensagem "Senha incorreta" e o status 401 UNAUTHORIZED')
def validar_exclusao_com_senha_errada(enviar_requisicao_delete_senha_errada):
    response = enviar_requisicao_delete_senha_errada
    assert response.status_code == 401  # Status esperado para senha incorreta
    data = json.loads(response.data)
    assert data["error"].strip() == "Senha incorreta."