Feature: Deletar Perfil

  Scenario: Deletar perfil com sucesso
    Given o aluno João deseja excluir seu perfil e não possui reservas ativas
    When ele envia uma requisição DELETE para "/api/perfil" com o ID "1" e a senha "senha123"
    Then o sistema retorna a mensagem "Perfil excluído com sucesso!" e o status 200 OK

  Scenario: Tentativa de deletar perfil com reservas ativas
    Given o aluno João tem reservas ativas no sistema
    When ele tenta excluir seu perfil enviando uma requisição DELETE para "/api/perfil" com o ID "1" e a senha "senha123"
    Then o sistema retorna a mensagem "Não é possível excluir o perfil com reservas ativas" e o status 400 BAD REQUEST

  Scenario: Tentativa de deletar perfil com ID de usuário incorreto
    Given o aluno João tenta excluir o perfil com a senha errada
    When ele envia uma requisição DELETE para "/api/perfil" especificando o ID "999" e a senha errada "senhaErrada"
    Then o sistema retorna a mensagem "Perfil não encontrado para o ID fornecido" e o status 404 NOT FOUND

  Scenario: Tentativa de deletar perfil com senha errada
    Given o aluno João tenta excluir o perfil com a senha errada
    When ele envia uma requisição DELETE para "/api/perfil" especificando o ID "1" e a senha errada "senhaErrada"
    Then o sistema retorna a mensagem "Senha incorreta" e o status 401 UNAUTHORIZED