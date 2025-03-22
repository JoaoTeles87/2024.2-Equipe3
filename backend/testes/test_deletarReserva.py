import sys
import json
import pytest
from flask import Flask
from pytest_bdd import scenarios, given, when, then

# Adiciona os cenários do arquivo .feature
scenarios('features/deletarReserva.feature')

# Importação da rota correta para deletar reserva
from rotas.exclusao_reserva import exclusao_reserva_bp  
from modelo.extensao import db  # Certifique-se de importar o db correto

# Fixture para configurar a aplicação de teste
@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória para os testes

    # Inicializa o db com a app
    db.init_app(app)

    # Registra o blueprint após a inicialização do db
    app.register_blueprint(exclusao_reserva_bp)

    # Criar as tabelas no banco de dados dentro do contexto da app
    with app.app_context():
        db.create_all()

    return app

# Fixture para criar um cliente de teste
@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

# Fixture para simular uma reserva existente (dados estáticos)
@pytest.fixture(scope="function")
def dados_reserva():
    return {"id": 1, "usuario_id": 1, "detalhes": "Reserva de teste 1"}

# Fixture para enviar a requisição DELETE
@pytest.fixture(scope="function")
def enviar_requisicao_delete_reserva(client, dados_reserva):
    response = client.delete(f"/api/reservas/{dados_reserva['id']}")
    return response

# Cenário: Deletar reserva existente
@given('o aluno João deseja deletar uma reserva feita anteriormente')
def aluno_joao():
    pass  # Os dados já estão simulados na rota

@when('ele envia uma requisição DELETE para "/api/reservas/1" especificando o id "1" da reserva que deseja deletar')
def step_enviar_requisicao_delete_reserva(enviar_requisicao_delete_reserva):
    pass  # A fixture já faz o trabalho necessário

@then('o sistema retorna a mensagem "Reserva excluída com sucesso!" e o status 200 OK')
def validar_exclusao_sucesso(enviar_requisicao_delete_reserva):
    response = enviar_requisicao_delete_reserva
    assert response.status_code == 200  

    data = json.loads(response.data)
    assert "Reserva excluída com sucesso!" in data["message"]

    # Verifique se a reserva foi realmente deletada
    from modelo import Reserva  # Certifique-se de importar a classe Reserva
    with app.app_context():  # Garante que a sessão do db esteja dentro do contexto da app
        reserva_deletada = db.session.query(Reserva).get(1)
        assert reserva_deletada is None  # Verifica se a reserva foi excluída
