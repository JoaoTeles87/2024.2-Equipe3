Feature: Atualizar Avaliação de Sala

    SCENARIO: Sucesso ao atualizar avaliação de sala
        GIVEN  eu estou na página “Avaliar Sala” para editar uma avaliação existente
        AND eu seleciono a avaliação "5"
        AND o campo “Nota” está preenchido com “4” estrelas
        AND o campo “Comentário” está preenchido com “Boa sala, mas precisa de melhorias.”
        WHEN eu modifico o campo “Nota” para “5” estrelas
        AND eu modifico o campo “Comentário” para “Excelente sala, muito boa para reuniões!”
        AND eu clico no botão “Atualizar Avaliação”
        THEN a mensagem “Avaliação atualizada com sucesso!” é exibida
        THEN o usuário é redirecionado para a página da avaliação atualizada
        THEN as alterações feitas são refletidas na página da avaliação.

    SCENARIO: Sucesso ao atualizar avaliação sem modificar nenhum campo
        GIVEN  eu estou na página “Avaliar Sala” para editar uma avaliação existente
        AND o campo “Nota” está preenchido com “4” estrelas
        AND o campo “Comentário” está preenchido com “Boa sala, mas precisa de melhorias.”
        WHEN eu não modifico os campos “Nota” e “Comentário”
        AND eu clico no botão “Atualizar Avaliação”
        THEN a mensagem “Avaliação atualizada com sucesso!” é exibida
        THEN o usuário é redirecionado para a página da avaliação sem alterações.

    SCENARIO: Falha ao atualizar avaliação se a avaliação não for encontrada
        GIVEN  eu estou na página para editar uma avaliação
        AND o ID da avaliação fornecido não corresponde a uma avaliação existente
        WHEN eu tento acessar a página para editar a avaliação
        THEN uma mensagem de erro “Avaliação não encontrada para o ID Fornecido” é exibida
        AND eu clico no botão "Voltar"
        AND eu não sou redirecionado para a página de edição