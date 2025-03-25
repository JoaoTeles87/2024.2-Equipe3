Feature: Listar Avaliações de Usuários

  SCENARIO: Sucesso ao listar avaliações quando há avaliações disponíveis
    GIVEN  eu estou na página "Avaliações de Usuários"
    AND há avaliações cadastradas
    WHEN eu acesso a página de "Avaliações de Usuários"
    THEN as avaliações devem ser listadas na página
    AND cada avaliação deve mostrar as informações de "ID da Reserva", "ID da Sala", "ID do Usuário", "Nota", "Comentário" e "Data da Avaliação"
    AND deve ser possível clicar em uma avaliação para visualizar mais detalhes

  SCENARIO: Exibição de mensagem quando não há avaliações cadastradas
    GIVEN  eu estou na página "Avaliações de Usuários"
    AND não há avaliações cadastradas
    WHEN eu acesso a página de "Avaliações de Usuários"
    THEN a mensagem "Nenhuma avaliação encontrada." deve ser exibida

