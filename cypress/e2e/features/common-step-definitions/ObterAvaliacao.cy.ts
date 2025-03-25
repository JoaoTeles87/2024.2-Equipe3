describe("Obtenção de Avaliação Individual", () => {
    beforeEach(() => {
      cy.intercept("GET", "http://127.0.0.1:5000/api/reviews/1", {
        statusCode: 200,
        body: {
          id: 1,
          reserva_id: 101,
          sala_id: 202,
          usuario_id: 303,
          nota: 5,
          comentario: "Ótima sala, muito confortável!",
          data_avaliacao: "2025-03-25T14:30:00Z",
        },
      }).as("getReviewSuccess");
  
      cy.intercept("GET", "http://127.0.0.1:5000/api/reviews/999", {
        statusCode: 404,
        body: { error: "Avaliação não encontrada para o ID fornecido." },
      }).as("getReviewNotFound");
    });
  
    it("Deve exibir os detalhes de uma avaliação existente", () => {
      cy.visit("/avaliacoes/1");
  
      cy.wait("@getReviewSuccess");
  
      cy.contains("Detalhes da Avaliação #1").should("be.visible");
      cy.contains("ID da Reserva:").should("be.visible");
      cy.contains("ID da Sala:").should("be.visible");
      cy.contains("ID do Usuário:").should("be.visible");
      cy.contains("Nota:").should("be.visible");
      cy.contains("Ótima sala, muito confortável!").should("be.visible");
      cy.contains("25/03/2025").should("be.visible");
    });
  
    it("Deve exibir uma mensagem de erro para uma avaliação inexistente", () => {
      cy.visit("/avaliacoes/999");
  
      cy.wait("@getReviewNotFound");
  
      cy.contains("Avaliação não encontrada para o ID fornecido.").should("be.visible");
      cy.contains("Voltar").should("be.visible").click();
      cy.visit('/avaliacoes');
    });
  });
  