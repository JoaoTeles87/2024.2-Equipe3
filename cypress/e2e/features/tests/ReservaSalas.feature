Feature: Pesquisar salas
  As a professor
  I want pesquisar salas
  so that eu possa fazer reservas

Scenario: Visualizar salas de reunião disponíveis em 15/01 das 14h às 15h com ar condicionado
  Given eu estou logado na página "Reservar"
  And no campo "Tipo de sala" está selecionado "Reunião"
  And no campo "Data" está inserido "2025-01-15"
  And no campo "Hora Início" está selecionada a opção "14:00"
  And no campo "Hora Fim" está selecionada a opção "15:00"
  And no campo "Equipamentos" está selecionada a opção "Ar-condicionado"
  When eu seleciono a opção "Procurar"
  Then é exibida a sala "E001" como sala disponível

Scenario: Visualizar salas auditório disponíveis em 16/01 das 10h às 12h com projetor
  Given eu estou logado na página "Reservar"
  And no campo "Tipo de sala" está selecionado "Auditório"
  And no campo "Data" está inserido "2025-01-16"
  And no campo "Hora Início" está selecionada a opção "10:00"
  And no campo "Hora Fim" está selecionada a opção "12:00"
  And no campo "Equipamentos" está selecionada a opção "Projetor"
  When eu seleciono a opção "Procurar"
  Then é exibida a sala "E002" como sala disponível

Scenario: Pesquisar salas sem preencher o horário
  Given eu estou logado na página "Reservar"
  And no campo "Tipo de sala" está selecionado "Reunião"
  And no campo "Data" está inserido "2025-01-17"
  When eu seleciono a opção "Procurar"
  Then o sistema deve exibir a mensagem "Data e horários são obrigatórios"

Scenario: Pesquisar salas sem nenhuma disponível
  Given eu estou logado na página "Reservar"
  And no campo "Tipo de sala" está selecionado "Auditório"
  And no campo "Data" está inserido "2025-12-31"
  And no campo "Hora Início" está selecionada a opção "09:00"
  And no campo "Hora Fim" está selecionada a opção "10:00"
  And no campo "Equipamentos" está selecionada a opção "Ar-condicionado"
  When eu seleciono a opção "Procurar"
  Then uma mensagem informa que nenhuma sala está disponível

Scenario: Realizar uma reserva com sucesso
  Given eu estou logado na página "Reservar"
  And no campo "Tipo de sala" está selecionado "Reunião"
  And no campo "Data" está inserido "2025-01-16"
  And no campo "Hora Início" está selecionada a opção "10:00"
  And no campo "Hora Fim" está selecionada a opção "11:00"
  And no campo "Equipamentos" está selecionada a opção "Ar-condicionado"
  When eu seleciono a opção "Procurar"
  And eu clico no botão "Reservar" da sala "E006"
  Then o sistema deve exibir a mensagem "Reserva criada com sucesso!"

Scenario: Tentar reservar uma sala com horário já reservado por outro professor
  Given existe uma reserva na sala "E002" para o dia "2024-01-16" das "10:00" às "11:00"
  And eu estou logado na página "Reservar"
  And no campo "Tipo de sala" está selecionado "Reunião"
  And no campo "Data" está inserido "2024-01-16"
  And no campo "Hora Início" está selecionada a opção "10:00"
  And no campo "Hora Fim" está selecionada a opção "11:00"
  When eu seleciono a opção "Procurar"
  And eu clico no botão "Reservar" da sala "E001"
  Then o sistema deve exibir a mensagem "Sala já reservada para esse horário"