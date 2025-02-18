Feature: Consultar Avaliação

  Scenario: Consulta de avaliação existente
    Given o professor Suruagy deseja consultar uma avaliação presente no sistema
    When ele envia uma requisição GET para "/api/reviews/1"
    Then o sistema retorna a avaliação com comentário "Sala excelente, as mudanças foram feitas e ficou ótima.", data_avaliacao "Sat, 15 Feb 2025 16:31:37 GMT", id "1", nota "5", reserva_id "1", sala_id "2", usuario_id "3" com o status 200 OK

  Scenario: Consulta de avaliação inexistente
    Given o professor Suruagy deseja consultar uma avaliação presente no sistema
    When ele envia uma requisição GET para "/api/reviews/1"
    Then o sistema não encontra avaliação presente com o ID especificado
    And retorna a mensagem de erro "Avaliação não encontrada para o ID fornecido." com o status 404 NOT FOUND
