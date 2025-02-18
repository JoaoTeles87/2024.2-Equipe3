import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import json
import pytest
from datetime import datetime
from pytest_bdd import scenarios, given, when, then

scenarios('features/listarReview.feature')

from backend.modelo.__init__ import create_app
from backend.modelo.extensao import db
from backend.modelo.reviewSala import ReviewSala

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def criar_avaliacao(app):
    with app.app_context():
        data_avaliacao = datetime.strptime("Sat, 15 Feb 2025 16:31:37 GMT", "%a, %d %b %Y %H:%M:%S GMT")
        review = ReviewSala(
            reserva_id=1,
            sala_id=2,
            usuario_id=3,
            nota=5,
            comentario="Sala excelente, as mudanças foram feitas e ficou ótima.",
            data_avaliacao=data_avaliacao
        )
        db.session.add(review)
        db.session.commit()
        db.session.refresh(review)
        return review

@given('o professor Suruagy deseja consultar as avaliações presentes no sistema e existem avaliações cadastradas')
def existem_avaliacoes(criar_avaliacao):
    pass

@given('o professor Suruagy deseja consultar as avaliações presentes no sistema e não existem avaliações cadastradas')
def nao_existem_avaliacoes(app):
    with app.app_context():
        db.session.query(ReviewSala).delete()
        db.session.commit()

@when('ele envia uma requisição GET para "/api/reviews"', target_fixture="enviar_requisicao_listar")
def enviar_requisicao_listar(client):
    return client.get("/api/reviews")

@then('o sistema lista todas as avaliações que foram postadas anteriormente para todas as salas com o status 200 OK')
def validar_listagem_sucesso(enviar_requisicao_listar):
    response = enviar_requisicao_listar
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

@then('o sistema não encontra nenhuma avaliação no sistema')
def validar_listagem_vazia(enviar_requisicao_listar):
    response = enviar_requisicao_listar
    assert response.status_code == 404

@then('exibe a mensagem de erro "Nenhuma avaliação encontrada." com o status 404 NOT FOUND')
def validar_mensagem_erro(enviar_requisicao_listar):
    response = enviar_requisicao_listar
    data = json.loads(response.data)
    assert data['error'] == "Nenhuma avaliação encontrada."
