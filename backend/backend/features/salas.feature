Feature: API de Salas

    Scenario: Criar sala com sucesso
      Given não existe uma sala com nome "E901"
      When uma requisição "POST" for enviada para "/api/salas" com o corpo: "{"nome": "E901", "tipo": "Reunião", "lugares": 20, "andar": 3, "equipamentos": ["Projetor", "Ar-condicionado"]}"
      Then o status da resposta deve ser "201"
      And o JSON da resposta deve conter "mensagem": "Sala criada com sucesso!"
      And o JSON da sala deve conter "andar": "3"
      And o JSON da sala deve conter "nome": "E901"
      And o JSON da sala deve conter "tipo": "Reunião"
      And o JSON da sala deve conter "lugares": "20"


    Scenario: Erro ao tentar criar sala com nome existente
      Given existe uma sala com nome "E001"
      When uma requisição "POST" for enviada para "/api/salas" com o corpo: "{"nome": "E001", "tipo": "Reunião", "lugares": 20, "andar": 3, "equipamentos": ["Projetor", "Ar-condicionado"]}"
      Then o status da resposta deve ser "409"
      And o JSON da resposta deve conter "erro": "Já existe uma sala com esse nome"


    Scenario: Buscar todas as salas disponíveis
        When uma requisição "GET" for enviada para "/api/salas" com o corpo: """"
        Then o status da resposta deve ser "200"
        And o JSON da resposta deve conter uma lista de salas com todos os dados


    Scenario: Erro ao buscar salas com tempo não informado
      When uma requisição "GET" for enviada para "/api/salas?data=2025-02-25&start_time=14:00" com o corpo: """"
      Then o status da resposta deve ser "400"
      And o JSON da resposta deve conter "erro": "tempo não informado"


    Scenario: Erro ao buscar salas sem data preenchida
      When uma requisição "GET" for enviada para "/api/salas?start_time=14:00&end_time=15:00" com o corpo: """"
      Then o status da resposta deve ser "400"
      And o JSON da resposta deve conter "erro": "data não informada"


    Scenario: Erro ao tentar deletar sala com reserva ativa
      Given a sala de id "1" tem uma reserva ativa
      When uma requisição "DELETE" for enviada para "/api/salas/1" com o corpo: """"
      Then o status da resposta deve ser "409"
      And o JSON da resposta deve conter "erro": "Sala possui reservas ativas e não pode ser deletada"