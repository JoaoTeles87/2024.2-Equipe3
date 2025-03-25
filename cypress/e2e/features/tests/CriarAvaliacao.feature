Feature: Criar Avaliação de Sala

    SCENARIO: Sucesso ao enviar avaliação de sala
        GIVEN  eu estou na página “Avaliar Sala”
        AND o campo “ID da Reserva” está preenchido com “12345”
        AND o campo “ID da Sala” está preenchido com “67890”
        AND o campo “ID do Usuário” está preenchido com “1”
        AND o campo “Nota” está preenchido com “5” estrelas
        AND o campo “Comentário” está preenchido com “Ótima sala!”
        WHEN eu clico no botão “Enviar Avaliação”
        THEN a mensagem “Avaliação enviada com sucesso!” é exibida
        THEN o usuário é redirecionado para a página “Avaliações”
        THEN os campos de avaliação são limpos.

    SCENARIO: Falta o ID da Reserva ao enviar avaliação
        GIVEN  eu estou na página “Avaliar Sala”
        AND o campo “ID da Reserva” está vazio
        AND o campo “ID da Sala” está preenchido com “67890”
        AND o campo “ID do Usuário” está preenchido com “1”
        AND o campo “Nota” está preenchido com “4” estrelas
        WHEN eu clico no botão “Enviar Avaliação”
        THEN a mensagem “ID da Reserva é obrigatório.” é exibida
        THEN o envio da avaliação é bloqueado.

    SCENARIO: Falta o ID da Sala ao enviar avaliação
        GIVEN  eu estou na página “Avaliar Sala”
        AND o campo “ID da Reserva” está preenchido com “12345”
        AND o campo “ID da Sala” está vazio
        AND o campo “ID do Usuário” está preenchido com “1”
        AND o campo “Nota” está preenchido com “4” estrelas
        WHEN eu clico no botão “Enviar Avaliação”
        THEN a mensagem “ID da Sala é obrigatório.” é exibida
        THEN o envio da avaliação é bloqueado.

    SCENARIO: Falta o ID do Usuário ao enviar avaliação
        GIVEN  eu estou na página “Avaliar Sala”
        AND o campo “ID da Reserva” está preenchido com “12345”
        AND o campo “ID da Sala” está preenchido com “67890”
        AND o campo “ID do Usuário” está vazio
        AND o campo “Nota” está preenchido com “4” estrelas
        WHEN eu clico no botão “Enviar Avaliação”
        THEN a mensagem “ID do Usuário é obrigatório.” é exibida
        THEN o envio da avaliação é bloqueado.

    SCENARIO: Falta a Nota ao enviar avaliação
        GIVEN  eu estou na página “Avaliar Sala”
        AND o campo “ID da Reserva” está preenchido com “12345”
        AND o campo “ID da Sala” está preenchido com “67890”
        AND o campo “ID do Usuário” está preenchido com “1”
        AND o campo “Nota” está vazio
        WHEN eu clico no botão “Enviar Avaliação”
        THEN a mensagem “Nota é obrigatória.” é exibida
        THEN o envio da avaliação é bloqueado.
