Feature: Solicitação de Manutenção
  As a professor
  I want gerenciar solicitações de manutenção
  so that eu possa reportar problemas nas salas

Scenario: Visualizar reservas ativas\/finalizadas para solicitar manutenção
  Given eu estou logado na página "Manutencoes"
  When o sistema carrega minhas reservas ativas
  Then eu vejo minha reserva no dia "2025-02-20" das "14:00" às "15:00"

Scenario: Criar uma solicitação de manutenção com sucesso
  Given eu estou logado na página "Manutencoes"
  And eu vejo minha reserva para a sala "001" no dia "2025-01-15" das "14:00" às "15:00"
  When eu preencho o textarea com "Ar condicionado não funciona"
  And eu clico no botão "Solicitar Manutenção"
  Then o sistema deve exibir o alerta "Solicitação de manutenção criada com sucesso!"
  And eu vejo a solicitação com descrição "Ar condicionado não funciona"

Scenario: Tentar criar solicitação sem descrição
  Given eu estou logado na página "Manutencoes"
  And eu vejo minha reserva para a sala "001" no dia "2025-01-15" das "14:00" às "15:00"
  When eu deixo o textarea vazio
  And eu clico no botão "Solicitar Manutenção"
  Then o sistema deve exibir o alerta "O campo 'O que havia de errado na sala?' não pode estar vazio."

Scenario: Editar uma solicitação de manutenção existente
  Given existe uma solicitação de manutenção para a sala "001" com descrição "Luz queimada"
  And eu estou logado na página "Manutencoes"
  When eu clico no botão "Editar" da solicitação
  And eu altero o textarea para "Lâmpada queimada"
  And eu clico no botão "Confirmar Edição"
  Then o sistema deve exibir o alerta "Solicitação de manutenção atualizada com sucesso!"
  And eu vejo a solicitação com descrição "Lâmpada queimada"

Scenario: Excluir uma solicitação de manutenção
  Given existe uma solicitação de manutenção para a sala "001" com descrição "Porta quebrada"
  And eu estou logado na página "Manutencoes"
  When eu clico no botão "Excluir" da solicitação
  And eu confirmo a exclusão no popup
  Then o sistema deve exibir o alerta "Solicitação de manutenção excluída com sucesso!"
  And eu não vejo mais a solicitação com descrição "Porta quebrada"