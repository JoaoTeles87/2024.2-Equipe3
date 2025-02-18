Feature: Criar/remover solicitação de recursos de sala

    Scenario: sucesso ao criar solicitação de recursos para uma reserva ativa com todos os campos preenchidos
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: "Projetor, Teclado", itens_nao_listados: "Extensão elétrica", observacoes: "Para aula prática"
    Then o sistema retorna "mensagem" "Parabéns, sua solicitação de recursos foi criada!" e um status "201"
    And a reserva_id "1" possui uma solicitação com recursos "Projetor, Teclado", itens_nao_listados "Extensão elétrica" e observacoes "Para aula prática"

    Scenario: fracasso ao criar solicitação de recursos com campos preenchidos com espaços ou não preenchidos
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: " ", itens_nao_listados: " ", observacoes: " "
    Then o sistema retorna "erro" "Você deve selecionar um recurso ou especificar itens não listados." e um status "400"

    Scenario: fracasso ao criar solicitação de recursos com apenas o campo observacoes preenchido
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: " ", itens_nao_listados: " ", observacoes: "Para aula prática"
    Then o sistema retorna "erro" "Você deve selecionar um recurso ou especificar itens não listados." e um status "400"

    Scenario: sucesso ao criar solicitação de recursos sem preencher o campo itens_nao_listados
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: "Projetor, Teclado", itens_nao_listados: " ", observacoes: "Para aula prática"
    Then o sistema retorna "mensagem" "Parabéns, sua solicitação de recursos foi criada!" e um status "201"
    And a reserva_id "1" possui uma solicitação com recursos "Projetor, Teclado", itens_nao_listados " " e observacoes "Para aula prática"

    Scenario: sucesso ao criar solicitação de recursos sem preencher o campo itens_nao_listados e o campo observacoes
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: "Projetor, Teclado", itens_nao_listados: " ", observacoes: " "
    Then o sistema retorna "mensagem" "Parabéns, sua solicitação de recursos foi criada!" e um status "201"
    And a reserva_id "1" possui uma solicitação com recursos "Projetor, Teclado", itens_nao_listados " " e observacoes " "

    Scenario: sucesso ao criar solicitação de recursos com o campo de recursos vazio e apenas especificando os itens não listados
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: " ", itens_nao_listados: "Extensão elétrica", observacoes: " "
    Then o sistema retorna "mensagem" "Parabéns, sua solicitação de recursos foi criada!" e um status "201"
    And a reserva_id "1" possui uma solicitação com recursos " ", itens_nao_listados "Extensão elétrica" e observacoes " "

    Scenario: sucesso ao criar solicitação de recursos com o campo de recursos vazio e especificando os itens não listados e as observacoes
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: " ", itens_nao_listados: "Extensão elétrica", observacoes: "Para aula prática"
    Then o sistema retorna "mensagem" "Parabéns, sua solicitação de recursos foi criada!" e um status "201"
    And a reserva_id "1" possui uma solicitação com recursos " ", itens_nao_listados "Extensão elétrica" e observacoes "Para aula prática"

    Scenario: sucesso ao editar uma solicitação de recursos existente
    Given o professor possui uma solicitação de recursos associada a reserva_id "1"
    When ele envia uma requisição PUT /solicitacoes/recursos/"1" contendo o ID da solicitação e os novos detalhes da solicitação recursos: "Projetor, Caixas de som", observacoes: "Para evento especial"
    Then o sistema retorna "mensagem" "Solicitação de recursos atualizada com sucesso" e um status "200"
    And o sistema atualiza os detalhes da solicitação: recursos: "Projetor, Caixas de som", observacoes: "Para evento especial"

    Scenario: fracasso ao editar uma solicitação de recursos com apenas o campo observacoes preenchido
    Given o professor possui uma reserva ativa com reserva_id "1"
    When ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "1", recursos: " ", itens_nao_listados: " ", observacoes: "Para aula prática"
    Then o sistema retorna "erro" "Você deve selecionar um recurso ou especificar itens não listados." e um status "400"

    Scenario: sucesso ao excluir uma solicitação de recursos existente
    Given o professor possui uma solicitação de recursos associada a reserva_id "1"
    When ele envia uma requisição DELETE /solicitacoes/recursos/"1" contendo o ID da solicitação
    Then o sistema remove a solicitação do banco de dados e retorna um status "204"