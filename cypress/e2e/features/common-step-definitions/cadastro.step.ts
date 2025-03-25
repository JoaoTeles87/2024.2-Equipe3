import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

// URL da página de cadastro
const cadastroUrl = "/cadastro";
const loginUrl = "/";

// Elementos da página baseados no seu HTML
const nomeInput = 'input[type="text"][placeholder="Nome"]';
const cpfInput = 'input[type="text"][placeholder="CPF"]';
const emailInput = 'input[type="email"][placeholder="Email"]';
const senhaInput = 'input[type="password"][placeholder="Senha"]';
const confirmarSenhaInput = 'input[type="password"][placeholder="Confirmar senha"]';
const professorSelect = 'select';
const siapeInput = 'input[type="text"][placeholder="SIAPE"]';
const criarButton = 'button:contains("Criar")';
const errorMessageContainer = '.error-message'; 
const successMessageContainer = 'div[style*="color: green"]';
const voltarLoginButton = 'button:contains("Voltar à Área de Login")';
const jaPossuoContaLink = 'span.link:contains("Já possuo uma conta")';

// Steps para cadastro
Given("o usuário está na página de cadastro", () => {
  cy.visit(cadastroUrl);
  cy.contains("Sistema de Agendamento e").should("be.visible");
});

When("ele preenche o campo de nome com {string}", (nome: string) => {
  cy.get(nomeInput).clear().type(nome);
});

When("ele preenche o campo de CPF com {string}", (cpf: string) => {
  cy.get(cpfInput).clear().type(cpf);
});

When("ele preenche o campo de email com {string}", (email: string) => {
  cy.get(emailInput).clear().type(email);
});

When("ele preenche o campo de senha com {string}", (senha: string) => {
  cy.get(senhaInput).clear().type(senha);
});

When("ele preenche o campo de confirmar senha com {string}", (senha: string) => {
  cy.get(confirmarSenhaInput).clear().type(senha);
});

When("ele seleciona a opção {string} para professor", (opcao: string) => {
  cy.get(professorSelect).select(opcao);
});

When("ele preenche o campo SIAPE com {string}", (siape: string) => {
  cy.get(siapeInput).clear().type(siape);
});

When("ele clica no botão {string}", (buttonText: string) => {
  cy.contains("button", buttonText).click();
});

When("ele clica no link {string}", (linkText: string) => {
  cy.contains("span.link", linkText).click();
});

Then("ele deve ver uma mensagem de sucesso", () => {
  cy.get(successMessageContainer).should("be.visible");
});

Then("deve haver um botão para voltar à área de login", () => {
  cy.get(voltarLoginButton).should("be.visible");
});

Then("ele deve ver uma mensagem de erro {string}", (message: string) => {
  cy.get(errorMessageContainer).should("contain", message);
});

Then("ele deve ser redirecionado para a página de login", () => {
  cy.url().should("eq", Cypress.config().baseUrl + loginUrl);
});