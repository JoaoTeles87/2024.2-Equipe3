Feature: Atualizar Perfil

  Scenario: Atualizar um perfil existente
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando as informações de perfil a serem editadas
    And modifica o nome de "João" para "João Pereira" e o CPF de "123.456.789-00" para "987.654.321-00"
    Then o sistema retorna a mensagem "Perfil atualizado com sucesso." e o status 200 OK

  Scenario: Tentar atualizar um perfil que não existe
    Given o aluno João  deseja editar um perfil cuja qual não está presente no sistema
    When ele envia uma requisição PUT para "/api/perfil" especificando as informações de perfil a serem editadas
    And modifica o nome de "João" para "João Pereira" e o CPF de "123.456.789-00" para "987.654.321-00"
    Then o sistema retorna a mensagem "Usuário não encontrado." e o status 404 NOT FOUND
  
  Scenario: Atualizar perfil com e-mail já em uso
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando um e-mail que já está em uso
    Then o sistema retorna a mensagem "E-mail já cadastrado" e o status 409 CONFLICT

  Scenario: Atualizar perfil com dados inválidos
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando o nome "A" e o CPF "123"
    Then o sistema retorna a mensagem "Dados inválidos" e o status 400 BAD REQUEST
