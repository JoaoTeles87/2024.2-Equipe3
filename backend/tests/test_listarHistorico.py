import sys
import os
from pathlib import Path
import json
import pytest
from datetime import datetime, time
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
scenarios('features/listarHistorico.feature')

# Função para limpar o banco de dados antes de cada teste
def setup_teardown():
    print("Limpando banco de dados...")
    db.session.query(Reserva).delete()
    db.session.query(Sala).delete()
    db.session.query(Usuario).delete()
    db.session.commit()

    # Verificar se não há reservas restantes
    reservas_restantes = db.session.query(Reserva).all()
    print(f"Reservas restantes após limpeza: {len(reservas_restantes)}")  # Log para verificar

# Função para gerar dados únicos para cada execução de teste
def gerar_cpf_unico():
    return str(random.randint(10000000000, 99999999999))

def gerar_email_unico():
    return f"joao{random.randint(1000, 9999)}@email.com"

# Fixture para configurar a aplicação e o banco de dados
@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['TESTING'] = True

    with app.app_context():  # Garantir o contexto da aplicação
        db.create_all()

        # Insere um usuário de teste
        usuario = Usuario(
            nome="João",
            email="teste@email.com",
            cpf="12345678901",
            professor="N",
            senha="senha123"
        )
        db.session.add(usuario)
        db.session.commit()

        # Insere uma sala fictícia
        sala = Sala(nome="Sala 1", capacidade=30, data_criacao=datetime.utcnow())
        db.session.add(sala)
        db.session.commit()

    yield app  # Faz o app ficar disponível para os testes

    with app.app_context():  # Garantir o contexto da aplicação para limpar o banco
        setup_teardown()

# Fixture para criar um cliente de teste
@pytest.fixture
def client(app):
    # Limpa o banco de dados antes de cada teste
    with app.app_context():
        setup_teardown()  # Chama a função que limpa o banco de dados
    return app.test_client()

# # Cenário 1 - Listar Histórico de Reservas com reservas
# @given('o aluno João deseja consultar o histórico de reservas e existem reservas históricas cadastradas')
# def existem_reservas_historicas(client):
#     with client.application.app_context():
#         # Exclui reservas antigas para garantir que as reservas que vamos criar são as únicas no banco
#         reservas_historicas = db.session.query(Reserva).filter_by(ativa=False).all()
#         for reserva in reservas_historicas:
#             db.session.delete(reserva)
#         db.session.commit()

#         # Cria o usuário se não existir
#         usuario = db.session.query(Usuario).filter_by(email="teste@email.com").first()
#         if not usuario:
#             usuario = Usuario(
#                 nome="João",
#                 email="teste@email.com",
#                 cpf="12345678901",
#                 professor="N",
#                 senha="senha123"
#             )
#             db.session.add(usuario)
#             db.session.commit()

#         # Cria a sala se não existir
#         sala = db.session.query(Sala).filter_by(nome="Sala 1").first()
#         if not sala:
#             sala = Sala(nome="Sala 1", capacidade=30, data_criacao=datetime.utcnow())
#             db.session.add(sala)
#             db.session.commit()

#         # Insere uma reserva histórica
#         reserva_historica = Reserva(
#             usuario_id=usuario.id,
#             sala_id=sala.id,
#             data=datetime.strptime("2025-02-14", "%Y-%m-%d"),
#             horario_inicio=time(8, 0),
#             horario_fim=time(10, 0),
#             ativa=False  # Garantindo que a reserva é histórica
#         )
#         db.session.add(reserva_historica)
#         db.session.commit()

# @when('ele envia uma requisição POST para "/api/reservas/historico"', target_fixture="enviar_requisicao_historico")
# def enviar_requisicao_historico(client):
#     # Envia uma requisição POST para o endpoint de histórico de reservas
#     return client.post("/api/reservas/historico")

# @then('o sistema lista todas as reservas históricas do usuário com o status 200 OK')
# def validar_listagem_historico_sucesso(enviar_requisicao_historico):
#     response = enviar_requisicao_historico
#     assert response.status_code == 200  # Verifica se o status da resposta é 200 OK

#     data = json.loads(response.data)
#     assert isinstance(data, list)  # Verifica se a resposta é uma lista
#     assert len(data) > 0  # Verifica se há pelo menos uma reserva histórica

# Cenário 2 - Listar Histórico de Reservas sem reservas ou com todas as reservas ativas
@given('o aluno João deseja consultar o histórico de reservas e não existem reservas históricas cadastradas ou todas as reservas estão ativas')
def nao_existem_reservas_historicas_ou_todas_ativas(client):
    with client.application.app_context():
        # Exclui todas as reservas desativadas (ativa=False) para garantir que não há reservas históricas
        reservas_historicas = db.session.query(Reserva).filter_by(ativa=False).all()
        for reserva in reservas_historicas:
            db.session.delete(reserva)
        db.session.commit()

        # Cria o usuário se não existir
        usuario = db.session.query(Usuario).filter_by(email="teste@email.com").first()
        if not usuario:
            usuario = Usuario(
                nome="João",
                email="teste@email.com",
                cpf="12345678901",
                professor="N",
                senha="senha123"
            )
            db.session.add(usuario)
            db.session.commit()

        # Cria a sala se não existir
        sala = db.session.query(Sala).filter_by(nome="Sala 1").first()
        if not sala:
            sala = Sala(nome="Sala 1", capacidade=30, data_criacao=datetime.utcnow())
            db.session.add(sala)
            db.session.commit()

        # Insere uma reserva ativa para garantir que o banco tenha apenas reservas ativas
        reserva_ativa = Reserva(
            usuario_id=usuario.id,
            sala_id=sala.id,
            data=datetime.strptime("2025-02-15", "%Y-%m-%d"),
            horario_inicio=time(10, 0),
            horario_fim=time(12, 0),
            ativa=True  # Garantindo que a reserva é ativa
        )
        db.session.add(reserva_ativa)
        db.session.commit()

@when('ele envia uma requisição POST para "/api/reservas/historico"', target_fixture="enviar_requisicao_historico")
def enviar_requisicao_historico(client):
    # Envia uma requisição POST para o endpoint de histórico de reservas
    return client.post("/api/reservas/historico")

@then('o sistema retorna uma lista vazia de reservas históricas com o status 200')
def validar_listagem_historico_vazio(enviar_requisicao_historico):
    response = enviar_requisicao_historico
    print("Resposta da API:", response.data)  # Para inspecionar o conteúdo da resposta
    assert response.status_code == 200  # Verifica o status da resposta
    data = json.loads(response.data)

    # Verifica se a resposta é um dicionário
    assert isinstance(data, dict)
    
    # Verifica se a chave 'message' existe e contém a mensagem correta
    assert "message" in data
    assert data["message"] == "Nenhuma reserva histórica encontrada."  # Verifica a mensagem
