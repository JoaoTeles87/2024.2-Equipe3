import pytest
import requests
from pytest_bdd import scenarios, given, when, then

scenarios('features/criarReview.feature')

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def context():
    return {}

@given('que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id "1" para a sala_id "2"')
@given('que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id ""')
@given('que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id "1" para a sala_id ""')
def preparar_contexto(context):
    context['url'] = f"{BASE_URL}/api/reviews"

@when(
    'ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "2", usuario_id "3", nota "4" e comentário "Sala boa, mas com algumas falhas."'
)
def enviar_review_valida(context):
    payload = {
        "reserva_id": 1,
        "sala_id": 2,
        "usuario_id": 3,
        "nota": 4,
        "comentario": "Sala boa, mas com algumas falhas."
    }
    context['response'] = requests.post(context['url'], json=payload)


@when(
    'ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "2", usuario_id "3", nota "" e comentário "Sala boa, mas sem computador!"'
)
def enviar_review_sem_nota(context):
    payload = {
        "reserva_id": 1,
        "sala_id": 2,
        "usuario_id": 3,
        "nota": None,
        "comentario": "Sala boa, mas sem computador!"
    }
    context['response'] = requests.post(context['url'], json=payload)


@when(
    'ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "", usuario_id "3", nota "4" e comentário "Sala boa, mas sem computador!"'
)
def enviar_review_sem_sala_id(context):
    payload = {
        "reserva_id": 1,
        "sala_id": None,
        "usuario_id": 3,
        "nota": 4,
        "comentario": "Sala boa, mas sem computador!"
    }
    context['response'] = requests.post(context['url'], json=payload)


@when(
    'ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "2", usuario_id "", nota "4" e comentário "Sala boa, mas sem computador!"'
)
def enviar_review_sem_usuario_id(context):
    payload = {
        "reserva_id": 1,
        "sala_id": 2,
        "usuario_id": None,
        "nota": 4,
        "comentario": "Sala boa, mas sem computador!"
    }
    context['response'] = requests.post(context['url'], json=payload)


@when(
    'ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "", sala_id "2", usuario_id "3", nota "4" e comentário "Sala boa, mas sem computador!"'
)
def enviar_review_sem_reserva_id(context):
    payload = {
        "reserva_id": None,
        "sala_id": 2,
        "usuario_id": 3,
        "nota": 4,
        "comentario": "Sala boa, mas sem computador!"
    }
    context['response'] = requests.post(context['url'], json=payload)


@then('o sistema retorna "Avaliação criada com sucesso!" com o status 201')
def validar_resposta_sucesso(context):
    assert context['response'].status_code == 201
    assert context['response'].json()["mensagem"] == "Avaliação criada com sucesso!"


@then('o sistema retorna "A nota é obrigatória para avaliar a sala." com o status 400')
def validar_resposta_sem_nota(context):
    assert context['response'].status_code == 400
    assert context['response'].json()["error"] == "A nota é obrigatória para avaliar a sala."


@then('o sistema retorna "O ID da Sala é obrigatório para avaliar a sala." com o status 400')
def validar_resposta_sem_sala_id(context):
    assert context['response'].status_code == 400
    assert context['response'].json()["error"] == "O ID da Sala é obrigatório para avaliar a sala."


@then('o sistema retorna "O ID do Usuário é obrigatório para avaliar a sala." com o status 400')
def validar_resposta_sem_usuario_id(context):
    assert context['response'].status_code == 400
    assert context['response'].json()["error"] == "O ID do Usuário é obrigatório para avaliar a sala."


@then('o sistema retorna "O ID da Reserva é obrigatório para avaliar a sala." com o status 400')
def validar_resposta_sem_reserva_id(context):
    assert context['response'].status_code == 400
    assert context['response'].json()["error"] == "O ID da Reserva é obrigatório para avaliar a sala."