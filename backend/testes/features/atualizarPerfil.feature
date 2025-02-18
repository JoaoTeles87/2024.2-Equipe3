Feature: Atualizar perfil

  Scenario: Atualizar perfil existente
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando as informações de perfil a serem editadas
    Then o sistema retorna a mensagem "Perfil atualizado com sucesso." e o status 200 OK

  Scenario: Atualizar perfil com dados inválidos
    Given o aluno João deseja editar seu perfil
    When ele envia uma requisição PUT para "/api/perfil" especificando o nome "A" e o CPF "123"
    Then o sistema retorna a mensagem "O CPF fornecido é inválido. Use o formato XXX.XXX.XXX-XX." e o status 400 BAD REQUEST


