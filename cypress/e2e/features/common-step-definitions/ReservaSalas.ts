import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

Given("eu estou logado na página {string}", (page: string) => {
  cy.visit(`/${page}`);
});

Given(
  'existe uma reserva na sala {string} para o dia {string} das {string} às {string}',
  (salaNome: string, data: string, horaInicio: string, horaFim: string) => {
    const salaId = getSalaIdFromNome(salaNome);

    cy.request('GET', 'http://127.0.0.1:5000/api/reservas/3').then((res) => {
      const reservas = res.body;
      const existeReserva = reservas.some(
        (r: any) =>
          r.sala_id === salaId &&
          r.data === data &&
          r.start_time === horaInicio &&
          r.end_time === horaFim &&
          r.status === 'ativa'
      );

      if (!existeReserva) {
        cy.request('POST', `http://127.0.0.1:5000/api/reservas/3`, {
          sala_id: salaId,
          data,
          start_time: horaInicio,
          end_time: horaFim,
        }).then((response) => {
          expect(response.status).to.eq(201);
        });
      }
    });
  }
);

// Util function to map sala names to IDs
function getSalaIdFromNome(nome: string): number {
  const mapaSalas: Record<string, number> = {
    "E001": 1,
    "E002": 2,
    "E003": 3,
  };
  return mapaSalas[nome] || 1;
}

Given("no campo {string} está selecionado {string}", (campo: string, valor: string) => {
  cy.get(`label:contains("${campo}")`)
    .parent()
    .find("select")
    .select(valor);
});

Given("no campo {string} está inserido {string}", (campo: string, valor: string) => {
  cy.get(`label:contains("${campo}")`)
    .parent()
    .find("input[type='date'], input[type='text'], input[type='time']")
    .each(($el) => {
      if ($el.is("input")) {
        cy.wrap($el).type(valor);
      } else if ($el.is("select")) {
        cy.wrap($el).select(valor);
      }
    });
});

Given("no campo {string} está selecionada a opção {string}", (campo: string, valor: string) => {
  if (campo === "Equipamentos") {
    cy.contains("Equipamentos").parent().find("button").click();
    cy.contains("label", valor)
      .find("input[type='checkbox']")
      .check({ force: true });
  } else {
    cy.get(`label:contains("${campo}")`)
      .parent()
      .find("input[type='time'], select")
      .type(valor);
  }
});

When("eu seleciono a opção {string}", (botao: string) => {
  cy.contains("button", botao).click();
});

When('eu clico no botão {string} da sala {string}', (button: string, salaNome: string) => {
  cy.contains("strong", `Sala ${salaNome}`)
    .parents(".sala-card")
    .within(() => {
      cy.contains("button", "Reservar").click();
    });
});

Then("é exibida a sala {string} como sala disponível", (salaNome: string) => {
  cy.contains(`Sala ${salaNome}`).should("exist");
  cy.contains(`Sala ${salaNome}`)
    .parent()
    .within(() => {
      cy.get("span").contains("(").should("exist"); // verifica que há avaliação
    });
});

Then("uma mensagem informa que nenhuma sala está disponível", () => {
  cy.contains("Não temos sala disponível").should("exist");
});

Then("o sistema deve exibir a mensagem {string}", (mensagem: string) => {
  cy.on("window:alert", (alerta) => {
    expect(alerta).to.equal(mensagem);
  });
});