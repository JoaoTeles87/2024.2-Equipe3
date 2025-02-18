import copy

EQUIPAMENTOS = [
    "Ar-condicionado", "Cabo P2", "Cabo HDMI", "Cabo VGA", "Microfone",
    "Extensão", "Mesa de som", "Passador", "Televisor", "Projetor",
    "Carregador", "Pen Drive", "Mouse", "Teclado", "Monitor", "USB-C",
    "Cafeteira", "Gelágua"
]

mock_salas = [
    {
        "id": 1,
        "nome": "E001",
        "tipo": "Reunião",
        "lugares": 14,
        "andar": 15,
        "equipamentos": ["Ar-condicionado", "Televisor"],
        "average_rating": 4.0,
        "review_count": 2
    },
    {
        "id": 2,
        "nome": "E002",
        "tipo": "Auditório",
        "lugares": 50,
        "andar": 10,
        "equipamentos": ["Projetor", "Microfone", "Mesa de som"],
        "average_rating": 5.0,
        "review_count": 5
    },
    {
        "id": 3,
        "nome": "E003",
        "tipo": "Reunião",
        "lugares": 8,
        "andar": 7,
        "equipamentos": ["Cabo HDMI", "Cabo VGA", "Extensão"],
        "average_rating": 3.5,
        "review_count": 3
    },
    {
        "id": 4,
        "nome": "E004",
        "tipo": "Auditório",
        "lugares": 80,
        "andar": 5,
        "equipamentos": ["Projetor", "Mesa de som", "Passador", "Teclado", "Mouse"],
        "average_rating": 4.8,
        "review_count": 10
    },
    {
        "id": 5,
        "nome": "E005",
        "tipo": "Reunião",
        "lugares": 12,
        "andar": 9,
        "equipamentos": ["Monitor", "USB-C", "Cabo P2"],
        "average_rating": 4.2,
        "review_count": 6
    },
    {
        "id": 6,
        "nome": "E006",
        "tipo": "Reunião",
        "lugares": 6,
        "andar": 3,
        "equipamentos": ["Ar-condicionado", "Gelágua", "Cafeteira"],
        "average_rating": 3.9,
        "review_count": 4
    },
    {
        "id": 7,
        "nome": "E007",
        "tipo": "Auditório",
        "lugares": 100,
        "andar": 2,
        "equipamentos": ["Projetor", "Microfone", "Mesa de som", "Extensão"],
        "average_rating": 4.7,
        "review_count": 8
    },
    {
        "id": 8,
        "nome": "E008",
        "tipo": "Reunião",
        "lugares": 10,
        "andar": 4,
        "equipamentos": ["Carregador", "Pen Drive", "USB-C"],
        "average_rating": 4.5,
        "review_count": 7
    }
]

MOCK_SALAS_COPY = copy.copy(mock_salas)

def salas_reset():
    mock_salas.clear()
    mock_salas.extend(copy.copy(MOCK_SALAS_COPY))
