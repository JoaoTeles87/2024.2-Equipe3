Feature: Atualizar avaliação

  Scenario: Atualizar uma avaliação existente
    Given o professor Suruagy deseja editar uma avaliação feita anteriormente
    When ele envia uma requisição PUT "/api/reviews/1" especificando o id "1" da avaliação que deseja editar
    And modifica a nota de "4" para "5" e o comentário de "Sala boa, mas com algumas falhas." para "Modificações feitas, a sala está impecável agora!"
    Then o sistema retorna a mensagem "Avaliação atualizada com sucesso." e o status 200 OK

  Scenario: Tentar atualizar uma avaliação que não existe
    Given o professor Suruagy deseja editar uma avaliação cuja qual não está presente no sistema
    When ele envia uma requisição PUT "/api/reviews/1" especificando o id "1" da avaliação que deseja editar
    And modifica a nota de "4" para "5" e o comentário de "Sala boa, mas com algumas falhas." para "Falhas corrigidas, a sala está impecável!"
    Then o sistema retorna a mensagem "Avaliação não encontrada para o ID fornecido." e o status 404 NOT FOUND
