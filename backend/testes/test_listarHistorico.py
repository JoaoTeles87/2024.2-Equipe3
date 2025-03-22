import pytest
import json
from flask import Flask
from pytest_bdd import scenarios, given, when, then 
from rotas.historico_reserva import historico_reservas_bp  

# Carrega os cenários do arquivo .feature 
scenarios('features/listarHistorico.feature')

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historico_reservas_bp)  
    return app.test_client()

@given('o aluno João deseja consultar o histórico de reservas e existem reservas históricas cadastradas')
def existem_reservas_historicas():
    pass  # Os dados já estão simulados na rota

@when('ele envia uma requisição POST para "/api/reservas/historico"', target_fixture="enviar_requisicao_historico")
def enviar_requisicao_historico(client):
    response = client.post("/api/reservas/historico", json={"email": "joao@email.com"})

    return response

@then('o sistema lista todas as reservas históricas do usuário com o status 200 OK')
def validar_listagem_historico_sucesso(enviar_requisicao_historico):
    response = enviar_requisicao_historico
    assert response.status_code == 200  
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
