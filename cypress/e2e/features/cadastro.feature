Feature: Cadastro de usuário no frontend

  Scenario: Cadastro bem-sucedido
    Given o usuário está na página de cadastro
    When ele preenche o campo de nome com "Demóstenes Silva"
    And ele preenche o campo de CPF com "123.456.789-00"
    And ele preenche o campo de email com "demostenes@example.com"
    And ele preenche o campo de senha com "SecurePassword123"
    And ele preenche o campo de confirmar senha com "SecurePassword123"
    And ele seleciona a opção "Não" para professor
    And ele clica no botão "Criar"
    Then ele deve ver uma mensagem de sucesso
    And deve haver um botão para voltar à área de login

  Scenario: Cadastro como professor
    Given o usuário está na página de cadastro
    When ele preenche o campo de nome com "Prof. Demóstenes"
    And ele preenche o campo de CPF com "987.654.321-00"
    And ele preenche o campo de email com "prof.demostenes@example.com"
    And ele preenche o campo de senha com "SecurePassword123"
    And ele preenche o campo de confirmar senha com "SecurePassword123"
    And ele seleciona a opção "Sim" para professor
    And ele preenche o campo SIAPE com "123456"
    And ele clica no botão "Criar"
    Then ele deve ver uma mensagem de sucesso
    And deve haver um botão para voltar à área de login

  Scenario: Erro no cadastro com senhas diferentes
    Given o usuário está na página de cadastro
    When ele preenche o campo de nome com "Demóstenes Silva"
    And ele preenche o campo de CPF com "123.456.789-00"
    And ele preenche o campo de email com "demostenes@example.com"
    And ele preenche o campo de senha com "SecurePassword123"
    And ele preenche o campo de confirmar senha com "DifferentPassword456"
    And ele seleciona a opção "Não" para professor
    And ele clica no botão "Criar"
    Then ele deve ver uma mensagem de erro "As senhas não coincidem."
    
  Scenario: Voltar para login a partir do cadastro
    Given o usuário está na página de cadastro
    When ele clica no link "Já possuo uma conta"
    Then ele deve ser redirecionado para a página de login