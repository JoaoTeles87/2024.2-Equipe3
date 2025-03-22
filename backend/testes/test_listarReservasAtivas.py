import pytest
import json
from flask import Flask
from pytest_bdd import scenarios, given, when, then 
from rotas.reservas_ativas import reservas_ativas_bp  

# Carrega os cenários do arquivo .feature 
scenarios('features/listarReservasAtivas.feature')

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(reservas_ativas_bp)  
    return app.test_client()

@given('o aluno João deseja consultar as reservas ativas e existem reservas ativas cadastradas')
def existem_reservas_ativas():
    pass  # Os dados já estão simulados na rota

@when('ele envia uma requisição POST para "/api/reservas/ativas"', target_fixture="enviar_requisicao_ativas")
def enviar_requisicao_ativas(client):
    response = client.post("/api/reservas/ativas")
    return response

@then('o sistema lista todas as reservas ativas do usuário com o status 200 OK')
def validar_listagem_ativas_sucesso(enviar_requisicao_ativas):
    response = enviar_requisicao_ativas
    assert response.status_code == 200  
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0  
