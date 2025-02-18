Feature: Criar/remover solicitação de manutenção de sala

    Scenario: sucesso ao criar uma solicitação de manutenção para uma reserva concluída
    Given o professor possui uma reserva de sala reserva_id "1" que já foi encerrada
    When ele envia uma requisição POST /solicitacoes/manutencao com os dados: reserva_id: "1", descricao: "Mesa quebrada."
    Then o sistema retorna "mensagem" "Parabéns, sua solicitação de manutenção foi criada!" e um status "201"
    And a reserva reserva_id: "1" possui uma solicitação de manutenção com descricao: "Mesa quebrada."

    Scenario: fracasso ao criar uma solicitação de manutenção sem preencher o campo descricao
    Given o professor possui uma reserva de sala reserva_id "1" que já foi encerrada
    When ele envia uma requisição POST /solicitacoes/manutencao com os dados: reserva_id: "1", descricao: " "
    Then o sistema retorna "erro" "O campo 'descricao' não pode estar vazio." e um status "400"

    Scenario: sucesso ao editar uma solicitação de manutenção existente
    Given o professor já criou uma solicitação de manutenção associada a reserva_id "1"
    When ele envia uma requisição PUT /solicitacoes/manutencao/"1" contendo o ID da solicitação de manutenção e a alteração descricao: "Mesa e cadeira quebradas."
    Then o sistema retorna "mensagem" "Solicitação de manutenção atualizada com sucesso" e um status "200"
    And o sistema atualiza os detalhes da solicitação com descricao: "Mesa e cadeira quebradas."

    Scenario: fracasso ao editar solicitação de manutenção sem preencher o campo descricao
    Given o professor já criou uma solicitação de manutenção associada a reserva_id "1"
    When ele envia uma requisição PUT /solicitacoes/manutencao/"1" contendo o ID da solicitação de manutenção e a alteração descricao: " "
    Then o sistema retorna "erro" "A descrição da manutenção não pode ser vazia" e um status "400"

    Scenario: sucesso ao excluir uma solicitação de manutenção existente
    Given o professor já criou uma solicitação de manutenção associada a reserva_id "1"
    When ele envia uma requisição DELETE /solicitacoes/manutencao/"1",
    Then o sistema remove a solicitação do banco de dados e retorna um status "204"