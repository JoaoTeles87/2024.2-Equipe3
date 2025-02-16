Feature: Serviço de Cadastro de Usuários

  Scenario: Sucesso no cadastro de usuário
    Given o usuário deseja se cadastrar
    When ele informa o nome "Demosténes"
    And ele informa o CPF "126.456.789-00"
    And ele informa o email "demostenes@example.com"
    And ele informa se é professor "N"
    And ele informa a senha "SecurePassword123"
    And ele informa a confirmação da senha "SecurePassword123"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "Cadastro criado com sucesso!"
    And o status code deve ser 201

  Scenario: Sucesso no cadastro de professor
    Given o usuário deseja se cadastrar
    When ele informa o nome "Paula"
    And ele informa o CPF "321.879.789-33"
    And ele informa o email "vanessa@example.com"
    And ele informa se é professor "S"
    And ele informa o SIAPE "101010"
    And ele informa a senha "12345678"
    And ele informa a confirmação da senha "12345678"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "Cadastro criado com sucesso!"
    And o status code deve ser 201

  Scenario: Fracasso no cadastro por campos obrigatórios não preenchidos
    Given o usuário deseja se cadastrar
    When ele informa o nome "João"
    And ele informa o CPF "987.654.321-00"
    And ele informa o email "joao@iat.com"
    And ele informa se é professor "N"
    And ele informa a senha "Password123"
    And ele deixa o campo "Confirmar Senha" com ""
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "Confirmar Senha é obrigatório."
    And o status code deve ser 400

  Scenario: Fracasso no cadastro por duplicação de ID única
    Given o usuário deseja se cadastrar
    When ele informa o nome "Carlos Mendes"
    And ele informa o CPF "126.456.789-00"
    And ele informa o email "demostenes@example.com"
    And ele informa se é professor "S"
    And ele informa o SIAPE "010101"
    And ele informa a senha "Password456"
    And ele informa a confirmação da senha "Password456"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "Erro: email/cpf já está registrado."
    And o status code deve ser 409

  Scenario: Fracasso no cadastro por senhas que não coincidem
    Given o usuário deseja se cadastrar
    When ele informa o nome "Beatriz"
    And ele informa o CPF "789.456.123-00"
    And ele informa o email "Beatriz.oliveira@example.com"
    And ele informa se é professor "N"
    And ele informa a senha "MyPassword123"
    And ele informa a confirmação da senha "DifferentPassword123"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "As senhas não coincidem."
    And o status code deve ser 400

    Scenario: Fracasso no cadastro por formato inválido de email
    Given o usuário deseja se cadastrar
    When ele informa o nome "Lucas"
    And ele informa o CPF "987.654.321-00"
    And ele informa o email "lucas.example.com"
    And ele informa se é professor "N"
    And ele informa a senha "SenhaForte123"
    And ele informa a confirmação da senha "SenhaForte123"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "Formato de email inválido. Use um email válido, como exemplo@dominio.com."
    And o status code deve ser 400

  Scenario: Fracasso no cadastro por formato inválido de CPF
    Given o usuário deseja se cadastrar
    When ele informa o nome "Fabricio"
    And ele informa o CPF "123"
    And ele informa o email "fabricio@example.com"
    And ele informa se é professor "N"
    And ele informa a senha "SenhaSegura456"
    And ele informa a confirmação da senha "SenhaSegura456"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "CPF inválido. Digite um CPF válido no formato XXX.XXX.XXX-XX."
    And o status code deve ser 400
  
  Scenario: Fracasso no cadastro por siape já registrado
    Given o usuário deseja se cadastrar
    When ele informa o nome "Max"
    And ele informa o CPF "987.654.321-00"
    And ele informa o email "max@gmail.com"
    And ele informa se é professor "S"
    And ele informa o SIAPE "101010"
    And ele informa a senha "Senha123"
    And ele informa a confirmação da senha "Senha123"
    And ele envia uma requisição POST para "/api/cadastro"
    Then a resposta deve conter a mensagem "Erro: siape já está registrado."

