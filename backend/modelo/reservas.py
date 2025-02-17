# TODO: ver quais dados ainda precisa colocar aqui
import copy

mock_reservas = [
    {
        "id": 1,
        "professor_id": 3,
        "sala_id": 5,
        "data": "2025-02-20",
        "start_time": "14:00",
        "end_time": "15:00",
        "status": "ativa"
    },

    {
        "id": 2,
        "professor_id": 3,
        "sala_id": 3,
        "data": "2025-02-21",
        "start_time": "09:00",
        "end_time": "11:00",
        "status": "ativa"
    },

    {
        "id": 3,
        "professor_id": 3,
        "sala_id": 1,
        "data": "2025-02-22",
        "start_time": "08:00",
        "end_time": "10:00",
        "status": "ativa"
    },

    {
        "id": 4,
        "professor_id": 3,
        "sala_id": 2,
        "data": "2025-02-20",
        "start_time": "16:00",
        "end_time": "18:00",
        "status": "ativa"
    }
]

MOCK_RESERVAS_COPY = copy.copy(mock_reservas)

def reservas_reset():
    mock_reservas.clear()
    mock_reservas.extend(copy.copy(MOCK_RESERVAS_COPY))