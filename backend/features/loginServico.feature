Feature: Autenticação de usuários

  Scenario: Sucesso no login
    Given o usuário possui o email "demostenes@example.com" e a senha "SecurePassword123" válidos
    When ele envia uma requisição POST para "/api/login" com os dados "demostenes@example.com" e "SecurePassword123"
    Then a resposta deve conter o email "demostenes@example.com" e a rota "/api/reservas"
    And o status code deve ser "200"

  Scenario: Fracasso no login por senha incorreta
    Given o usuário possui o email "demostenes@example.com" válido e a senha "SecureIncorreta123" inválida
    When ele envia uma requisição POST para "/api/login" com os dados "demostenes@example.com" e "SecureIncorreta123"
    Then a resposta deve conter a mensagem "Usuário ou senha inválidos."
    And o status code deve ser "401"

  Scenario: Fracasso no login por falta de email ou senha
    Given o usuário envia uma requisição sem email ou senha
    When ele envia uma requisição POST para "/api/login" com os dados " " e " "
    Then a resposta deve conter a mensagem "Usuário e senha são obrigatórios."
    And o status code deve ser "400"

 