Feature: Gerenciar Perfil
  As a usuário
  I want gerenciar meu perfil
  so that eu possa manter meus dados atualizados e excluir minha conta

Scenario: Visualizar dados do perfil
  Given eu estou na página "Perfil"
  Then devo ver meus dados pessoais
  And devo ver minhas reservas ativas
  And devo ver meu histórico de reservas

Scenario: Editar perfil com sucesso
  Given eu estou na página "Perfil"
  When eu clico no botão "Editar"
  And altero o campo "Nome" para "Novo Nome"
  And altero o campo "Email" para "novo@gmail.com"
  And clico em "Salvar alterações"

Scenario: Falha ao excluir perfil com reservas ativas
  Given eu estou na página "Perfil"
  And possuo uma reserva ativa
  When eu clico no botão "Excluir conta"
  And preencho a senha correta
  And clico em "Confirmar exclusão"

Scenario: Cancelar reserva ativa com sucesso
  Given eu estou na página "Perfil"
  And possuo uma reserva ativa
  When eu clico no botão "Excluir" na reserva
  Then o sistema deve exibir a mensagem "Reserva cancelada com sucesso!"
  And devo ver a mensagem "Não há reservas ativas no momento"

Scenario: Excluir perfil com sucesso
  Given eu estou na página "Perfil"
  And não possuo reservas ativas
  When eu clico no botão "Excluir conta"
  And preencho a senha correta
  And clico em "Confirmar exclusão"
  And devo ser redirecionado para a página inicial
  
Scenario: Visualizar histórico de reservas vazio
  Given eu estou na página "Perfil"
  And não possuo reservas anteriores
  Then devo ver a mensagem "Não há histórico de reservas"