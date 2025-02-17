Feature: API de Reservas

    Scenario: Criar uma reserva com sucesso
        Given a sala de id "5" está disponível no dia "2025-03-03" das "14:00" às "15:00"
        And o professor de id "3" não tem uma reserva no dia "2025-03-03" das "14:00" às "15:00"
        When uma requisição "POST" for enviada para "/api/reservas/3" com o corpo: "{"sala_id": 5,"data": "2025-03-03","start_time": "14:00","end_time": "15:00"}"
        Then o status da resposta deve ser "201"
        And o JSON da resposta deve conter "mensagem": "Reserva criada com sucesso!"
        And o JSON da reserva deve conter "sala_id": "5"
        And o JSON da reserva deve conter "professor_id": "3"


    Scenario: Erro ao tentar reservar uma sala já ocupada
        Given a sala de id "5" não está disponível no dia "2025-02-20" das "14:30" às "16:00"
        When uma requisição "POST" for enviada para "/api/reservas/3" com o corpo: "{"sala_id": 5,"data": "2025-02-20","start_time": "14:30","end_time": "16:00"}"
        Then o status da resposta deve ser "409"
        And o JSON da resposta deve conter "erro": "Sala já reservada para esse horário"


    Scenario: Erro ao tentar reservar com campos ausentes
        Given a sala de id "5" está disponível no dia "2025-01-21" das "14:00" às "15:00"
        And o professor de id "3" não tem uma reserva no dia "2025-01-21" das "14:00" às "15:00"
        When uma requisição "POST" for enviada para "/api/reservas/3" com o corpo: "{"data": "2025-01-21","start_time": "14:00","end_time": "15:00"}"
        Then o status da resposta deve ser "400"
        And o JSON da resposta deve conter "erro": "Campos obrigatórios ausentes"


    Scenario: Cancelar uma reserva com sucesso
        Given o professor de id "3" tem uma reserva ativa de id "2"
        When uma requisição "DELETE" for enviada para "/api/reservas/2" com o corpo: """"
        Then o status da resposta deve ser "200"
        And o JSON da resposta deve conter "mensagem": "Reserva cancelada!"
        And o JSON da reserva deve conter "id": "2"


    Scenario: Erro ao tentar cancelar uma reserva inexistente
        When uma requisição "DELETE" for enviada para "/api/reservas/99" com o corpo: """"
        Then o status da resposta deve ser "404"
        And o JSON da resposta deve conter "erro": "Reserva não encontrada."


