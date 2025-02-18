import json
import requests
from pytest_bdd import scenario, when, then, given, parsers

from backend.testes.common_step_definitions import *


BASE_URL = 'http://127.0.0.1:5000'

@scenario('../features/salas.feature', 'Criar sala com sucesso')
def test_criar_sala_com_sucesso():
    pass

@scenario('../features/salas.feature', 'Buscar todas as salas disponíveis')
def test_buscar_salas():
    pass

@scenario('../features/salas.feature', 'Erro ao buscar salas sem data preenchida')
def test_erro_ao_buscar_salas_data():
    pass

@scenario('../features/salas.feature', 'Erro ao buscar salas com tempo não informado')
def test_erro_ao_buscar_salas_tempo():
    pass

@scenario('../features/salas.feature', 'Erro ao tentar deletar sala com reserva ativa')
def test_erro_ao_tentar_deletar_sala_com_reserva():
    pass

@given(parsers.parse('a sala de id "{sala_id}" tem uma reserva ativa'))
def sala_tem_reserva_ativa(sala_id):
    sala_id = int(sala_id)

    response = requests.get(f"{BASE_URL}/api/reservas")
    assert response.status_code == 200, f"Erro ao buscar reservas: {response.text}"

    reservas = response.json()

    reserva_existente = any(
        reserva for reserva in reservas if reserva["sala_id"] == sala_id and reserva["status"] == "ativa"
    )

    if not reserva_existente:
        reserva_body = {
            "sala_id": sala_id,
            "data": "2025-02-25",
            "start_time": "14:00",
            "end_time": "15:00"
        }

        reserva_response = requests.post(f"{BASE_URL}/api/reservas/3", json=reserva_body)  # Aqui eu crio só para o professor de id 3
        assert reserva_response.status_code == 201, f"Erro ao criar reserva ativa: {reserva_response.text}"


@given(parsers.parse('existe uma sala com nome "{nome}"'))
def existe_uma_sala_com_nome(nome):
    response = requests.get(f"{BASE_URL}/api/salas")

    salas = response.json()


    sala_existente = next((sala for sala in salas if sala["nome"] == nome), None)

    if not sala_existente:
        sala_body = {
            "nome": nome,
            "tipo": "Reunião",
            "lugares": 10,
            "andar": 0,
            "equipamentos": ["Projetor"]
        }

        sala_response = requests.post(f"{BASE_URL}/api/salas", json=sala_body)
        assert sala_response.status_code == 201, f"Erro ao criar sala: {response.text}"

@given(parsers.parse('não existe uma sala com nome "{nome}"'))
def sala_nao_existe(nome):

    response = requests.get(f"{BASE_URL}/api/salas")
    assert response.status_code == 200, "Erro ao buscar salas: " + response.text

    salas = response.json()

    for sala in salas:
        if sala["nome"] == nome:
            sala_id = sala["id"]

            # Deleta se necessário
            delete_response = requests.delete(f"{BASE_URL}/api/salas/{sala_id}")
            assert delete_response.status_code in [200, 204], "Erro ao deletar sala: " + delete_response.text


@then(parsers.parse('o JSON da sala deve conter "{atributo}": "{valor}"'))
def checar_atributo(atributo, valor):
    response_json = mandar_requisicao.response.json()

    assert "sala" in response_json, f"Erro; 'sala' não encontrado na resposta: \n{response_json}"

    assert atributo in response_json["sala"], \
        f"Erro: Atributo '{atributo}' não encontrado dentro de 'sala': \n{response_json}"

    if valor.isdigit():
        valor = int(valor)

    valor_real = response_json["sala"][atributo]

    assert valor_real == valor, (
        f"Erro: Para '{atributo}', esperado '{valor}' ({type(valor).__name__}), "
        f"obtido '{valor_real}' ({type(valor_real).__name__})"
    )


@then('o JSON da resposta deve conter uma lista de salas com todos os dados')
def checar_lista_de_salas():
    response_json = mandar_requisicao.response.json()

    assert isinstance(response_json, list), f'Uma lista de salas não for retornada'
    assert len(response_json) > 0, f'A lista de salas retornada está vazia'

    for sala in response_json:
        assert "id" in sala, f"'id' faltando: {sala}"
        assert "tipo" in sala, f"'tipo' faltando: {sala}"
        assert "lugares" in sala, f"'lugares' faltando: {sala}"
        assert 'andar' in sala, f"'andar' faltando: {sala}"
        assert 'equipamentos' in sala, f"'equipamentos' faltando: {sala}"
        assert 'nome' in sala, f"'nome' faltando: {sala}"
