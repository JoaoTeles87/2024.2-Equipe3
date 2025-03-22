import sys
import os
from pathlib import Path
import json
import pytest
from datetime import datetime, time
from pytest_bdd import scenarios, given, when, then

# Adiciona o diretório raiz do projeto ao PATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importações do Flask e do projeto
from flask import Flask
from modelo.extensao import db
from modelo.usuario import Usuario
from modelo.sala_perfil import Sala
from modelo.reserva_perfil import Reserva
from rotas.exclusao_perfil import exclusao_perfil_bp

# Carrega os cenários do arquivo .feature
scenarios('features/deletarPerfil.feature')

# Fixture para configurar a aplicação e o banco de dados
@pytest.fixture(scope="module")
def app():
    # Criação da aplicação Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    # Inicializa o SQLAlchemy corretamente
    db.init_app(app)  # Inicializa a extensão com o app

    # Registra o blueprint
    app.register_blueprint(exclusao_perfil_bp)

    # Cria o banco de dados na inicialização
    with app.app_context():
        db.create_all()  # Cria as tabelas

    return app

# Fixture para criar um cliente de teste
@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            setup_teardown(client)  # Certifica-se de que o setup/teardown está no contexto
        yield client

# Função para limpar o banco de dados antes de cada teste
def setup_teardown(client):
    with client.application.app_context():  # Garante que o contexto do app seja usado
        db.session.query(Reserva).delete()
        db.session.query(Sala).delete()
        db.session.query(Usuario).delete()
        db.session.commit()

# Cenário 1 - Deletar perfil com sucesso
@given('o aluno João deseja excluir seu perfil e não possui reservas ativas')
def aluno_sem_reservas_ativas(client):
    with client.application.app_context():
        usuario = Usuario(nome="João", email="joao@email.com", cpf="123.456.789-00", professor="N", senha="senha123")
        db.session.add(usuario)
        db.session.commit()

@when('ele envia uma requisição DELETE para "/api/perfil" com o ID "1" e a senha "senha123"', target_fixture="enviar_requisicao_delete_sucesso")
def enviar_requisicao_delete_sucesso(client):
    return client.delete("/api/perfil", json={"id": 1, "senha": "senha123"})

@then('o sistema retorna a mensagem "Perfil excluído com sucesso!" e o status 200 OK')
def validar_exclusao_sucesso(enviar_requisicao_delete_sucesso):
    response = enviar_requisicao_delete_sucesso
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Perfil excluído com sucesso!" in data["message"]

# Cenário 2 - Tentativa de deletar perfil com reservas ativas
@given('o aluno João tem reservas ativas no sistema')
def aluno_com_reservas_ativas(client):
    with client.application.app_context():
        usuario = Usuario(nome="João", email="joao@email.com", cpf="123.456.789-00", professor="N", senha="senha123")
        db.session.add(usuario)
        db.session.commit()

        sala = Sala(nome="Sala 1", capacidade=30, data_criacao=datetime.now())
        db.session.add(sala)
        db.session.commit()

        reserva = Reserva(usuario_id=usuario.id, sala_id=sala.id, data=datetime.now().date(), horario_inicio=time(8, 0), horario_fim=time(10, 0), ativa=True)
        db.session.add(reserva)
        db.session.commit()

@when('ele tenta excluir seu perfil enviando uma requisição DELETE para "/api/perfil" com o ID "1" e a senha "senha123"', target_fixture="enviar_requisicao_delete_reservas_ativas")
def enviar_requisicao_delete_reservas_ativas(client):
    return client.delete("/api/perfil", json={"id": 1, "senha": "senha123"})

@then('o sistema retorna a mensagem "Não é possível excluir o perfil com reservas ativas" e o status 400 BAD REQUEST')
def validar_exclusao_com_reservas_ativas(enviar_requisicao_delete_reservas_ativas):
    response = enviar_requisicao_delete_reservas_ativas
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Não é possível excluir o perfil com reservas ativas" in data["error"]

# Cenário 3 - Tentativa de deletar perfil com ID incorreto
@given('o aluno João tenta excluir o perfil com o ID incorreto')
def aluno_tenta_excluir_com_id_incorreto(client):
    with client.application.app_context():
        usuario = Usuario(nome="João", email="joao@email.com", cpf="123.456.789-00", professor="N", senha="senha123")
        db.session.add(usuario)
        db.session.commit()

@when('ele envia uma requisição DELETE para "/api/perfil" com o ID "999" e a senha "senha123"', target_fixture="enviar_requisicao_delete_id_incorreto")
def enviar_requisicao_delete_id_incorreto(client):
    return client.delete("/api/perfil", json={"id": 999, "senha": "senha123"})

@then('o sistema retorna a mensagem "Perfil não encontrado para o ID fornecido" e o status 404 NOT FOUND')
def validar_exclusao_com_id_incorreto(enviar_requisicao_delete_id_incorreto):
    response = enviar_requisicao_delete_id_incorreto
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "Perfil não encontrado para o ID fornecido" in data["error"]

# Cenário 4 - Tentativa de deletar perfil com senha errada
@given('o aluno João tenta excluir o perfil com a senha errada')
def aluno_tenta_excluir_com_senha_errada(client):
    with client.application.app_context():
        usuario = Usuario(nome="João", email="joao@email.com", cpf="123.456.789-00", professor="N", senha="senha123")
        db.session.add(usuario)
        db.session.commit()

@when('ele envia uma requisição DELETE para "/api/perfil" especificando o ID "1" e a senha errada "senhaErrada"', target_fixture="enviar_requisicao_delete_senha_errada")
def enviar_requisicao_delete_senha_errada(client):
    return client.delete("/api/perfil", json={"id": 1, "senha": "senhaErrada"})

@then('o sistema retorna a mensagem "Senha incorreta" e o status 401 UNAUTHORIZED')
def validar_exclusao_com_senha_errada(enviar_requisicao_delete_senha_errada):
    response = enviar_requisicao_delete_senha_errada
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "Senha incorreta" in data["error"]
