Feature: Listar Reservas Ativas

  Scenario: Listar reservas ativas quando o usuário tem reservas ativas
    Given o aluno João deseja consultar as reservas ativas e existem reservas ativas cadastradas
    When ele envia uma requisição POST para "/api/reservas/ativas"
    Then o sistema lista todas as reservas ativas do usuário com o status 200 OK

  Scenario: Listar reservas ativas quando o usuário não tem reservas ativas
    Given o aluno João deseja consultar as reservas ativas e não existem reservas ativas cadastradas
    When ele envia uma requisição POST para "/api/reservas/ativas"
    Then o sistema não encontra nenhuma reserva ativa para o usuário
    And exibe a mensagem de erro "Nenhuma reserva ativa encontrada." com o status 404 NOT FOUND

  Scenario: Consultar reservas ativas quando o usuário não tem reservas ativas
    Given o professor Suruagy não tem reservas ativas no sistema
    When ele envia uma requisição POST para "/api/reservas/ativas"
    Then o sistema retorna uma mensagem "Nenhuma reserva ativa encontrada." e o status 404 NOT FOUND
