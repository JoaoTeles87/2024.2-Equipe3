import sys
import os
from pathlib import Path
import json
import pytest
from pytest_bdd import scenarios, given, when, then

# Adiciona o diretório raiz do projeto ao PATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importações do projeto
from modelo import create_app
from modelo.extensao import db
from modelo.reserva import Reserva
from modelo.usuario import Usuario
from modelo.sala import Sala

# Carrega os cenários do arquivo .feature
scenarios('features/deletarReserva.feature')

# Fixture para configurar a aplicação
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

# Fixture para criar um cliente de teste
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture para simular uma reserva existente (dados estáticos)
@pytest.fixture
def dados_reserva():
    # Simula a existência de uma reserva
    reserva = {"id": 1, "usuario_id": 1, "detalhes": "Reserva de teste 1"}
    return reserva

# Fixture para enviar a requisição DELETE
@pytest.fixture
def enviar_requisicao_delete_reserva(client, dados_reserva):
    # Realiza a requisição DELETE
    return client.delete(f"/api/reservas/{dados_reserva['id']}")

# Cenário: Deletar reserva existente
@given('o aluno João deseja deletar uma reserva feita anteriormente')
def aluno_joao(client, dados_reserva):
    pass  # Não precisa de configuração adicional

@when('ele envia uma requisição DELETE para "/api/reservas/1" especificando o id "1" da reserva que deseja deletar')
def step_enviar_requisicao_delete_reserva(enviar_requisicao_delete_reserva):
    pass  # A fixture já faz o trabalho necessário

@then('o sistema retorna a mensagem "Reserva excluída com sucesso!" e o status 200 OK')
def validar_exclusao_sucesso(enviar_requisicao_delete_reserva):
    response = enviar_requisicao_delete_reserva
    print(response.data)  
    assert response.status_code == 200 
    data = json.loads(response.data)
    assert "Reserva excluída com sucesso!" in data["message"]