Feature: Criação de Review

  Scenario: Criação bem-sucedida de review
    Given que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id "1" para a sala_id "2"
    When ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "2", usuario_id "3", nota "4" e comentário "Sala boa, mas com algumas falhas."
    Then o sistema retorna "Avaliação criada com sucesso!" com o status 201

  Scenario: Falha ao criar review sem nota
    Given que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id "1" para a sala_id "2"
    When ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "2", usuario_id "3", nota "" e comentário "Sala boa, mas sem computador!"
    Then o sistema retorna "A nota é obrigatória para avaliar a sala." com o status 400

  Scenario: Falha ao criar review sem sala_id
    Given que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id "1" para a sala_id ""
    When ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "", usuario_id "3", nota "4" e comentário "Sala boa, mas sem computador!"
    Then o sistema retorna "O ID da Sala é obrigatório para avaliar a sala." com o status 400

  Scenario: Falha ao criar review sem usuario_id
    Given que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id "1" para a sala_id "2"
    When ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "1", sala_id "2", usuario_id "", nota "4" e comentário "Sala boa, mas sem computador!"
    Then o sistema retorna "O ID do Usuário é obrigatório para avaliar a sala." com o status 400

  Scenario: Falha ao criar review sem reserva_id
    Given que o professor Suruagy deseja fazer uma avaliação pós reserva com reserva_id ""
    When ele envia uma requisição POST para "/api/reviews" com os dados reserva_id "", sala_id "2", usuario_id "3", nota "4" e comentário "Sala boa, mas sem computador!"
    Then o sistema retorna "O ID da Reserva é obrigatório para avaliar a sala." com o status 400
