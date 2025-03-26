import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

const selectors = {
  profileSection: '[data-testid="profile-section"]',
  profileData: '[data-testid="profile-data"]',
  reservationSection: '[data-testid="reservation-section"]', 
  historySection: '[data-testid="history-section"]',
  editButton: '[data-testid="edit-button"]',
  deleteButton: '[data-testid="delete-button"]',
  confirmDeleteButton: '[data-testid="confirm-delete-button"]',
  saveButton: '[data-testid="save-button"]',
  passwordInput: 'input[type="password"]',
  deleteReservationButton: '[data-testid="delete-reservation-button"]'
};

// Given steps
Given("eu estou na página {string}", (page: string) => {
  cy.visit(`/${page.toLowerCase()}`);
  cy.intercept('GET', '**/api/perfil').as('getPerfil');
  cy.intercept('GET', '**/api/reservas/ativas').as('getReservas'); 
  cy.intercept('GET', '**/api/reservas/historico/*').as('getHistorico');
  cy.wait(['@getPerfil', '@getReservas', '@getHistorico']);
});

Given("não possuo reservas ativas", () => {
  cy.get(selectors.reservationSection).within(() => {
    cy.contains('Não há reservas ativas no momento').should('exist');
  });
});

Given("possuo uma reserva ativa", () => {
  cy.get(selectors.reservationSection).within(() => {
    cy.contains('Próxima Reserva').should('exist');
  });
});

Given("não possuo reservas anteriores", () => {
  cy.get(selectors.historySection).within(() => {
    cy.contains('Não há histórico de reservas').should('exist');
  });
});

// When steps
When("eu clico no botão {string}", (button: string) => {
  switch(button) {
    case "Editar":
      cy.get(selectors.editButton).click();
      break;
    case "Excluir conta":
      cy.get(selectors.deleteButton).click();
      break;
    case "Excluir":
      cy.get(selectors.deleteReservationButton).first().click();
      break;
    default:
      cy.contains('button', button).click();
  }
});

When("eu clico no botão {string} na reserva", () => {
    cy.intercept('DELETE', '**/api/reservas/ativas/*').as('deleteReserva');
    
    cy.get(selectors.reservationSection).should('be.visible').within(() => {
      cy.get(selectors.deleteReservationButton)
        .should('exist')
        .should('be.visible')
        .click();
    });
  
    cy.on('window:confirm', () => true);
    cy.wait('@deleteReserva');
  });

When("altero o campo {string} para {string}", (field: string, value: string) => {
  switch(field) {
    case "Nome":
      cy.get('input[type="text"]').first().clear().type(value);
      break;
    case "Email":
      cy.get('input[type="email"]').clear().type(value);
      break;
    default:
      cy.get(`input[name="${field.toLowerCase()}"]`).clear().type(value);
  }
});

When("preencho a senha correta", () => {
  cy.get(selectors.passwordInput).type("123456");
});

When("clico em {string}", (buttonText: string) => {
  switch(buttonText) {
    case "Salvar alterações":
      cy.get(selectors.saveButton).click();
      break;
    case "Confirmar exclusão":
      cy.get(selectors.confirmDeleteButton).click();
      break;
    default:
      cy.contains('button', buttonText).click();
  }
});

When("confirmo o cancelamento", () => {
  cy.on('window:confirm', () => true);
});

// Then steps
Then("devo ver meus dados pessoais", () => {
    cy.get(selectors.profileSection).should('be.visible');
    cy.get(selectors.profileData).first().should('be.visible').within(() => {
      cy.contains('Nome:').should('be.visible');
      cy.contains('Email:').should('be.visible');
    });
  });
  
  Then("devo ver minhas reservas ativas", () => {
    cy.get(selectors.reservationSection).first().should('be.visible');
  });
  
  Then("devo ver meu histórico de reservas", () => {
    cy.get(selectors.historySection).first().should('be.visible');
  });
  
  
  Then('devo ver a mensagem "Não há reservas ativas no momento"', () => {
    cy.get(selectors.reservationSection).first().within(() => {
      cy.contains('Não há reservas ativas no momento').should('be.visible');
    });
  });
  
  Then('devo ver a mensagem "Não há histórico de reservas"', () => {
    cy.get(selectors.historySection).first().within(() => {
      cy.contains('Não há histórico de reservas').should('be.visible');
    });
  });
  
  Then("devo ser redirecionado para a página inicial", () => {
    // Verifica se a URL corresponde a qualquer uma das possíveis URLs base
    cy.url().should('match', /(http:\/\/localhost:3000\/|http:\/\/127.0.0.1:5000\/)/);
  });
  
  Then("a reserva deve aparecer no histórico", () => {
    cy.get(selectors.historySection).first().within(() => {
      cy.contains('Reserva cancelada').should('be.visible');
    });
  });