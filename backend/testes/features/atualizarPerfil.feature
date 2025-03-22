Feature: Atualizar perfil

  Scenario: Atualizar perfil existente
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando as informações de perfil a serem editadas
    Then o sistema retorna a mensagem "Perfil atualizado com sucesso." e o status 200 OK

  Scenario: Atualizar perfil com CPF inválido
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando CPF "123"
    Then o sistema retorna a mensagem "O CPF fornecido é inválido." e o status 400 BAD REQUEST

  Scenario: Atualizar perfil com nome inválido
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando o nome "A"
    Then o sistema retorna a mensagem "O nome é inválido. Deve conter apenas letras e espaços, e ter pelo menos 2 caracteres." e o status 400 BAD REQUEST
