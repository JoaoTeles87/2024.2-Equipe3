Feature: Listar Reservas Ativas

  Scenario: Listar reservas ativas quando o usuário tem reservas ativas
    Given o aluno João deseja consultar as reservas ativas e existem reservas ativas cadastradas
    When ele envia uma requisição POST para "/api/reservas/ativas"
    Then o sistema lista todas as reservas ativas do usuário com o status 200 OK
  
