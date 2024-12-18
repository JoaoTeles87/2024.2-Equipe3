SCENARIO: Visualizar salas de reunião disponíveis em 15/01 das 14h às 15h com ar condicionado
    GIVEN  eu estou logado como "professor" na página “Reservar"
    AND no campo “tipo de sala” está selecionado “reunião"
    AND no campo “data” está inserido “15/01/2025”
    AND no campo “Hora Início” está selecionada a opção “14:00"
    AND no campo “Hora Fim” está selecionada a opção “15:00"
    AND no campo “Equipamentos” está selecionada a opção “Ar-condicionado"
    WHEN eu seleciono a opção “Procurar"
    THEN é exibida a sala "E001" como sala disponível