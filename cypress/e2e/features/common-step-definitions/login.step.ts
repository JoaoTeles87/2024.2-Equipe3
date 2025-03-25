import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

// URL da página de login e home
const loginUrl = "/";
const homeUrl = "/home"; // Ajustar conforme o caminho real da sua aplicação
const cadastroUrl = "/cadastro";

// Elementos da página baseados no seu HTML
const emailInput = 'input[type="email"][placeholder="Email"]';
const passwordInput = 'input[type="password"][placeholder="Senha"]';
const loginButton = 'button[type="submit"]';
const errorMessageContainer = '.error-message'; // Ajuste para o seletor real do seu componente ErrorMessage
const naoCadastradoLink = 'span.link:contains("Não tem conta ainda?")';
const userInfoElement = '[data-testid="user-info"]'; // Ajuste para o seletor real onde o email do usuário é exibido

// Steps para login
Given("o usuário está na página de login", () => {
  cy.visit(loginUrl);
  cy.contains("Sistema de Agendamento e").should("be.visible");
});

When("ele preenche o campo de email com {string}", (email: string) => {
  cy.get(emailInput).clear().type(email);
});

When("ele preenche o campo de senha com {string}", (password: string) => {
  cy.get(passwordInput).clear().type(password);
});

When("ele clica no botão {string}", (buttonText: string) => {
  cy.get(loginButton).contains(buttonText).click();
});

When("ele clica no botão {string} sem preencher os campos", (buttonText: string) => {
  cy.get(emailInput).clear();
  cy.get(passwordInput).clear();
  cy.get(loginButton).contains(buttonText).click();
});

When("ele clica no link {string}", (linkText: string) => {
  cy.contains("span.link", linkText).click();
});

Then("ele deve ser redirecionado para a página principal", () => {
  cy.url().should("include", homeUrl);
});

Then("ele deve ver seu email {string} na tela", (email: string) => {
  cy.get(userInfoElement).should("contain", email);
});

Then("ele deve ver uma mensagem de erro {string}", (message: string) => {
  cy.get(errorMessageContainer).should("contain", message);
});

Then("ele deve permanecer na página de login", () => {
  cy.url().should("eq", Cypress.config().baseUrl + loginUrl);
});

Then("ele deve ser redirecionado para a página de cadastro", () => {
  cy.url().should("include", cadastroUrl);
});