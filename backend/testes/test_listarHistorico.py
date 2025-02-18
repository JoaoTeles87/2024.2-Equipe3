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
    print(f"Reservas restantes após limpeza: {len(reservas_restantes)}") 

# Função para gerar dados únicos para cada execução de teste
def gerar_cpf_unico():
    return str(random.randint(10000000000, 99999999999))

def gerar_email_unico():
    return f"joao{random.randint(1000, 9999)}@email.com"


# Fixture para criar um cliente de teste
@pytest.fixture
def client(app):
    # Limpa o banco de dados antes de cada teste
    with app.app_context():
        setup_teardown() 
    return app.test_client()

# Cenário 1 - Listar Histórico de Reservas com reservas
@given('o aluno João deseja consultar o histórico de reservas e existem reservas históricas cadastradas')
def existem_reservas_historicas(client):
    with client.application.app_context():  # Certifique-se de que o contexto da aplicação está ativo
        # Não é necessário criar reservas aqui, pois já estão no banco de dados
        pass

@when('ele envia uma requisição POST para "/api/reservas/historico"', target_fixture="enviar_requisicao_historico")
def enviar_requisicao_historico(client):
    # Envia uma requisição POST para o endpoint de histórico de reservas
    return client.post("/api/reservas/historico")

@then('o sistema lista todas as reservas históricas do usuário com o status 200 OK')
def validar_listagem_historico_sucesso(enviar_requisicao_historico):
    response = enviar_requisicao_historico
    assert response.status_code == 200  # Verifica se o status da resposta é 200 OK

    data = json.loads(response.data)
    assert isinstance(data, list)  # Verifica se a resposta é uma lista
    assert len(data) > 0  # Verifica se há pelo menos uma reserva histórica
