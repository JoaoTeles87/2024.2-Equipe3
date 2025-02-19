Feature: Listar Avaliações

  Scenario: Listar avaliações quando há avaliações no sistema
    Given o professor Suruagy deseja consultar as avaliações presentes no sistema e existem avaliações cadastradas
    When ele envia uma requisição GET para "/api/reviews"
    Then o sistema lista todas as avaliações que foram postadas anteriormente para todas as salas com o status 200 OK

  Scenario: Listar avaliações quando não há nenhuma avaliação
    Given o professor Suruagy deseja consultar as avaliações presentes no sistema e não existem avaliações cadastradas
    When ele envia uma requisição GET para "/api/reviews"
    Then o sistema não encontra nenhuma avaliação no sistema
    And exibe a mensagem de erro "Nenhuma avaliação encontrada." com o status 404 NOT FOUND
