Feature: Obtenção de Avaliação Individual

  SCENARIO: Deve exibir os detalhes de uma avaliação existente
    GIVEN que eu estou na página de "Avaliações de Usuários" e existe uma avaliação com ID "1"
    WHEN eu acesso a página de detalhes da avaliação com ID "1"
    THEN o sistema deve exibir as informações completas da avaliação

  SCENARIO: Deve exibir uma mensagem de erro para uma avaliação inexistente
    GIVEN que eu estou na página de "Avaliações de Usuários" e que não existe uma avaliação com ID "999"
    WHEN eu acesso a página de detalhes da avaliação com ID "999" pela barra de pesquisa
    THEN o sistema deve exibir uma mensagem de erro informando que a avaliação não foi encontrada
