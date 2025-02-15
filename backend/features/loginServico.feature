Feature: Autenticação de usuários

  Scenario: Sucesso no login
    Given o usuário possui um email e senha válidos
    When ele envia uma requisição POST para "/api/login"
    Then a resposta deve conter os dados do usuário
    And o status code deve ser 200

  Scenario: Fracasso no login por senha incorreta
    Given o usuário possui um email válido, mas senha inválida
    When ele envia uma requisição POST para "/api/login"
    Then a resposta deve conter a mensagem "Usuário ou senha inválidos."
    And o status code deve ser 401

  Scenario: Fracasso no login por falta de email ou senha
    Given o usuário envia uma requisição sem email ou senha
    When ele envia uma requisição POST para "/api/login"
    Then a resposta deve conter a mensagem "Usuário e senha são obrigatórios."
    And o status code deve ser 400
