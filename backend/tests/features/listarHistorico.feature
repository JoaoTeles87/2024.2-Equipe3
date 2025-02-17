Feature: Listar Histórico de Reservas

  # Scenario: Listar histórico de reservas com reservas históricas
  #   Given o aluno João deseja consultar o histórico de reservas e existem reservas históricas cadastradas
  #   When ele envia uma requisição POST para "/api/reservas/historico"
  #   Then o sistema lista todas as reservas históricas do usuário com o status 200 OK


Scenario: Listar Histórico de Reservas sem reservas ou com todas as reservas ativas
    Given o aluno João deseja consultar o histórico de reservas e não existem reservas históricas cadastradas ou todas as reservas estão ativas
    When ele envia uma requisição POST para "/api/reservas/historico"
    Then o sistema retorna uma lista vazia de reservas históricas com o status 200