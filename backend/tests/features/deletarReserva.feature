Feature: Deletar Reserva

  Scenario: Deletar reserva existente
    Given o aluno João deseja deletar uma reserva feita anteriormente
    When ele envia uma requisição DELETE para "/api/reservas/1" especificando o id "1" da reserva que deseja deletar
    Then o sistema retorna a mensagem "Reserva excluída com sucesso!" e o status 200 OK

  Scenario: Deletar reserva que não existe
    Given o aluno João deseja deletar uma reserva que não existe
    When ele envia uma requisição DELETE para "/api/reservas/1" especificando o id "1" da reserva que deseja deletar
    Then o sistema retorna a mensagem "Reserva não encontrada para o ID fornecido." e o status 404 NOT FOUND
