Feature: Deletar Avaliação

  SCENARIO: Deletar uma avaliação existente
    GIVEN que eu estou na página de "Avaliações de Usuários" e existe uma avaliação com ID "1"
    WHEN eu acesso a página de exclusão da avaliação com ID "1"
    AND eu confirmo a exclusão da avaliação
    THEN o sistema deve exibir uma mensagem de sucesso informando que a avaliação foi deletada
    AND a avaliação não deve mais estar na lista de avaliações

  SCENARIO: Tentar deletar uma avaliação inexistente
    GIVEN que eu estou na página de "Avaliações de Usuários" e não existe uma avaliação com ID "999"
    WHEN eu acesso a página de exclusão da avaliação com ID "999"
    AND eu confirmo a exclusão da avaliação
    THEN o sistema deve exibir uma mensagem de erro informando que a avaliação não foi encontrada
