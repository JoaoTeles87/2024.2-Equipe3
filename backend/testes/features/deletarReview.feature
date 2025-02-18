Feature: Deletar Avaliação

  Scenario: Deletar avaliação existente
    Given o professor Suruagy deseja deletar uma avaliação feita anteriormente
    When ele envia uma requisição DELETE para "/api/reviews/1" especificando o id "1" da avaliação que deseja deletar
    Then o sistema retorna a mensagem "Avaliação deletada com sucesso!" e o status 200 OK

  Scenario: Deletar avaliação que não existe
    Given o professor Suruagy deseja deletar uma avaliação que não existe
    When ele envia uma requisição DELETE para "/api/reviews/1" especificando o id "1" da avaliação que deseja deletar
    Then o sistema retorna a mensagem "Avaliação não encontrada para o ID fornecido." e o status 404 NOT FOUND
