Feature: Listar Histórico de Reservas

  Scenario: Listar histórico de reservas com reservas históricas
    Given o aluno João deseja consultar o histórico de reservas e existem reservas históricas cadastradas
    When ele envia uma requisição POST para "/api/reservas/historico"
    Then o sistema lista todas as reservas históricas do usuário com o status 200 OK