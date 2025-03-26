import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

Given(
  'eu vejo minha reserva para a sala {string} no dia {string} das {string} às {string}',
  (sala: string, data: string, horaInicio: string, horaFim: string) => {
    cy.intercept('GET', '/api/reservas/3', {
      body: [{
        id: 1,
        sala_id: sala.replace('E', ''),
        nome_sala: sala,
        data,
        start_time: horaInicio,
        end_time: horaFim,
        status: "ativa"
      }]
    }).as('getReservas');
    
    cy.wait('@getReservas');
    cy.contains(`Sala ${sala}`).should('exist');
    cy.contains(`${data} | Hora: ${horaInicio} às ${horaFim}`).should('exist');
  }
);

Given(
    'existe uma solicitação de manutenção para a sala {string} com descrição {string}',
    (sala: string, descricao: string) => {
      // Mock para verificar as reservas ativas
      cy.intercept('GET', '/api/reservas/3', {
        body: [{
          id: 1,
          sala_id: sala,
          nome_sala: sala,
          data: "2025-01-15",
          start_time: "14:00",
          end_time: "15:00",
          status: "ativa"
        }]
      }).as('getReservas');
  
      cy.intercept('GET', '/solicitacoes/manutencao', {
        body: [{
          id: 1,
          reserva_id: 1,
          descricao: descricao
        }]
      }).as('getSolicitacoes');
  

      cy.intercept('PUT', '/solicitacoes/manutencao/1', {
        statusCode: 200,
        body: {
          mensagem: "Solicitação de manutenção atualizada com sucesso",
          id: 1,
          descricao: "Lâmpada queimada"
        }
      }).as('putSolicitacao');
  
      cy.visit('/Manutencoes');

      cy.wait('@getReservas');
      
      cy.get('.reserva-card').should('be.visible');
      
      cy.contains(`Sala ${sala}`).should('exist');
      
      cy.get('.reserva-card').within(() => {

        cy.contains('p', 'Solicitação realizada:').should('exist');

        cy.contains('p', descricao).should('exist');
      });
    }
  );
  

When("o sistema carrega minhas reservas ativas", function () {
    cy.contains(`Sala `).should("exist");

});

When('eu preencho o textarea com {string}', (descricao: string) => {
  cy.get('textarea[placeholder="O que havia de errado na sala?"]')
    .first()
    .type(descricao);
});

When('eu deixo o textarea vazio', () => {
  cy.get('textarea[placeholder="O que havia de errado na sala?"]')
    .first()
    .clear();
});

When('eu clico no botão {string}', (botao: string) => {
  cy.contains('button', botao).click();
});

When('eu clico no botão {string} da solicitação', (botao: string) => {
    // Espera que o botão de edição esteja visível antes de clicar
    cy.contains('button', botao).should('be.visible').click();
  });
  

When('eu altero o textarea para {string}', (descricao: string) => {
  cy.get('textarea[placeholder="O que havia de errado na sala?"]')
    .first()
    .clear()
    .type(descricao);
});

When('eu confirmo a exclusão no popup', () => {
  cy.contains('button', 'Excluir Solicitação').click();
});

Then('eu vejo minha reserva no dia {string} das {string} às {string}', 
  (data: string, horaInicio: string, horaFim: string) => {
    cy.get(".reserva-card").contains(`${data} | Hora: ${horaInicio} às ${horaFim}`).should('exist');
  }
);

Then('o sistema deve exibir o alerta {string}', (mensagem: string) => {
  cy.on('window:alert', (text) => {
    expect(text).to.equal(mensagem);
  });
});

Then('eu vejo a solicitação com descrição {string}', (descricao: string) => {
    cy.get('.reserva-card').within(() => {
      cy.contains('p', 'Solicitação realizada:').should('exist');
      cy.contains('p', descricao).should('exist');
    });
  });

Then('eu não vejo mais a solicitação com descrição {string}', (descricao: string) => {
  cy.contains('p', descricao).should('not.exist');
});