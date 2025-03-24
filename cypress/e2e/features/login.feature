Feature: Login de usuário no frontend

  Scenario: Login bem-sucedido
    Given o usuário está na página de login
    When ele preenche o campo de email com "demostenes@example.com"
    And ele preenche o campo de senha com "SecurePassword123"
    And ele clica no botão "Entrar"
    Then ele deve ser redirecionado para a página principal
    

  Scenario: Login falha com senha incorreta
    Given o usuário está na página de login
    When ele preenche o campo de email com "demostenes@example.com"
    And ele preenche o campo de senha com "SecureIncorreta123"
    And ele clica no botão "Entrar"
    Then ele deve ver uma mensagem de erro "Usuário ou senha inválidos."
    And ele deve permanecer na página de login

  Scenario: Login falha com campos vazios
    Given o usuário está na página de login
    When ele clica no botão "Entrar" sem preencher os campos
    Then ele deve ver uma mensagem de erro "Usuário e senha são obrigatórios."
    And ele deve permanecer na página de login
    
  Scenario: Navegar para a página de cadastro
    Given o usuário está na página de login
    When ele clica no link "Não tem conta ainda?"
    Then ele deve ser redirecionado para a página de cadastro