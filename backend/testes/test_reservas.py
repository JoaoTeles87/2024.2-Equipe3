import requests
from pytest_bdd import scenario, when, then, given, parsers
from backend.testes.common_step_definitions import *

BASE_URL = 'http://127.0.0.1:5000'


@scenario('../features/reservas.feature', 'Criar uma reserva com sucesso')
def test_criar_uma_reserva_com_sucesso():
    pass

@scenario('../features/reservas.feature', 'Erro ao tentar reservar uma sala já ocupada')
def test_erro_ao_tentar_reservar_sala_ocupada():
    pass

@scenario('../features/reservas.feature', 'Erro ao tentar reservar com campos ausentes')
def test_erro_ao_tentar_reservar_campos_ausentes():
    pass

@scenario('../features/reservas.feature', 'Cancelar uma reserva com sucesso')
def test_cancelar_uma_reserva_com_sucesso():
    pass

@scenario('../features/reservas.feature', 'Erro ao tentar cancelar uma reserva inexistente')
def test_cancelar_uma_reserva_inexistente():
    pass


@given(parsers.parse('o professor de id "{professor_id:d}" não tem uma reserva no dia "{data}" '
                     'das "{start_time}" às "{end_time}"'))
def professor_disponivel(professor_id, data, start_time, end_time):
    url = f'{BASE_URL}/api/reservas/{professor_id}'
    response = requests.get(url)
    reservas = response.json()

    for reserva in reservas:
        if reserva['data'] == data and reserva['status'] == ['ativa']:
            assert (start_time >= reserva['end_time'] or end_time <= reserva['start_time']), \
                f'Professor {professor_id} já tem uma reserva nesse horário'


@given(parsers.parse('o professor de id "{professor_id:d}" tem uma reserva ativa de id "{reserva_id}"'))
def professor_disponivel(professor_id, reserva_id):
    url = f'{BASE_URL}/api/reservas/{professor_id}'
    response = requests.get(url)

    assert response.status_code == 200, f'Erro ao buscar reservas do professor {professor_id}'

    reservas = response.json()

    reserva_encontrada = any(
        reserva['id'] == int(reserva_id) and reserva["status"] for reserva in reservas
    )

    assert reserva_encontrada, f"O professor {professor_id} não tem uma reserva ativa de id {reserva_id}"


@then(parsers.parse('o JSON da reserva deve conter "{atributo}": "{valor}"'))
def checar_atributo(atributo, valor):
    response_json = mandar_requisicao.response.json()

    assert "reservation" in response_json, (
        f"Erro: 'reservation' não encontrado na resposta:\n{response_json}"
    )

    assert atributo in response_json["reservation"], (
        f"Erro: Atributo '{atributo}' não encontrado dentro de 'reservation':\n{response_json}"
    )

    if valor.isdigit():
        valor = int(valor)

    valor_real = response_json["reservation"][atributo]

    assert valor_real == valor, (
        f"Erro: Para '{atributo}', esperado '{valor}' ({type(valor).__name__}), "
        f"obtido '{valor_real}' ({type(valor_real).__name__})"
    )