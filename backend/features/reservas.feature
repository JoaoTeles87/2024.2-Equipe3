Feature: API de Reservas

    Scenario: Criar uma reserva com sucesso
        Given a sala "E001" está disponível no dia "2025-02-25" das "14:00" às "15:00"
        When uma requisição POST for enviada para "/api/reservas" com o corpo:
            """
            {
                "sala_id": 1,
                "professor_id": 3,
                "data": "2025-02-25",
                "start_time": "14:00",
                "end_time": "15:00"
            }
            """
        Then o status da resposta deve ser "201"
        And o JSON da resposta deve conter "message": "Reserva criada com sucesso"
        And o JSON da resposta deve conter "sala_id": 1
        And o JSON da resposta deve conter "professor_id": 3