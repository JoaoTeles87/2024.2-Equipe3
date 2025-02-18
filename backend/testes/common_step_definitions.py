import json
import requests
from pytest_bdd import when, then, given, parsers


BASE_URL = 'http://127.0.0.1:5000'

@when(parsers.parse('uma requisição "{metodo}" for enviada para "{url}" com o corpo: "{body}"'))
def mandar_requisicao(metodo, url, body):
    url = f'{BASE_URL}/{url}'

    metodo = metodo.upper()
    request_method = {
        "POST": requests.post,
        "GET": requests.get,
        "DELETE": requests.delete,
        "PUT": requests.put
    }.get(metodo)

    assert request_method is not None, f"Método HTTP inválido: {metodo}"

    json_body = json.loads(body) if metodo in ["POST", "PUT"] else None

    response = request_method(url, json=json_body)

    mandar_requisicao.response = response


@then(parsers.parse('o status da resposta deve ser "{status}"'))
def checar_status(status):
    assert mandar_requisicao.response.status_code == int(status), f'mensagem: "{mandar_requisicao.response.text}"'

@then(parsers.parse('o JSON da resposta deve conter "{atributo}": "{string}"'))
def checar_mensagem(atributo, string):
    response_json = mandar_requisicao.response.json()

    assert response_json.get(atributo) == string, (
        f"Erro: Esperado '{atributo}': '{string}', obtido '{response_json.get(atributo)}'"
    )


@given(parsers.parse('a sala de id "{sala_id:d}" está disponível no dia "{data}" das "{start_time}" às "{end_time}"'))
def sala_disponivel(sala_id, data, start_time, end_time):
    url = f'{BASE_URL}/api/salas?data={data}&start_time={start_time}&end_time={end_time}'
    response = requests.get(url)

    assert response.status_code == 200, f"Erro ao buscar salas disponíveis: {response.text}"

    sala_encontrada = any(sala['id'] == sala_id for sala in response.json())

    assert sala_encontrada, (f'Sala {sala_id} não está disponível no horário solicitado ({data} das {start_time} '
                             f'às {end_time})')


@given(parsers.parse('a sala de id "{sala_id:d}" não está disponível no dia "{data}" das "{start_time}" às "{end_time}"'))
def sala_nao_disponivel(sala_id, data, start_time, end_time):
    url = f'{BASE_URL}/api/salas?data={data}&start_time={start_time}&end_time={end_time}'
    response = requests.get(url)

    assert response.status_code == 200, f"Erro ao buscar salas disponíveis: {response.text}"

    sala_encontrada = any(sala['id'] == sala_id for sala in response.json())

    assert not sala_encontrada, (f'Sala {sala_id} está disponível no horário solicitado ({data} das {start_time} '
                             f'às {end_time})')